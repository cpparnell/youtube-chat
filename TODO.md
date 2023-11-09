# TODO

Finish implmenting send_message() and get_response()

- need to add validation/restrictions:
    - responses must stay on topic of video
    - nonsense(non-question, irrelevant to video) inputs should be responded to wtih encouragement to ask questions about the video
    - find and replace transcription with video

- figure out a way to either get whisper.cpp working, or use Mac M2 graphics processing to speed up initial transcription.

#### Longterm:

- implement annotations
- provide more files
- user interface where you watch the video and hop to points based on questions

- **turn into live video chat where you can ask questions as you go, forgo summary**

