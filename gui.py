# -*- coding: UTF-8 -*-
import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
# Imports the Google Cloud client library
from google.cloud import translate

print("testing")

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
	# file_name = os.path.join('/home','pi','Desktop',
	# 			'JusTalk','file.wav')
	file_name = os.path.join('/Users','khoatran','Desktop',
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
	# language list: [numerical order][English Name|Actual Name][Speech2text Language code][Translation code]
	"""
		Note: The following languages are not supported by the Neural Machine Translation (NMT) model: 
		Belarusian (be), Kyrgyz (ky), Latin (la), Maltese (mt) for Maltese to English translations only,
		Myanmar (my), and Sundanese (su). If you request one of theses translation pairs using the NMT model,
		then the Translation API defaults to the PBMT model to translate your text.
	"""
	language_list =[[1,"Afrikaans(South Africa) 				   | Afrikaans(Suid-Afrika)"		,"af-ZA"		,"af"	,None],	
					[2,"Amharic(Ethiopia)አማርኛ 					   | (ኢትዮጵያ)"						,"am-ET"		,"am"	,None],	
					[3,"Armenian(Armenia)Հայ 					   | (Հայաստան)"					,"hy-AM"		,"hy"	,None],	
					[4,"Azerbaijani(Azerbaijan) 				   | Azərbaycan(Azərbaycan)"		,"az-AZ"		,"az"	,None],
					[5,"Arabic(Israel) 							   | العربية (إسرائيل)"				,"ar-IL"		,"ar"	,"ar-XA"],
					[6,"Arabic(Jordan) 				   			   | العربية (الأردن)"				,"ar-JO"		,"ar"	,"ar-XA"],	
					[7,"Arabic(United Arab Emirates) 			   | العربية (الإمارات)"			,"ar-AE"		,"ar"	,"ar-XA"],	
					[8,"Arabic(Bahrain) 						   | العربية (البحرين)"				,"ar-BH"		,"ar"	,"ar-XA"],	
					[9,"Arabic(Algeria) 				   		   | العربية (الجزائر)"				,"ar-DZ"		,"ar"	,"ar-XA"],	
					[10,"Arabic(Saudi Arabia) 					   | العربية (السعودية)"			,"ar-SA"		,"ar"	,"ar-XA"],	
					[11,"Arabic(Iraq) 				   			   | العربية (العراق)"				,"ar-IQ"		,"ar"	,"ar-XA"],	
					[12,"Arabic(Kuwait) 						   | العربية (الكويت)"				,"ar-KW"		,"ar"	,"ar-XA"],
					[13,"Arabic(Morocco) 				 		   | العربية (المغرب)"				,"ar-MA"		,"ar"	,"ar-XA"],	
					[14,"Arabic(Tunisia) 				   		   | العربية (تونس)"				,"ar-TN"		,"ar"	,"ar-XA"],	
					[15,"Arabic(Oman) 				   			   | العربية (عُمان)"				,"ar-OM"		,"ar"	,"ar-XA"],	
					[16,"Arabic(State of Palestine) 			   | العربية (فلسطين)"				,"ar-PS"		,"ar"	,"ar-XA"],	
					[17,"Arabic(Qatar) 				   			   | العربية (قطر)"					,"ar-QA"		,"ar"	,"ar-XA"],	
					[18,"Arabic(Lebanon) 				   		   | العربية (لبنان)"				,"ar-LB"		,"ar"	,"ar-XA"],	
					[19,"Arabic(Egypt) 				   			   | العربية (مصر)"					,"ar-EG"		,"ar"	,"ar-XA"],	
					[20,"Bengali(Bangladesh) 				   	   | বাংলা (বাংলাদেশ)"					,"bn-BD"		,"bn"	,None],	
					[21,"Bengali(India) 				   		   | বাংলা (ভারত)"					,"bn-IN"		,"bn"	,None],	
					[22,"Basque(Spain) 				   			   | Euskara (Espainia)"			,"eu-ES"		,"eu"	,None],	
					[23,"Bulgarian(Bulgaria) 					   | Български (България)"			,"bg-BG"		,"bg"	,None],
					[24,"Croatian(Croatia) 						   | Hrvatski (Hrvatska)"			,"hr-HR"		,"hr"	,None],	
					[25,"Catalan(Spain) 						   | Català (Espanya)"				,"ca-ES"		,"ca"	,None],	
					[26,"Czech(Czech Republic) 					   | Čeština (Česká republika)"		,"cs-CZ"		,"cs"	,"cs-CZ"],	
					[27,"Chinese,Mandarin(Traditional, Taiwan) 	   | 國語 (台灣)"						,"zh-TW"		,"zh-TW","cmn-CN"],	
					[28,"Chinese,Cantonese(Traditional, Hong Kong) | 廣東話 (香港)"					,"yue-Hant-HK"	,"zh"	,None],	
					[29,"Chinese,Mandarin(Simplified, Hong Kong)   | 普通話 (香港)"					,"zh-HK"		,"zh"	,"cmn-CN"], #zh OR zh-CN(for translation)
					[30,"Chinese,Mandarin(Simplified, China) 	   | 普通话 (中国大陆)"				,"zh"			,"zh-CN","cmn-CN"],	
					[31,"Danish(Denmark) 			 			   | Dansk (Danmark)"				,"da-DK"		,"da"	,"da-DK"],	
					[32,"Dutch(Netherlands) 		 			   | Nederlands (Nederland)"		,"nl-NL"		,"nl"	,"nl-NL"],	
					[33,"English(Australia) 		 			   | English (Australia)"			,"en-AU"		,"en"	,"en-AU"],	
					[34,"English(Canada) 			 			   | English (Canada)"				,"en-CA"		,"en"	,None],	
					[35,"English(Ghana) 			 			   | English (Ghana)"				,"en-GH"		,"en"	,None],	
					[36,"English(United Kingdom) 	 			   | English (Great Britain)"		,"en-GB"		,"en"	,"en-GB"],	
					[37,"English(India) 			 			   | English (India)"				,"en-IN"		,"en"	,"en-IN"],	
					[38,"English(Ireland) 			 			   | English (Ireland)"				,"en-IE"		,"en"	,None],	
					[39,"English(Kenya) 			 			   | English (Kenya)"				,"en-KE"		,"en"	,None],	
					[40,"English(New Zealand) 		 			   | English (New Zealand)"			,"en-NZ"		,"en"	,None],	
					[41,"English(Nigeria) 			 			   | English (Nigeria)"				,"en-NG"		,"en"	,None],	
					[42,"English(Philippines) 		 			   | English (Philippines)"			,"en-PH"		,"en"	,None],	
					[43,"English(Singapore) 		 			   | English (Singapore)"			,"en-SG"		,"en"	,None],	
					[44,"English(South Africa) 		 			   | English (South Africa)"		,"en-ZA"		,"en"	,None],	
					[45,"English(Tanzania) 			 			   | English (Tanzania)"			,"en-TZ"		,"en"	,None],	
					[46,"English(United States) 	 			   | English (United States)"		,"en-US"		,"en"	,"en-US"],	
					[47,"Filipino(Philippines) 		 			   | Filipino (Pilipinas)"			,"fil-PH"		,"tl"	,"fil-PH"],	
					[48,"Finnish(Finland) 			 			   | Suomi (Suomi)"					,"fi-FI"		,"fi"	,"fi-FI"],	
					[49,"French(Canada) 			 			   | Français (Canada)"				,"fr-CA"		,"fr"	,"fr-CA"],	
					[50,"French(France) 			 			   | Français (France)"				,"fr-FR"		,"fr"	,"fr-FR"],	
					[51,"Greek(Greece) 				 			   | Ελληνικά (Ελλάδα)"				,"el-GR"		,"el"	,"el-GR"],	
					[52,"Galician(Spain) 			 			   | Galego (España)"				,"gl-ES"		,"gl"	,None],	
					[53,"Georgian(Georgia) 			 			   | ქართული (საქართველო)"			,"ka-GE"		,"ka"	,None],	
					[54,"Gujarati(India) 			 			   | ગુજરાતી (ભારત)"					,"gu-IN"		,"gu"	,None],	
					[55,"German(Germany) 			 			   | Deutsch (Deutschland)"			,"de-DE"		,"de"	,"de-DE"],	
					[56,"Hebrew(Israel) 			 			   | עברית (ישראל)"					,"he-IL"		,"he"	,None],	#he or iw(for translation)
					[57,"Hindi(India) 				 			   | हिन्दी (भारत)"						,"hi-IN"		,"hi"	,"hi-IN"],	
					[58,"Hungarian(Hungary) 		 			   | Magyar (Magyarország)"			,"hu-HU"		,"hu"	,"hu-HU"],	
					[59,"Indonesian(Indonesia) 		 			   | Bahasa Indonesia(Indonesia)"	,"id-ID"		,"id"	,"id-ID"],	
					[60,"Icelandic(Iceland) 		 			   | Íslenska (Ísland)"				,"is-IS"		,"is"	,None],	
					[61,"Italian(Italy) 			 			   | Italiano (Italia)"				,"it-IT"		,"it"	,"it-IT"],	
					[62,"Javanese(Indonesia) 		 			   | Jawa (Indonesia)"				,"jv-ID"		,"jw"	,None],	
					[63,"Japanese(Japan) 			 			   | 日本語（日本）"					,"ja-JP"		,"ja"	,"ja-JP"],
					[64,"Korean(South Korea) 		 			   | 한국어 (대한민국)"					,"ko-KR"		,"ko"	,"ko-KR"],	
					[65,"Kannada(India) 			 			   | ಕನ್ನಡ (ಭಾರತ)"					,"kn-IN"		,"kn"	,None],	
					[66,"Khmer(Cambodia) 			 			   | ភាសាខ្មែរ (កម្ពុជា)"				,"km-KH"		,"km"	,None],	
					[67,"Lao(Laos) 					 			   | ລາວ (ລາວ)"						,"lo-LA"		,"lo"	,None],
					[68,"Latvian(Latvia) 			 			   | Latviešu (latviešu)"			,"lv-LV"		,"lv"	,None],	
					[69,"Lithuanian(Lithuania) 		 			   | Lietuvių (Lietuva)"			,"lt-LT"		,"lt"	,None],	
					[70,"Malay(Malaysia) 			 			   | Bahasa Melayu (Malaysia)"		,"ms-MY"		,"ms"	,None],	
					[71,"Malayalam(India) 			 			   | മലയാളം (ഇന്ത്യ)"				,"ml-IN"		,"ml"	,None],	
					[72,"Marathi(India) 			 			   | मराठी (भारत)"						,"mr-IN"		,"mr"	,None],	
					[73,"Nepali(Nepal) 				 			   | नेपाली (नेपाल)"					,"ne-NP"		,"ne"	,None],	
					[74,"Norwegian Bokmål(Norway) 	 			   | Norsk bokmål (Norge)"			,"nb-NO"		,"no"	,"nb-NO"],	
					[75,"Persian(Iran) 				 			   | فارسی (ایران)"					,"fa-IR"		,"fa"	,None],	
					[76,"Polish(Poland) 			 			   | Polski (Polska)"				,"pl-PL"		,"pl"	,"pl-PL"],	
					[77,"Portuguese(Brazil) 		 			   | Português (Brasil)"			,"pt-BR"		,"pt"	,"pt-BR"],	
					[78,"Portuguese(Portugal) 		 			   | Português (Portugal)"			,"pt-PT"		,"pt"	,"pt-PT"],	
					[79,"Romanian(Romania) 			 			   | Română (România)"				,"ro-RO"		,"ro"	,None],				
					[80,"Russian(Russia) 			 			   | Русский (Россия)"				,"ru-RU"		,"ru"	,"ru-RU"],
					[81,"Spanish(Argentina) 		 			   | Español (Argentina)"			,"es-AR"		,"es"	,"es-ES"],	
					[82,"Spanish(Bolivia) 			 			   | Español (Bolivia)"				,"es-BO"		,"es"	,"es-ES"],	
					[83,"Spanish(Chile) 			 			   | Español (Chile)"				,"es-CL"		,"es"	,"es-ES"],	
					[84,"Spanish(Colombia 			 			   | Español (Colombia)"			,"es-CO"		,"es"	,"es-ES"],	
					[85,"Spanish(Costa Rica) 		 			   | Español (Costa Rica)"			,"es-CR"		,"es"	,"es-ES"],	
					[86,"Spanish(Ecuador) 			 			   | Español (Ecuador)"				,"es-EC"		,"es"	,"es-ES"],
					[87,"Spanish(El Salvador) 		 			   | Español (El Salvador)"			,"es-SV"		,"es"	,"es-ES"],	
					[88,"Spanish(Spain) 			 			   | Español (España)"				,"es-ES"		,"es"	,"es-ES"],
					[89,"Spanish(United States)		 			   | Español (Estados Unidos)"		,"es-US"		,"es"	,"es-ES"],	
					[90,"Spanish(Guatemala) 		 			   | Español (Guatemala)"			,"es-GT"		,"es"	,"es-ES"],	
					[91,"Spanish(Honduras) 			 			   | Español (Honduras)"			,"es-HN"		,"es"	,"es-ES"],	
					[92,"Spanish(Mexico) 			 			   | Español (México)"				,"es-MX"		,"es"	,"es-ES"],	
					[93,"Spanish(Nicaragua) 		 			   | Español (Nicaragua)"			,"es-NI"		,"es"	,"es-ES"],	
					[94,"Spanish(Panama) 			 			   | Español (Panamá)"				,"es-PA"		,"es"	,"es-ES"],	
					[95,"Spanish(Paraguay) 			 			   | Español (Paraguay)"			,"es-PY"		,"es"	,"es-ES"],	
					[96,"Spanish(Peru) 				 			   | Español (Perú)"				,"es-PE"		,"es"	,"es-ES"],	
					[97,"Spanish(Puerto Rico) 		 			   | Español (Puerto Rico)"			,"es-PR"		,"es"	,"es-ES"],	
					[98,"Spanish(Dominican Republic) 			   | Español (República Dominicana)","es-DO"		,"es"	,"es-ES"],	
					[99,"Spanish(Uruguay) 			 			   | Español (Uruguay)"				,"es-UY"		,"es"	,"es-ES"],	
					[100,"Spanish(Venezuela) 		 			   | Español (Venezuela)"			,"es-VE"		,"es"	,"es-ES"],		
					[101,"Serbian(Serbia) 			 			   | Српски (Србија)"				,"sr-RS"		,"sr"	,None],
					[102,"Sinhala(Sri Lanka) 		 			   | සිංහල (ශ්රී ලංකාව)"				,"si-LK"		,"si"	,None],	
					[103,"Slovak(Slovakia)			 			   | Slovenčina (Slovensko)"		,"sk-SK"		,"sk"	,"sk-SK"],	
					[104,"Slovenian(Slovenia) 		 			   | Slovenščina (Slovenija)"		,"sl-SI"		,"sl"	,None],	
					[105,"Sundanese(Indonesia) 		 			   | Urang (Indonesia)"				,"su-ID"		,"su"	,None],	
					[106,"Swahili(Tanzania) 		 			   | Swahili (Tanzania)"			,"sw-TZ"		,"sw"	,None],	
					[107,"Swahili(Kenya) 			 			   | Swahili (Kenya)"				,"sw-KE"		,"sw"	,None],	
					[108,"Swedish(Sweden) 			 			   | Svenska (Sverige)"				,"sv-SE"		,"sv"	,"sv-SE"],
					[109,"Tamil(India) 				 			   | தமிழ் (இந்தியா)"					,"ta-IN"		,"ta"	,None],	
					[110,"Tamil(Singapore) 			 			   | தமிழ் (சிங்கப்பூர்)"					,"ta-SG"		,"ta"	,None],	
					[111,"Tamil(Sri Lanka) 			 			   | தமிழ் (இலங்கை)"					,"ta-LK"		,"ta"	,None],	
					[112,"Tamil(Malaysia) 			 			   | தமிழ் (மலேசியா)"					,"ta-MY"		,"ta"	,None],	
					[113,"Telugu(India) 			 			   | తెలుగు (భారతదేశం)"				,"te-IN"		,"te"	,None],	
					[114,"Turkish(Turkey) 			 			   | Türkçe (Türkiye)"				,"tr-TR"		,"tr"	,"tr-TR"],		
					[115,"Thai(Thailand) 			 			   | ไทย (ประเทศไทย)"				,"th-TH"		,"th"	,None],	
					[116,"Ukrainian(Ukraine) 		 			   | Українська (Україна)"			,"uk-UA"		,"uk"	,"uk-UA"],	
					[117,"Urdu(Pakistan) 			 			   | اردو (پاکستان)"				,"ur-PK"		,"ur"	,None],	
					[118,"Urdu(India) 				 			   | اردو (بھارت)"					,"ur-IN"		,"ur"	,None],	
					[119,"Vietnamese(Vietnam) 		 			   | Tiếng Việt (Việt Nam)"			,"vi-VN"		,"vi"	,"vi-VN"],
					[120,"Zulu(South Africa) 		 			   | IsiZulu (Ningizimu Afrika)"	,"zu-ZA"		,"zu"	,None]]	
	"""
		Languages that don't have Speech-to-text
			Albanian	sq
			Belarusian	be
			Bosnian	bs
			Cebuano	ceb (ISO-639-2)
			Corsican	co
			Esperanto	eo
			Estonian	et
			Frisian	fy
			Haitian Creole	ht
			Hausa	ha
			Hawaiian	haw (ISO-639-2)
			Hmong	hmn (ISO-639-2)
			Igbo	ig
			Irish	ga
			Kazakh	kk
			Kurdish	ku
			Kyrgyz	ky
			Latin	la
			Luxembourgish	lb
			Macedonian	mk
			Malagasy	mg
			Maltese	mt
			Maori	mi
			Mongolian	mn
			Myanmar (Burmese)	my
			Nyanja (Chichewa)	ny
			Pashto	ps
			Punjabi	pa
			Samoan	sm
			Scots Gaelic	gd
			Sesotho	st
			Shona	sn
			Sindhi	sd
			Somali	so
			Tajik	tg
			Uzbek	uz
			Welsh	cy
			Xhosa	xh
			Yiddish	yi
			Yoruba	yo
	"""
	isSelected = False
	while(isSelected is False):
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
			out_language = language[4]
			print("Output Language: ",language[1])

	return in_language,trans_targ_code,out_language

def main():
	in_language,trans_targ_code,out_language = menu()
	Record()
	speech2txt_result = Speech_to_text(in_language)
	translated_text = Translation(speech2txt_result,trans_targ_code)
	#print("(Debug)Translated text: ",translated_text)
	if(out_language != None):
		Text_to_speech(str(translated_text),out_language)
	else:
		print("Text to Speech not available for this language")

if __name__ == "main":
	main()
