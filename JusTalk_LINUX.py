# -*- coding: UTF-8 -*-
import io
import os
import time

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
# Imports the Google Cloud client library
from google.cloud import translate_v2 as translate

from tkinter import *
from tkinter import ttk
import threading
import time
import gi

from google.cloud import texttospeech
import pyaudio
import wave

from playsound import playsound

# time_list = [] #for testing performance

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/Desktop/JusTalk-d73706149e2a.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/khoa/Desktop/JusTalk-d73706149e2a.json"
# Microphone Frequency Response in Hertz
MIC_FREQ_RESP = 44100
# language list: [numerical order][English Name][Actual Name][Speech2text Language code][Translation code][Text2speech Language code]
"""
	Note: The following languages are not supported by the Neural Machine Translation (NMT) model: 
	Belarusian (be), Kyrgyz (ky), Latin (la), Maltese (mt) for Maltese to English translations only,
	Myanmar (my), and Sundanese (su). If you request one of theses translation pairs using the NMT model,
	then the Translation API defaults to the PBMT model to translate your text.
"""
language_list =[	[1,"English(United States)", 	 			   " English (United States)"		,"en-US"		,"en"	,"en-US"],
					[2,"Spanish(Mexico)", 			 			   " Español (México)"				,"es-MX"		,"es"	,"es-ES"],
					[31,"French(France)"," 			 			    Français (France)"				,"fr-FR"		,"fr"	,"fr-FR"],
					[3,"Chinese,Mandarin(Simplified)", 	   " 普通话 (中国大陆)"				,"zh"			,"zh-CN","cmn-CN"],	
					[119,"Vietnamese(Vietnam)"," 		 			    Tiếng Việt (Việt Nam)"			,"vi-VN"		,"vi"	,"vi-VN"],
					[4,"Japanese(Japan)", 			 			   " 日本語（日本）"					,"ja-JP"		,"ja"	,"ja-JP"],
					[38,"Korean(South Korea)"," 		 			    한국어 (대한민국)"					,"ko-KR"		,"ko"	,"ko-KR"],
					[33,"German(Germany)"," 			 			    Deutsch (Deutschland)"			,"de-DE"		,"de"	,"de-DE"],	
					[34,"Hindi(India)"," 				 			    हिन्दी (भारत)"						,"hi-IN"		,"hi"	,"hi-IN"],
					[42,"Portuguese(Portugal)"," 		 			    Português (Portugal)"			,"pt-PT"		,"pt"	,"pt-PT"],	
					[80,"Russian(Russia)"," 			 			    Русский (Россия)"				,"ru-RU"		,"ru"	,"ru-RU"],
					[36,"Indonesian(Indonesia)"," 		 			    Bahasa Indonesia(Indonesia)"	,"id-ID"		,"id"	,"id-ID"],	
					[37,"Italian(Italy)"," 			 			    Italiano (Italia)"				,"it-IT"		,"it"	,"it-IT"],
					[5,"Arabic(Israel)", 							   " العربية (إسرائيل)"				,"ar-IL"		,"ar"	,"ar-XA"],
					[6,"Arabic(Jordan)",				   			   " العربية (الأردن)"				,"ar-JO"		,"ar"	,"ar-XA"],	
					[7,"Arabic(United Arab Emirates)", 			   " العربية (الإمارات)"			,"ar-AE"		,"ar"	,"ar-XA"],	
					[8,"Arabic(Bahrain)", 						   " العربية (البحرين)"				,"ar-BH"		,"ar"	,"ar-XA"],	
					[9,"Arabic(Algeria)", 				   		   " العربية (الجزائر)"				,"ar-DZ"		,"ar"	,"ar-XA"],	
					[10,"Arabic(Saudi Arabia)", 					   " العربية (السعودية)"			,"ar-SA"		,"ar"	,"ar-XA"],	
					[11,"Arabic(Iraq)", 				   			   " العربية (العراق)"				,"ar-IQ"		,"ar"	,"ar-XA"],	
					[12,"Arabic(Kuwait)"," 						    العربية (الكويت)"				,"ar-KW"		,"ar"	,"ar-XA"],
					[13,"Arabic(Morocco)"," 				 		    العربية (المغرب)"				,"ar-MA"		,"ar"	,"ar-XA"],	
					[14,"Arabic(Tunisia)"," 				   		    العربية (تونس)"				,"ar-TN"		,"ar"	,"ar-XA"],	
					[15,"Arabic(Oman)"," 				   			    العربية (عُمان)"				,"ar-OM"		,"ar"	,"ar-XA"],	
					[16,"Arabic(State of Palestine)"," 			    العربية (فلسطين)"				,"ar-PS"		,"ar"	,"ar-XA"],	
					[17,"Arabic(Qatar)"," 				   			    العربية (قطر)"					,"ar-QA"		,"ar"	,"ar-XA"],	
					[18,"Arabic(Lebanon)"," 				   		    العربية (لبنان)"				,"ar-LB"		,"ar"	,"ar-XA"],	
					[19,"Arabic(Egypt)"," 				   			    العربية (مصر)"					,"ar-EG"		,"ar"	,"ar-XA"],	
					[20,"Czech(Czech Republic)"," 					    Čeština (Česká republika)"		,"cs-CZ"		,"cs"	,"cs-CZ"],	
					[21,"Chinese,Mandarin(Traditional)"," 	    國語 (台灣)"						,"zh-TW"		,"zh-TW","cmn-CN"],	
					[23,"Danish(Denmark)"," 			 			    Dansk (Danmark)"				,"da-DK"		,"da"	,"da-DK"],	
					[24,"Dutch(Netherlands)"," 		 			    Nederlands (Nederland)"		,"nl-NL"		,"nl"	,"nl-NL"],	
					[25,"English(Australia)"," 		 			    English (Australia)"			,"en-AU"		,"en"	,"en-AU"],	
					[26,"English(United Kingdom)"," 	 			    English (Great Britain)"		,"en-GB"		,"en"	,"en-GB"],	
					[27,"English(India)"," 			 			    English (India)"				,"en-IN"		,"en"	,"en-IN"],	
					[28,"Filipino(Philippines)"," 		 			    Filipino (Pilipinas)"			,"fil-PH"		,"tl"	,"fil-PH"],	
					[29,"Finnish(Finland)"," 			 			    Suomi (Suomi)"					,"fi-FI"		,"fi"	,"fi-FI"],	
					[30,"French(Canada)"," 			 			    Français (Canada)"				,"fr-CA"		,"fr"	,"fr-CA"],		
					[32,"Greek(Greece)"," 				 			    Ελληνικά (Ελλάδα)"				,"el-GR"		,"el"	,"el-GR"],		
					[35,"Hungarian(Hungary)"," 		 			    Magyar (Magyarország)"			,"hu-HU"		,"hu"	,"hu-HU"],			
					[39,"Norwegian Bokmål(Norway)"," 	 			    Norsk bokmål (Norge)"			,"nb-NO"		,"no"	,"nb-NO"],	
					[40,"Polish(Poland)"," 			 			    Polski (Polska)"				,"pl-PL"		,"pl"	,"pl-PL"],	
					[41,"Portuguese(Brazil)"," 		 			    Português (Brasil)"			,"pt-BR"		,"pt"	,"pt-BR"],	
					[81,"Spanish(Argentina)"," 		 			    Español (Argentina)"			,"es-AR"		,"es"	,"es-ES"],	
					[82,"Spanish(Bolivia)"," 			 			    Español (Bolivia)"				,"es-BO"		,"es"	,"es-ES"],	
					[83,"Spanish(Chile)"," 			 			    Español (Chile)"				,"es-CL"		,"es"	,"es-ES"],	
					[84,"Spanish(Colombia)"," 			 			    Español (Colombia)"			,"es-CO"		,"es"	,"es-ES"],	
					[85,"Spanish(Costa Rica)"," 		 			    Español (Costa Rica)"			,"es-CR"		,"es"	,"es-ES"],	
					[86,"Spanish(Ecuador)"," 			 			    Español (Ecuador)"				,"es-EC"		,"es"	,"es-ES"],
					[87,"Spanish(El Salvador)"," 		 			    Español (El Salvador)"			,"es-SV"		,"es"	,"es-ES"],	
					[88,"Spanish(Spain)"," 			 			    Español (España)"				,"es-ES"		,"es"	,"es-ES"],
					[89,"Spanish(United States)","		 			    Español (Estados Unidos)"		,"es-US"		,"es"	,"es-ES"],	
					[90,"Spanish(Guatemala)"," 		 			    Español (Guatemala)"			,"es-GT"		,"es"	,"es-ES"],	
					[91,"Spanish(Honduras)"," 			 			    Español (Honduras)"			,"es-HN"		,"es"	,"es-ES"],	
					[93,"Spanish(Nicaragua)"," 		 			    Español (Nicaragua)"			,"es-NI"		,"es"	,"es-ES"],	
					[94,"Spanish(Panama)"," 			 			    Español (Panamá)"				,"es-PA"		,"es"	,"es-ES"],	
					[95,"Spanish(Paraguay)"," 			 			    Español (Paraguay)"			,"es-PY"		,"es"	,"es-ES"],	
					[96,"Spanish(Peru)"," 				 			    Español (Perú)"				,"es-PE"		,"es"	,"es-ES"],	
					[97,"Spanish(Puerto Rico)"," 		 			    Español (Puerto Rico)"			,"es-PR"		,"es"	,"es-ES"],	
					[98,"Spanish(Dominican Republic)"," 			    Español (República Dominicana)","es-DO"		,"es"	,"es-ES"],	
					[99,"Spanish(Uruguay)"," 			 			    Español (Uruguay)"				,"es-UY"		,"es"	,"es-ES"],	
					[100,"Spanish(Venezuela)"," 		 			    Español (Venezuela)"			,"es-VE"		,"es"	,"es-ES"],		
					[103,"Slovak(Slovakia)","			 			    Slovenčina (Slovensko)"		,"sk-SK"		,"sk"	,"sk-SK"],	
					[108,"Swedish(Sweden)"," 			 			    Svenska (Sverige)"				,"sv-SE"		,"sv"	,"sv-SE"],
					[114,"Turkish(Turkey)"," 			 			    Türkçe (Türkiye)"				,"tr-TR"		,"tr"	,"tr-TR"],		
					[116,"Ukrainian(Ukraine)"," 		 			    Українська (Україна)"			,"uk-UA"		,"uk"	,"uk-UA"],	
				]	

