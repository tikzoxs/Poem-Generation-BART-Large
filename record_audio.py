import pyaudio
import wave
import s2t
# from communication import comm

def record_and_transcribe(time_s):
	filename = "recordings/recorded.wav"

	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	RECORD_SECONDS = 10
	WAVE_OUTPUT_FILENAME = "output.wav"

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
	                channels=CHANNELS,
	                rate=RATE,
	                input=True,
	                frames_per_buffer=CHUNK)

	print("* recording")

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)

	print("* done recording")

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

	return s2t.transcribe_file(filename)

# def record_and_transcribe(time_s):
# 	# the file name output you want to record into
# 	# comm("recrding")
# 	filename = "recordings/recorded.wav"
# 	# set the chunk size of 1024 samples
# 	chunk = 1024
# 	# sample format
# 	FORMAT = pyaudio.paInt16
# 	# mono, change to 2 if you want stereo
# 	channels = 1
# 	# 44100 samples per second
# 	sample_rate = 44100
# 	record_seconds = time_s
# 	# initialize PyAudio object
# 	p = pyaudio.PyAudio()
# 	# open stream object as input & output
# 	stream = p.open(format=FORMAT,
# 	                channels=channels,
# 	                rate=sample_rate,
# 	                input=True,
# 	                output=True,
# 	                frames_per_buffer=chunk)
# 	frames = []
# 	print("Recording...")
# 	for i in range(int(44100 / chunk * record_seconds)):
# 	    data = stream.read(chunk)
# 	    # if you want to hear your voice while recording
# 	    # stream.write(data)
# 	    frames.append(data)
# 	print("Finished recording.")
# 	# stop and close stream
# 	stream.stop_stream()
# 	stream.close()
# 	# terminate pyaudio object
# 	p.terminate()
# 	# save audio file
# 	# open the file in 'write bytes' mode
# 	wf = wave.open(filename, "wb")
# 	# set the channels
# 	wf.setnchannels(channels)
# 	# set the sample format
# 	wf.setsampwidth(p.get_sample_size(FORMAT))
# 	# set the sample rate
# 	wf.setframerate(sample_rate)
# 	# write the frames as bytes
# 	wf.writeframes(b"".join(frames))
# 	# close the file
# 	wf.close()
# 	# comm("processing")

# 	return s2t.transcribe_file(filename)