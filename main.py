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
	print("Recording...")
	frames = []
	 
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)
	print("Finished Recording")
	 
	 
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
	file_name = os.path.join('/home','pi','Desktop',
				'JusTalk','file.wav')

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

	result = None
	for result in response.results:
		print(u'Transcript: {}'.format(result.alternatives[0].transcript))
		print(u"Print out result", result)
	
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
	return translation['translatedText']

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
	language_list =[[1,"Afrikaans(South Africa) | Afrikaans(Suid-Afrika)","af-ZA","af"],	
					[2,"Amharic(Ethiopia)አማርኛ | (ኢትዮጵያ)","am-ET","am"],	
					[3,"Armenian(Armenia)Հայ | (Հայաստան)","hy-AM","hy"],	
					[4,"Azerbaijani(Azerbaijan) | Azərbaycan(Azərbaycan)","az-AZ","az"],
					[5,"Arabic(Israel) | العربية (إسرائيل)","ar-IL","ar"],
					[6,"Arabic(Jordan) | العربية (الأردن)","ar-JO","ar"],	
					[7,"Arabic(United Arab Emirates) | العربية (الإمارات)","ar-AE","ar"],	
					[8,"Arabic(Bahrain) | العربية (البحرين)","ar-BH","ar"],	
					[9,"Arabic(Algeria) | العربية (الجزائر)","ar-DZ","ar"],	
					[10,"Arabic(Saudi Arabia) | العربية (السعودية)","ar-SA","ar"],	
					[11,"Arabic(Iraq) | العربية (العراق)","ar-IQ","ar"],	
					[12,"Arabic(Kuwait) | العربية (الكويت)","ar-KW","ar"],
					[13,"Arabic(Morocco) | العربية (المغرب)","ar-MA","ar"],	
					[14,"Arabic(Tunisia) | العربية (تونس)","ar-TN","ar"],	
					[15,"Arabic(Oman) | العربية (عُمان)","ar-OM","ar"],	
					[16,"Arabic(State of Palestine) | العربية (فلسطين)","ar-PS","ar"],	
					[17,"Arabic(Qatar) | العربية (قطر)","ar-QA","ar"],	
					[18,"Arabic(Lebanon) | العربية (لبنان)","ar-LB","ar"],	
					[19,"Arabic(Egypt) | العربية (مصر)","ar-EG","ar"],	
					[20,"Bengali(Bangladesh) | বাংলা (বাংলাদেশ)","bn-BD","bn"],	
					[21,"Bengali(India) | বাংলা (ভারত)","bn-IN","bn"],	
					[22,"Basque(Spain) | Euskara (Espainia)","eu-ES","eu"],	
					[23,"Bulgarian(Bulgaria) | Български (България)","bg-BG","bg"],
					[24,"Croatian(Croatia) | Hrvatski (Hrvatska)","hr-HR","hr"],	
					[25,"Catalan(Spain) | Català (Espanya)","ca-ES","ca"],	
					[26,"Czech(Czech Republic) | Čeština (Česká republika)","cs-CZ","cs"],	
					[27,"Chinese,Mandarin(Traditional, Taiwan) | 國語 (台灣)"	,"zh-TW","zh-TW"],	
					[28,"Chinese,Cantonese(Traditional, Hong Kong) | 廣東話 (香港)","yue-Hant-HK",None],	
					[29,"Chinese,Mandarin(Simplified, Hong Kong) | 普通話 (香港)","zh-HK","zh-CN"], #Used zh-CN	
					[30,"Chinese,Mandarin(Simplified, China) | 普通话 (中国大陆)","zh","zh-CN"],	
					[31,"Danish(Denmark) | Dansk (Danmark)","da-DK","da"],	
					[32,"Dutch(Netherlands) | Nederlands (Nederland)","nl-NL","nl"],	
					[33,"English(Australia) | English (Australia)","en-AU","en"],	
					[34,"English(Canada) | English (Canada)","en-CA","en"],	
					[35,"English(Ghana) | English (Ghana)","en-GH","en"],	
					[36,"English(United Kingdom) | English (Great Britain)","en-GB","en"],	
					[37,"English(India) | English (India)","en-IN","en"],	
					[38,"English(Ireland) | English (Ireland)","en-IE","en"],	
					[39,"English(Kenya) | English (Kenya)","en-KE","en"],	
					[40,"English(New Zealand) | English (New Zealand)","en-NZ","en"],	
					[41,"English(Nigeria) | English (Nigeria)","en-NG","en"],	
					[42,"English(Philippines) | English (Philippines)","en-PH","en"],	
					[43,"English(Singapore) | English (Singapore)","en-SG","en"],	
					[44,"English(South Africa) | English (South Africa)","en-ZA","en"],	
					[45,"English(Tanzania) | English (Tanzania)","en-TZ","en"],	
					[46,"English(United States) | English (United States)","en-US","en"],	
					[47,"Filipino(Philippines) | Filipino (Pilipinas)","fil-PH","tl"],	
					[48,"Finnish(Finland) | Suomi (Suomi)","fi-FI","fi"],	
					[49,"French(Canada) | Français (Canada)","fr-CA","fr"],	
					[50,"French(France) | Français (France)","fr-FR","fr"],	
					[51,"Greek(Greece) | Ελληνικά (Ελλάδα)","el-GR","el"],	
					[52,"Galician(Spain) | Galego (España)","gl-ES","gl"],	
					[53,"Georgian(Georgia) | ქართული (საქართველო)","ka-GE","ka"],	
					[54,"Gujarati(India) | ગુજરાતી (ભારત)","gu-IN","gu"],	
					[55,"German(Germany) | Deutsch (Deutschland)","de-DE","de"],	
					[56,"Hebrew(Israel) | עברית (ישראל)","he-IL","he**"],	
					[57,"Hindi(India) | हिन्दी (भारत)","hi-IN","hi"],	
					[58,"Hungarian(Hungary) | Magyar (Magyarország)","hu-HU","hu"],	
					[59,"Indonesian(Indonesia) | Bahasa Indonesia(Indonesia)","id-ID","id"],	
					[60,"Icelandic(Iceland) | Íslenska (Ísland)","is-IS","is"],	
					[61,"Italian(Italy) | Italiano (Italia)","it-IT","it"],	
					[62,"Javanese(Indonesia) | Jawa (Indonesia)","jv-ID","jw"],	
					[63,"Japanese(Japan) | 日本語（日本）"	,"ja-JP","ja"],
					[64,"Korean(South Korea) | 한국어 (대한민국)","ko-KR","ko"],	
					[65,"Kannada(India) | ಕನ್ನಡ (ಭಾರತ)"	,"kn-IN","kn"],	
					[66,"Khmer(Cambodia) | ភាសាខ្មែរ (កម្ពុជា)","km-KH","km"],	
					[67,"Lao(Laos) | ລາວ (ລາວ)","lo-LA","lo"],
					[68,"Latvian(Latvia) | Latviešu (latviešu)","lv-LV","lv"],	
					[69,"Lithuanian(Lithuania) | Lietuvių (Lietuva)","lt-LT","lt"],	
					[70,"Malay(Malaysia) | Bahasa Melayu (Malaysia)","ms-MY","ms"],	
					[71,"Malayalam(India) | മലയാളം (ഇന്ത്യ)","ml-IN","ml"],	
					[72,"Marathi(India) | मराठी (भारत)","mr-IN","mr"],	
					[73,"Nepali(Nepal) | नेपाली (नेपाल)","ne-NP","ne"],	
					[74,"Norwegian Bokmål(Norway) | Norsk bokmål (Norge)","nb-NO","no"],	
					[75,"Persian(Iran) | فارسی (ایران)","fa-IR","fa"],	
					[76,"Polish(Poland) | Polski (Polska)","pl-PL","pl"],	
					[77,"Portuguese(Brazil) | Português (Brasil)","pt-BR","pt"],	
					[78,"Portuguese(Portugal) | Português (Portugal)","pt-PT","pt"],	
					[79,"Romanian(Romania) | Română (România)","ro-RO","ro"],				
					[80,"Russian(Russia) | Русский (Россия)","ru-RU","ru"],
					[81,"Spanish(Argentina) | Español (Argentina)","es-AR","es"],	
					[82,"Spanish(Bolivia) | Español (Bolivia)","es-BO","es"],	
					[83,"Spanish(Chile) | Español (Chile)","es-CL","es"],	
					[84,"Spanish(Colombia | Español (Colombia)","es-CO","es"],	
					[85,"Spanish(Costa Rica) | Español (Costa Rica)","es-CR","es"],	
					[86,"Spanish(Ecuador) | Español (Ecuador)","es-EC","es"],
					[87,"Spanish(El Salvador) | Español (El Salvador)","es-SV","es"],	
					[88,"Spanish(Spain) | Español (España)","es-ES","es"],
					[89,"Spanish(United States) | Español (Estados Unidos)","es-US","es"],	
					[90,"Spanish(Guatemala) | Español (Guatemala)","es-GT","es"],	
					[91,"Spanish(Honduras) | Español (Honduras)","es-HN","es"],	
					[92,"Spanish(Mexico) | Español (México)","es-MX","es"],	
					[93,"Spanish(Nicaragua) | Español (Nicaragua)","es-NI","es"],	
					[94,"Spanish(Panama) | Español (Panamá)","es-PA","es"],	
					[95,"Spanish(Paraguay) | Español (Paraguay)","es-PY","es"],	
					[96,"Spanish(Peru) | Español (Perú)","es-PE","es"],	
					[97,"Spanish(Puerto Rico) | Español (Puerto Rico)","es-PR","es"],	
					[98,"Spanish(Dominican Republic) | Español (República Dominicana)","es-DO","es"],	
					[99,"Spanish(Uruguay) | Español (Uruguay)","es-UY","es"],	
					[100,"Spanish(Venezuela) | Español (Venezuela)","es-VE","es"],		
					[101,"Serbian(Serbia) | Српски (Србија)","sr-RS","sr"],
					[102,"Sinhala(Sri Lanka) | සිංහල (ශ්රී ලංකාව)","si-LK","si"],	
					[103,"Slovak(Slovakia) | Slovenčina (Slovensko)","sk-SK","sk"],	
					[104,"Slovenian(Slovenia) | Slovenščina (Slovenija)","sl-SI","sl"],	
					[105,"Sundanese(Indonesia) | Urang (Indonesia)","su-ID","su"],	
					[106,"Swahili(Tanzania) | Swahili (Tanzania)","sw-TZ","sw"],	
					[107,"Swahili(Kenya) | Swahili (Kenya)","sw-KE","sw"],	
					[108,"Swedish(Sweden) | Svenska (Sverige)","sv-SE","sv"],
					[109,"Tamil(India) | தமிழ் (இந்தியா)","ta-IN","ta"],	
					[110,"Tamil(Singapore) | தமிழ் (சிங்கப்பூர்)","ta-SG","ta"],	
					[111,"Tamil(Sri Lanka) | தமிழ் (இலங்கை)","ta-LK","ta"],	
					[112,"Tamil(Malaysia) | தமிழ் (மலேசியா)","ta-MY","ta"],	
					[113,"Telugu(India) | తెలుగు (భారతదేశం)","te-IN","te"],	
					[114,"Turkish(Turkey) | Türkçe (Türkiye)","tr-TR","tr"],		
					[115,"Thai(Thailand) | ไทย (ประเทศไทย)","th-TH","th"],	
					[116,"Ukrainian(Ukraine) | Українська (Україна)","uk-UA","uk"],	
					[117,"Urdu(Pakistan) | اردو (پاکستان)","ur-PK","ur"],	
					[118,"Urdu(India) | اردو (بھارت)","ur-IN","ur"],	
					[119,"Vietnamese(Vietnam) | Tiếng Việt (Việt Nam)","vi-VN","vi"],
					[120,"Zulu(South Africa) | IsiZulu (Ningizimu Afrika)","zu-ZA","zu"]]	
	
	isSelected = False
	while(isSelected is False):
		print("አማርኛ ")
		for language in language_list:
			print str(language[0]) + " " + language[1]
			# print(temp)
			# print language[0] 
			# print language[1]
		in_language_num = int(raw_input("Input Language: "))
		out_language_num = int(raw_input("Output Language: "))
		if((in_language_num > 0 and in_language_num <= 120) and (out_language_num > 0 and out_language_num <= 120)):
			isSelected = True
		else:
			print("Invalid Option, Please Try Again")
			continue
	for language in language_list:
		if(language[0]==in_language_num):
			in_language = language[2]
			print("Input Language: ",language[1])
		if(language[0]==out_language_num):
			trans_targ_code = language[3]
		if(language[0]==out_language_num):
			out_language = language[2]
			print("Output Language: ",language[1])

	return in_language,trans_targ_code,out_language

def main():
	in_language,trans_targ_code,out_language = menu()
	Record()
	speech2txt_result = Speech_to_text(in_language)
	translated_text = Translation(speech2txt_result,trans_targ_code)
	#print("(Debug)Translated text: ",translated_text)
	Text_to_speech(str(translated_text),out_language)

main()