gui_language_list = []
for line in language_list:
	gui_language_list.append(line[1])

def Speech_to_text(input_language_code):
	# Instantiates a client
	client = speech.SpeechClient()

	# The name of the audio file to transcribe
	# input_audio_file_path = os.path.join('/home','pi','Desktop',
	# 			'JusTalk','file.wav')

	# Loads the audio into memory
	with io.open(input_audio_file_path, 'rb') as audio_file:
	    content = audio_file.read()
	    audio = types.RecognitionAudio(content=content)

	config = types.RecognitionConfig(
	    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
	    sample_rate_hertz=MIC_FREQ_RESP,
	    language_code = input_language_code)

	# Detects speech in the audio file
	response = client.recognize(config, audio)

	result = None
	for result in response.results:
		print(u'Transcript: {}'.format(result.alternatives[0].transcript))
		print(u"Print out result", result)
	
	#return str(result.alternatives[0].transcript)
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

def FindIndex(input_string):
	for language in language_list:
		if language[1] == input_string:
			return language_list.index(language)

def OnRecord():
	global record
	global record_finished
	record = not record 
	if not record:
		buttontext.set("Record")
		while not record_finished:
			pass	
		string_left = leftcombo.get()
		string_right = rightcombo.get()
		in_language = language_list[FindIndex(string_left)][3]
		out_language = language_list[FindIndex(string_right)][5]
		trans_targ_code = language_list[FindIndex(string_right)][4]
		S2T_start_time = time.time()
		speech2txt_result = Speech_to_text(in_language)
		print("Speech-to-text Completed. Took {} seconds".format(time.time()-S2T_start_time))
		#time_list.append(time.time()-S2T_start_time)
		lefttext.set(str(speech2txt_result.alternatives[0].transcript))
		Transl_start_time = time.time()
		translated_text = Translation(speech2txt_result,trans_targ_code)
		print("Translation Completed. Took {} seconds".format(time.time()-Transl_start_time))
		#time_list.append(time.time()-Transl_start_time)
		righttext.set(translated_text)

		text2speech_thread = threading.Thread(target = text2speech_thread_function, args = (str(translated_text),out_language))
		text2speech_thread.daemon = True
		text2speech_thread.start()
	else:
		buttontext.set("Stop")
		record_finished = False
		recordthread = threading.Thread(target = RecordThread)
		recordthread.daemon = True
		recordthread.start()

