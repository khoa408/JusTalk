# -*- coding: UTF-8 -*-
import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
# Imports the Google Cloud client library
from google.cloud import translate

def Record():
	import pyaudio
	import wave
	 
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	CHUNK = 1024
	RECORD_SECONDS = 5
	WAVE_OUTPUT_FILENAME = "file.wav"
	 
	audio = pyaudio.PyAudio()
	 
	# start Recording
	stream = audio.open(format=FORMAT, channels=CHANNELS,
	                rate=RATE, input=True,
	                frames_per_buffer=CHUNK)
	print "Recording..."
	frames = []
	 
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)
	print "Finished Recording"
	 
	 
	# stop Recording
	stream.stop_stream()
	stream.close()
	audio.terminate()
	 
	waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	waveFile.setnchannels(CHANNELS)
	waveFile.setsampwidth(audio.get_sample_size(FORMAT))
	waveFile.setframerate(RATE)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()

def Speech_to_text(input_language_code):
	# Instantiates a client
	client = speech.SpeechClient()

	# The name of the audio file to transcribe
	file_name = os.path.join('/Users','khoatran','Desktop',
				'Repositories','JusTalk','file.wav')

	# Loads the audio into memory
	with io.open(file_name, 'rb') as audio_file:
	    content = audio_file.read()
	    audio = types.RecognitionAudio(content=content)

	config = types.RecognitionConfig(
	    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
	    sample_rate_hertz=44100,
	    language_code = input_language_code)

	# Detects speech in the audio file
	response = client.recognize(config, audio)

	for result in response.results:
		print('Transcript: {}'.format(result.alternatives[0].transcript))
		print("Print out result", result)
	
	# return str(result.alternatives[0].transcript)
	return result

def Translation(text,language):
	# @inputs: Text, Target Language
	# @output: Translated Text
	
	# Instantiates a client
	translate_client = translate.Client()

	# The target language
	target = str(language)

	# Translates the text to the target language
	translation = translate_client.translate(text.alternatives[0].transcript,target_language=language)

	print(u'Text: {}'.format(text))
	print(u'Translation: {}'.format(translation['translatedText']))

	#return translation
	return translation

def Text_to_speech(translated_text,translated_language_code):
	from google.cloud import texttospeech

	# Instantiates a client
	client = texttospeech.TextToSpeechClient()

	# Set the text input to be synthesized
	synthesis_input = texttospeech.types.SynthesisInput(text=u'{}'.format(translated_text))

	# Build the voice request, select the language code ("en-US") and the ssml
	# voice gender ("neutral")
	voice = texttospeech.types.VoiceSelectionParams(
	    language_code = translated_language_code,
	    ssml_gender = texttospeech.enums.SsmlVoiceGender.NEUTRAL)

	# Select the type of audio file you want returned
	audio_config = texttospeech.types.AudioConfig(
	    audio_encoding = texttospeech.enums.AudioEncoding.MP3)

	# Perform the text-to-speech request on the text input with the selected
	# voice parameters and audio file type
	response = client.synthesize_speech(synthesis_input, voice, audio_config)

	# The response's audio_content is binary.
	with open('output.mp3', 'wb') as out:
	    # Write the response to the output file.
	    out.write(response.audio_content)
	    print('Audio content written to file "output.mp3"')

