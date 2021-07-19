"""Synthesizes speech from the input string of text or ssml.

#export GOOGLE_APPLICATION_CREDENTIALS="/home/tharindu/Desktop/black/GoogleCloudProjects/dragon/dragon-project-313222-28d7d9fd60f0.json"



Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.playback import play
import io
import random

country_list = ['US', 'AU', 'IN', 'UK']
variants = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
voices_list = {'AU':[0,1,2,3], 'IN':[0,1,2,3], 'UK':[0,1,2,3,5], 'US':[0,1,2,3,4,5,6,7,8,9]}

# en-AU-Wavenet-C
# en-GB-Wavenet-C
# en-GB-Wavenet-F
# en-US-Wavenet-C
# en-US-Wavenet-F

# en-GB-Wavenet-D
# en-US-Wavenet-B
# en-US-Wavenet-D
# en-US-Wavenet-I



def voice_selector(emotion):
	if(emotion == 'joy'):
		accent = 'en-US'
		voice_id = '-Wavenet-B'
		gender = 'MALE'
	elif(emotion == 'protect'):
		accent = 'en-US'
		voice_id = '-Wavenet-C'
		gender = 'FEMALE'
	elif(emotion == 'attack'):
		accent = 'en-GB'
		voice_id = '-Wavenet-A'
		gender = 'FEMALE'
	else:
		accent = 'en-US'
		voice_id = '-Wavenet-A'
		gender = 'MALE'
	return accent, accent+voice_id, gender

def get_speed_and_pitch(emotion):
	if(emotion == 'joy'):
		speed = 0.9
		pitch = 3
	elif(emotion == 'protect'):
		speed = 0.8
		pitch = 4
	elif(emotion == 'attack'):
		speed = 0.75
		pitch = 0
	else:
		speed = 0.9
		pitch = -4
	return speed, pitch

# poem = "Synthesizes speech from the input string of text or ssml. perform the text-to-speech request on the text input with the selected voice parameters and audio file type"

def text_to_voice(poem, question, emotion):
	global country_list,variants,voices_list
	# Instantiates a client
	client = texttospeech.TextToSpeechClient()

	# Set the text input to be synthesized
	synthesis_input = texttospeech.SynthesisInput(text=poem+question)

	# Build the voice request, select the language code ("en-US") and the ssml
	# voice gender ("neutral")
	
	accent, voice_id, gender= voice_selector(emotion)
	print(accent, voice_id, gender)
	voice = texttospeech.VoiceSelectionParams(
	    language_code=accent, name=voice_id
	) #ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL

	# Select the type of audio file you want returned
	speaking_rate, pitch = get_speed_and_pitch(emotion)
	print(speaking_rate, pitch)
	audio_config = texttospeech.AudioConfig(
	    audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=speaking_rate, pitch=pitch
	)

	# Perform the text-to-speech request on the text input with the selected
	# voice parameters and audio file type
	response = client.synthesize_speech(
	    input=synthesis_input, voice=voice, audio_config=audio_config
	)

	# The response's audio_content is binary.
	filename = "output1.mp3"
	with open(filename, "wb") as out:
	    # Write the response to the output file.
	    out.write(response.audio_content)
	    print('Audio content written to file "output.mp3"')

	with open(filename, 'rb') as voice:
		data = voice.read()
		song = AudioSegment.from_mp3(filename)
		play(song)


# text_to_voice("i am so sad that this is happening to me. to be honest, i never expected to test this out, this soon. by the way, how are you feeling now?", "so?", 'caution')