def Swap():
	temp = leftcombo.get()
	leftcombo.set(rightcombo.get())
	rightcombo.set(temp)

def ToggleFull(event):
	global fullscreen
	fullscreen = not fullscreen
	root.attributes("-fullscreen", fullscreen)

def RecordThread():
	global record
	global record_finished

	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = MIC_FREQ_RESP
	CHUNK = 1024
	RECORD_SECONDS = 5
	WAVE_OUTPUT_FILENAME = "file.wav"
	 
	audio = pyaudio.PyAudio()
	stream = audio.open(format=FORMAT, channels=CHANNELS,
				rate=RATE, input=True,
				frames_per_buffer=CHUNK)
	
	frames = []
	print("Start Recoding...")	
	""" TIME """
	start_time = time.time()
	while record:
		# start Recording
		data = stream.read(CHUNK)
		frames.append(data)		
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
	print("Finished recording. Took {} seconds".format(time.time()-start_time))
	#time_list.append(time.time()-start_time)
	record_finished = True    

def play_output_audio():#for non-Pi use
	dir_path = 	os.getcwd()
	input_audio_file_path = os.path.join(dir_path,'output.mp3')
	playsound(input_audio_file_path)

def play_output_audio_for_pi():
	dir_path = 	os.getcwd()
	input_audio_file_path = os.path.join(dir_path,'output.mp3')
	#playsound(input_audio_file_path)
	pygame.mixer.init()
	pygame.mixer.music.load(input_audio_file_path)
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
		continue