def menu():
	language_list =[[1,"Afrikaans(South Africa) | Afrikaans(Suid-Afrika)","af-ZA"],	
					[2,"Amharic(Ethiopia)አማርኛ | (ኢትዮጵያ)","am-ET"],	
					[3,"Armenian(Armenia)Հայ | (Հայաստան)","hy-AM"],	
					[4,"Azerbaijani(Azerbaijan) | Azərbaycan(Azərbaycan)","az-AZ"],
					[5,"Arabic(Israel) | العربية (إسرائيل)","ar-IL"],
					[6,"Arabic(Jordan) | العربية (الأردن)","ar-JO"],	
					[7,"Arabic(United Arab Emirates) | العربية (الإمارات)","ar-AE"],	
					[8,"Arabic(Bahrain) | العربية (البحرين)","ar-BH"],	
					[9,"Arabic(Algeria) | العربية (الجزائر)","ar-DZ"],	
					[10,"Arabic(Saudi Arabia) | العربية (السعودية)","ar-SA"],	
					[11,"Arabic(Iraq) | العربية (العراق)","ar-IQ"],	
					[12,"Arabic(Kuwait) | العربية (الكويت)","ar-KW"],
					[13,"Arabic(Morocco) | العربية (المغرب)","ar-MA"],	
					[14,"Arabic(Tunisia) | العربية (تونس)","ar-TN"],	
					[15,"Arabic(Oman) | العربية (عُمان)","ar-OM"],	
					[16,"Arabic(State of Palestine) | العربية (فلسطين)","ar-PS"],	
					[17,"Arabic(Qatar) | العربية (قطر)","ar-QA"],	
					[18,"Arabic(Lebanon) | العربية (لبنان)","ar-LB"],	
					[19,"Arabic(Egypt) | العربية (مصر)","ar-EG"],	
					[20,"Bengali(Bangladesh) | বাংলা (বাংলাদেশ)","bn-BD"],	
					[21,"Bengali(India) | বাংলা (ভারত)","bn-IN"],	
					[22,"Basque(Spain) | Euskara (Espainia)","eu-ES"],	
					[23,"Bulgarian(Bulgaria) | Български (България)","bg-BG"],
					[24,"Croatian(Croatia) | Hrvatski (Hrvatska)","hr-HR"],	
					[25,"Catalan(Spain) | Català (Espanya)","ca-ES"],	
					[26,"Czech(Czech Republic) | Čeština (Česká republika)","cs-CZ"],	
					[27,"Chinese,Mandarin(Traditional, Taiwan) | 國語 (台灣)"	,"zh-TW"],	
					[28,"Chinese,Cantonese(Traditional, Hong Kong) | 廣東話 (香港)","yue-Hant-HK"],	
					[29,"Chinese,Mandarin(Simplified, Hong Kong) | 普通話 (香港)","zh-HK"],	
					[30,"Chinese,Mandarin(Simplified, China) | 普通话 (中国大陆)","zh"],	
					[31,"Danish(Denmark) | Dansk (Danmark)","da-DK"],	
					[32,"Dutch(Netherlands) | Nederlands (Nederland)","nl-NL"],	
					[33,"English(Australia) | English (Australia)","en-AU"],	
					[34,"English(Canada) | English (Canada)","en-CA"],	
					[35,"English(Ghana) | English (Ghana)","en-GH"],	
					[36,"English(United Kingdom) | English (Great Britain)","en-GB"],	
					[37,"English(India) | English (India)","en-IN"],	
					[38,"English(Ireland) | English (Ireland)","en-IE"],	
					[39,"English(Kenya) | English (Kenya)","en-KE"],	
					[40,"English(New Zealand) | English (New Zealand)","en-NZ"],	
					[41,"English(Nigeria) | English (Nigeria)","en-NG"],	
					[42,"English(Philippines) | English (Philippines)","en-PH"],	
					[43,"English(Singapore) | English (Singapore)","en-SG"],	
					[44,"English(South Africa) | English (South Africa)","en-ZA"],	
					[45,"English(Tanzania) | English (Tanzania)","en-TZ"],	
					[46,"English(United States) | English (United States)","en-US"],	
					[47,"Filipino(Philippines) | Filipino (Pilipinas)","fil-PH"],	
					[48,"Finnish(Finland) | Suomi (Suomi)","fi-FI"],	
					[49,"French(Canada) | Français (Canada)","fr-CA"],	
					[50,"French(France) | Français (France)","fr-FR"],	
					[51,"Greek(Greece) | Ελληνικά (Ελλάδα)","el-GR"],	
					[52,"Galician(Spain) | Galego (España)","gl-ES"],	
					[53,"Georgian(Georgia) | ქართული (საქართველო)","ka-GE"],	
					[54,"Gujarati(India) | ગુજરાતી (ભારત)","gu-IN"],	
					[55,"German(Germany) | Deutsch (Deutschland)","de-DE"],	
					[56,"Hebrew(Israel) | עברית (ישראל)","he-IL"],	
					[57,"Hindi(India) | हिन्दी (भारत)","hi-IN"],	
					[58,"Hungarian(Hungary) | Magyar (Magyarország)","hu-HU"],	
					[59,"Indonesian(Indonesia) | Bahasa Indonesia(Indonesia)","id-ID"],	
					[60,"Icelandic(Iceland) | Íslenska (Ísland)","is-IS"],	
					[61,"Italian(Italy) | Italiano (Italia)","it-IT"],	
					[62,"Javanese(Indonesia) | Jawa (Indonesia)","jv-ID"],	
					[63,"Japanese(Japan) | 日本語（日本）"	,"ja-JP"],
					[64,"Korean(South Korea) | 한국어 (대한민국)","ko-KR"],	
					[65,"Kannada(India) | ಕನ್ನಡ (ಭಾರತ)"	,"kn-IN"],	
					[66,"Khmer(Cambodia) | ភាសាខ្មែរ (កម្ពុជា)","km-KH"],	
					[67,"Lao(Laos) | ລາວ (ລາວ)","lo-LA"],
					[68,"Latvian(Latvia) | Latviešu (latviešu)","lv-LV"],	
					[69,"Lithuanian(Lithuania) | Lietuvių (Lietuva)","lt-LT"],	
					[70,"Malay(Malaysia) | Bahasa Melayu (Malaysia)","ms-MY"],	
					[71,"Malayalam(India) | മലയാളം (ഇന്ത്യ)","ml-IN"],	
					[72,"Marathi(India) | मराठी (भारत)","mr-IN"],	
					[73,"Nepali(Nepal) | नेपाली (नेपाल)","ne-NP"],	
					[74,"Norwegian Bokmål(Norway) | Norsk bokmål (Norge)","nb-NO"],	
					[75,"Persian(Iran) | فارسی (ایران)","fa-IR"],	
					[76,"Polish(Poland) | Polski (Polska)","pl-PL"],	
					[77,"Portuguese(Brazil) | Português (Brasil)","pt-BR"],	
					[78,"Portuguese(Portugal) | Português (Portugal)","pt-PT"],	
					[79,"Romanian(Romania) | Română (România)","ro-RO"],				
					[80,"Russian(Russia) | Русский (Россия)","ru-RU"],
					[81,"Spanish(Argentina) | Español (Argentina)","es-AR"],	
					[82,"Spanish(Bolivia) | Español (Bolivia)","es-BO"],	
					[83,"Spanish(Chile) | Español (Chile)","es-CL"],	
					[84,"Spanish(Colombia | Español (Colombia)","es-CO"],	
					[85,"Spanish(Costa Rica) | Español (Costa Rica)","es-CR"],	
					[86,"Spanish(Ecuador) | Español (Ecuador)","es-EC"],
					[87,"Spanish(El Salvador) | Español (El Salvador)","es-SV"],	
					[88,"Spanish(Spain) | Español (España)","es-ES"],
					[89,"Spanish(United States) | Español (Estados Unidos)","es-US"],	
					[90,"Spanish(Guatemala) | Español (Guatemala)","es-GT"],	
					[91,"Spanish(Honduras) | Español (Honduras)","es-HN"],	
					[92,"Spanish(Mexico) | Español (México)","es-MX"],	
					[93,"Spanish(Nicaragua) | Español (Nicaragua)","es-NI"],	
					[94,"Spanish(Panama) | Español (Panamá)","es-PA"],	
					[95,"Spanish(Paraguay) | Español (Paraguay)","es-PY"],	
					[96,"Spanish(Peru) | Español (Perú)","es-PE"],	
					[97,"Spanish(Puerto Rico) | Español (Puerto Rico)","es-PR"],	
					[98,"Spanish(Dominican Republic) | Español (República Dominicana)","es-DO"],	
					[99,"Spanish(Uruguay) | Español (Uruguay)","es-UY"],	
					[100,"Spanish(Venezuela) | Español (Venezuela)","es-VE"],		
					[101,"Serbian(Serbia) | Српски (Србија)","sr-RS"],
					[102,"Sinhala(Sri Lanka) | සිංහල (ශ්රී ලංකාව)","si-LK"],	
					[103,"Slovak(Slovakia) | Slovenčina (Slovensko)","sk-SK"],	
					[104,"Slovenian(Slovenia) | Slovenščina (Slovenija)","sl-SI"],	
					[105,"Sundanese(Indonesia) | Urang (Indonesia)","su-ID"],	
					[106,"Swahili(Tanzania) | Swahili (Tanzania)","sw-TZ"],	
					[107,"Swahili(Kenya) | Swahili (Kenya)","sw-KE"],	
					[108,"Swedish(Sweden) | Svenska (Sverige)","sv-SE"],
					[109,"Tamil(India) | தமிழ் (இந்தியா)","ta-IN"],	
					[110,"Tamil(Singapore) | தமிழ் (சிங்கப்பூர்)","ta-SG"],	
					[111,"Tamil(Sri Lanka) | தமிழ் (இலங்கை)","ta-LK"],	
					[112,"Tamil(Malaysia) | தமிழ் (மலேசியா)","ta-MY"],	
					[113,"Telugu(India) | తెలుగు (భారతదేశం)","te-IN"],	
					[114,"Turkish(Turkey) | Türkçe (Türkiye)","tr-TR"],		
					[115,"Thai(Thailand) | ไทย (ประเทศไทย)","th-TH"],	
					[116,"Ukrainian(Ukraine) | Українська (Україна)","uk-UA"],	
					[117,"Urdu(Pakistan) | اردو (پاکستان)","ur-PK"],	
					[118,"Urdu(India) | اردو (بھارت)","ur-IN"],	
					[119,"Vietnamese(Vietnam) | Tiếng Việt (Việt Nam)","vi-VN"],
					[120,"Zulu(South Africa) | IsiZulu (Ningizimu Afrika)","zu-ZA"]]	
	
	isSelected = False
	while(isSelected is False):
		for language in language_list:
			print language[0],language[1]
		in_language_num = int(raw_input("Input Language: "))
		out_language_num = int(raw_input("Output Language: "))
		if((in_language_num > 0 and in_language_num <= 120) and (out_language_num > 0 and out_language_num <= 120)):
			isSelected = True
		else:
			print "Invalid Option, Please Try Again"
			continue
	for language in language_list:
		if(language[0]==in_language_num):
			in_language = language[2]
			print "Input Language: ",language[1]
		if(language[0]==out_language_num):
			out_language = language[2]
			print "Output Language: ",language[1]

	return in_language,out_language

def main():
	in_language, out_language = menu()
	Record()
	speech2txt_result = Speech_to_text(in_language)
	translated_text = Translation(speech2txt_result,'es')
	Text_to_speech(translated_text,out_language)

main()
