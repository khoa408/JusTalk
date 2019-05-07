import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
# Imports the Google Cloud client library
from google.cloud import translate

def Speech_to_text():
	# Instantiates a client
	client = speech.SpeechClient()

	# The name of the audio file to transcribe
	file_name = os.path.join('/Users','khoatran','Desktop',
				'Repositories','JusTalk','JusTalkENV','thisisatest.wav')

	# Loads the audio into memory
	with io.open(file_name, 'rb') as audio_file:
	    content = audio_file.read()
	    audio = types.RecognitionAudio(content=content)

	config = types.RecognitionConfig(
	    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
	    sample_rate_hertz=8000,
	    language_code='en-US')

	# Detects speech in the audio file
	response = client.recognize(config, audio)

	for result in response.results:
	    print('Transcript: {}'.format(result.alternatives[0].transcript))
	print("Print out result", result)
	return result

def Translation(text):
	# Instantiates a client
	translate_client = translate.Client()

	# The target language
	target = 'zh-CN'

	# Translates some text into Russian
	translation = translate_client.translate(
	    text.alternatives[0].transcript,
	    target_language=target)

	print(u'Text: {}'.format(text))
	print(u'Translation: {}'.format(translation['translatedText']))

def main():
	speech2txt_result = Speech_to_text()
	Translation(speech2txt_result)

main()