def text2speech_thread_function(translated_text,translated_language_code):
	T2S_start_time = time.time()
	Text_to_speech(translated_text,translated_language_code)
	print("Text-to-speech completed. Took {} seconds".format(time.time()-T2S_start_time))
	#time_list.append(time.time()-T2S_start_time)
	Output_start_time = time.time()
	play_output_audio()
	#play_output_audio_for_pi()
	print("Output audio played. Took {} seconds".format(time.time()-Output_start_time))
	#time_list.append(time.time()-Output_start_time)
	#print(time_list)

dir_path = 	os.getcwd()
input_audio_file_path = os.path.join(dir_path,'file.wav')
#GUI setup 
root = Tk()
root.title("JusTalk")
record_finished = False
root.minsize(650,150)

#not fullscreen by default
fullscreen = False
root.bind("<Escape>",ToggleFull)

frame = Frame(root)
frame.pack(side = TOP)
bottomframe = Frame(root)
bottomframe.pack(side = BOTTOM)

# exitbutton = Button(frame,text = "Quit",command = quit)
# exitbutton.grid(row=3,column=1)
in_language = 0
out_language = 0

record = False
buttontext = StringVar()
record_button_img = PhotoImage(file = "mic.png").subsample(20,20)
buttontext.set("Record")
recordbutton = Button(frame,image=record_button_img,compound=LEFT,font=("bold"),textvariable=buttontext,command=OnRecord)
recordbutton.grid(row=2,column=1,pady=10)

leftcombo = ttk.Combobox(frame,values=gui_language_list)
leftcombo.current(0)
leftcombo.grid(column=0,row=0,pady=10,padx=10)
lefttext = StringVar()
lefttext.set("")
leftlabel = Label(frame,textvariable=lefttext,width=30,wraplength=150)
leftlabel.grid(column=0,row=1)

swap_button_img = PhotoImage(file="swap.png").subsample(10,9)
swapbutton = Button(frame,image=swap_button_img,text="",command=Swap)
swapbutton.grid(column=1,row=0,pady=10)

rightcombo = ttk.Combobox(frame,values=gui_language_list)
rightcombo.current(0)
rightcombo.grid(column=2,row=0,pady=10,padx=10)
righttext = StringVar()
righttext.set("")
rightlabel = Label(frame,textvariable=righttext,width=30,wraplength=150)
rightlabel.grid(column=2, row=1)

root.mainloop()
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