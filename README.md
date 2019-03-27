# JusTalk

### Wenhao Tan, Amrit Thapa, Khoa Tran, Long Vu
1. Abstract: https://docs.google.com/presentation/d/1231-SMrZi-ZwCWly-Zq6qjbRMwKIVmCrPr9n3Y4eBB4/edit?usp=sharing
2. Mid-Semester Update: https://docs.google.com/presentation/d/1MJ8uhqp4fPv2BBnxLeWKV0CXuA7NlqNdYIj64fqnrK4/edit?usp=sharing

<br/>

(Prereq)Install the following:
-----------------
<br/>
```
python 2.7
pip
virtualenv
Google Speech-to-Text client library: pip install --upgrade google-cloud-speech
Google Translate client library: pip install --upgrade google-cloud-translate
Google Text-to-Speech client library: pip install --upgrade google-cloud-texttospeech (not yet implemented)
```
<br/>
<br/>

Running the app
-----------------
To verify service account key
<br/>
For Mac
`export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"`
For Windows with PowerShell
`$env:GOOGLE_APPLICATION_CREDENTIALS="[PATH]]"`
For Windows with Command Prompt
`set GOOGLE_APPLICATION_CREDENTIALS=[PATH]`
i.e: PATH = C:\Users\username\Downloads\[FILE_NAME].json

<br/>
<br/>