# JusTalk

### Wenhao Tan, Amrit Thapa, Khoa Tran, Long Vu
1. Abstract: https://docs.google.com/presentation/d/1231-SMrZi-ZwCWly-Zq6qjbRMwKIVmCrPr9n3Y4eBB4/edit?usp=sharing
2. Mid-Semester Update: https://docs.google.com/presentation/d/1MJ8uhqp4fPv2BBnxLeWKV0CXuA7NlqNdYIj64fqnrK4/edit?usp=sharing

<br/>

(Prereq)Install the following:
-----------------
<br/>
python 2.7<br/>
pip<br/>
virtualenv<br/>
Google Speech-to-Text client library: `pip install --upgrade google-cloud-speech`<br/>
Google Translate client library: `pip install --upgrade google-cloud-translate`<br/>
Google Text-to-Speech client library: `pip install --upgrade google-cloud-texttospeech` (not yet implemented)<br/>
<br/>
<br/>

Running the app
-----------------
To verify service account key
<br/>
For Mac<br/>
`export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"`<br/>
For Windows with PowerShell<br/>
`$env:GOOGLE_APPLICATION_CREDENTIALS="[PATH]]"`<br/>
For Windows with Command Prompt<br/>
`set GOOGLE_APPLICATION_CREDENTIALS=[PATH]`<br/>
i.e: PATH = C:\Users\username\Downloads\[FILE_NAME].json

<br/>
<br/>