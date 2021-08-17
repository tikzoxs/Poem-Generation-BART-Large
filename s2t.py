#export GOOGLE_APPLICATION_CREDENTIALS="/home/tharindu/Desktop/black/GoogleCloudProjects/dragon/dragon-project-313222-28d7d9fd60f0.json"
import io

def transcribe_file(speech_file):
    """Transcribe the given audio file asynchronously."""
    from google.cloud import speech

    client = speech.SpeechClient()

    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    """
     Note that transcription is limited to a 60 seconds audio file.
     Use a GCS file for audio longer than 1 minute.
    """
    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
    )


    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    in_text = ''
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        in_text = in_text + result.alternatives[0].transcript
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))

    return in_text