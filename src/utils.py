from pytube import YouTube
import whisper
import os
import openai
import re

from .exceptions import InvalidYouTubeUrlError

openai.api_key = os.environ['OPENAI_API_KEY']

class AudioDownloader:
    def is_youtube_video_url(url: str) -> bool:
        """
        Validates if the provided URL is a valid YouTube video URL.
        """
        # Patterns for various YouTube URL formats
        youtube_regex_patterns = [
            r'(https?://)?(www\.)?(youtube\.com/watch\?v=)([a-zA-Z0-9_-]{11})',
            r'(https?://)?(www\.)?(youtu\.be/)([a-zA-Z0-9_-]{11})'
        ]

        for pattern in youtube_regex_patterns:
            match = re.match(pattern, url)
            if match:
                return True
        return False


    def download_audio_from_youtube(video_url: str, output_path: str, filename: str) -> str:
        if not AudioDownloader.is_youtube_video_url(video_url):
            raise InvalidYouTubeUrlError(f"The provided url is not a YouTube video: {video_url}")
        yt = YouTube(video_url)
        audio_stream = yt.streams.get_audio_only()
        file_location = audio_stream.download(output_path=output_path, filename=filename)
        print(f'Downloaded: {audio_stream.title}')
        return file_location

class Transcriber:

    def transcribe_audio_to_file(audio_path: str, output_path: str, filename: str):
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, fp16=False)
        with open(os.path.join(output_path, filename), "w") as f:
            f.write(result["text"])
    

class OpenAIAssistantManager:
    
    def __init__(self, path: str, filename: str) -> None:
        self.assistant = self.__create_assistant(path, filename)
        self.thread = openai.beta.threads.create()
    
    def __create_assistant(self, path: str, filename: str): # creates Assistant
        # create FileObject from transcription
        file = openai.files.create(file=open(os.path.join(path, filename), 'rb'), purpose='assistants')
        response = openai.beta.assistants.create(
            name="Domain Expert",
            instructions="You are a an expert on the topic described in the attached video transcription. Be prepared to summarize and answer questions about the subject matter based on the transcription. Your answers should be SHORT and INFORMATIVE. Do NOT answer any questions that are not directly related to the transcription.",
            tools=[{"type": "retrieval"}],
            model="gpt-4-1106-preview",
            file_ids=[file.id]
        )
        return response

    def create_summary(self):
        message = openai.beta.threads.messages.create(thread_id=self.thread.id,role="user",content="Please create a succint 1 paragraph summary of the provided transcription. Refer to the transcription as if it is a video.")
        run = openai.beta.threads.runs.create(thread_id=self.thread.id, assistant_id=self.assistant.id)
        while run.status != 'completed':
            run = openai.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=run.id)
        messages = openai.beta.threads.messages.list(thread_id=self.thread.id)
        return messages.data[0].content[0].text.value
    