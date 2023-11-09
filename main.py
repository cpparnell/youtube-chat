import sys
from pathlib import Path
import tempfile
# Add the directory containing your package to the Python path
sys.path.append(str(Path(__file__).resolve().parent))

from src.utils import AudioDownloader, Transcriber, OpenAIAssistantManager


GREEN = '\033[92m'
RESET = '\033[0m'

if __name__ == "__main__":
    video_url = input("Enter YouTube video url: ")
    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = AudioDownloader.download_audio_from_youtube(video_url=video_url, output_path=temp_dir, filename='audio.mp4')
        Transcriber.transcribe_audio_to_file(filepath, temp_dir, 'trans.txt')
        manager = OpenAIAssistantManager(temp_dir, 'trans.txt')
        summary = manager.create_summary()
        print('\nSummary of Video:' + summary)
        while True:
            question = input(f"\n{GREEN}What other questions do you have?{RESET}\n")
            if question.lower() in ['none', 'exit', 'quit']:
                break
            # TODO validate question makes sense
            content = manager.send_message(question)
            response = manager.get_response()
            # TODO validate response makes sense
            if response == None:
                # there is something deeply wrong
                raise Exception("Assistant did not provide a response!")
            print(response)