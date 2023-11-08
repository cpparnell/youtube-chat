from pytube import YouTube
import whisper
import os
import openai

openai.api_key = os.environ['OPENAI_API_KEY']

def download_audio_from_youtube(video_url: str, output_path: str, filename: str) -> str:
    yt = YouTube(video_url)
    audio_stream = yt.streams.get_audio_only()
    file_location = audio_stream.download(output_path=output_path, filename=filename)
    print(f'Downloaded: {audio_stream.title} to {file_location}')
    return file_location

video_url = "https://www.youtube.com/watch?v=H6u0VBqNBQ8"
output_path = "output/"
filename = "example.mp4"
audio_file_path = download_audio_from_youtube(video_url, output_path, filename)

def transcribe_audio_to_file(audio_path: str, output_path: str, filename: str):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, fp16=False)
    with open(os.path.join(output_path, filename), "w") as f:
        f.write(result["text"])
    
transcribe_audio_to_file(audio_file_path, 'output/', 'transcription.txt')

def create_assistant(): # creates Assistant
    # create file object out of transcription
    file = openai.files.create(file=open('output/transcription.txt', 'rb'), purpose='assistants')
    response = openai.beta.assistants.create(
        name="Domain Expert",
        instructions="You are a an expert on the topic described in the attached video transcription. Be prepared to summarize and answer questions about the subject matter based on the transcription. Your answers should be SHORT and INFORMATIVE. Do NOT answer any questions that are not directly related to the transcription.",
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview",
        file_ids=[file.id]
    )
    return response

assistant = create_assistant()

def create_thread(): # creates Thread
    # create thread that will be used by assistant
    thread = openai.beta.threads.create()
    return thread

thread = create_thread()

def create_summary(assistant, thread):
    message = openai.beta.threads.messages.create(thread_id=thread.id,role="user",content="Please create a succint 1 paragraph summary of the provided transcription. Refer to the transcription as if it is a video.")
    run = openai.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
    while run.status != 'completed':
        run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    return messages.data[0].content[0].text.value

summ = create_summary(assistant, thread)
