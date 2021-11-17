import os
import pandas as pd #  pip install numpy==1.19.3
from google.cloud import texttospeech # outdated or incomplete comparing to v1
from google.cloud import texttospeech_v1

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"txt-spch-secrets.json"
# Instantiates a client
client = texttospeech_v1.TextToSpeechClient()

voice_list = []
for voice in client.list_voices().voices:
    voice_list.append([voice.name, voice.language_codes[0], voice.ssml_gender, voice.natural_sample_rate_hertz])
df_voice_list = pd.DataFrame(voice_list, columns=['name', 'language code', 'ssml gender', 'hertz rate']).to_csv('Voice List.csv', index=False)
print(client.list_voices().voices)
# Set the text input to be synthesized
quote = 'The habit of saving is itself an education; it fosters every virtue, teaches self-denial, cultivates the sense of order, trains to forethought, and so broadens the mind. By T.T.Munger'
synthesis_input = texttospeech_v1.SynthesisInput(text=quote)

voices=client.list_voices().voices

voice = texttospeech_v1.VoiceSelectionParams(
    name = "en-US-Standard-F",language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.MALE
)
# voices.append(voice)
# voice = texttospeech_v1.VoiceSelectionParams(
#     name='ar-XA-Wavenet-B', language_code="en-GB"
#     # name='vi-VN-Wavenet-D', language_code="vi-VN"
# )
# voices.append(voice)

# Select the type of audio file you want returned
audio_config = texttospeech_v1.AudioConfig(
    # https://cloud.google.com/text-to-speech/docs/reference/rpc/google.cloud.texttospeech.v1#audioencoding
    audio_encoding=texttospeech_v1.AudioEncoding.MP3
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
count=1
quote = 'The habit of saving is itself an education; it fosters every virtue'
responses=[]
filename="voices.mp3"
# for v in voices:
# q="Voice number "+str(count)+quote
# params =texttospeech_v1.VoiceSelectionParams(name=v.name, language_code=v.language_codes[0], ssml_gender=v.ssml_gender)
synthesis_input = texttospeech_v1.SynthesisInput(text=quote)
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)
# responses.append(response)
    # The response's audio_content is binary.
count+=1

with open(r"voices.mp3", "wb") as out:
    # Write the response to the output file.
    # for r in responses:
    out.write(response.audio_content)
    print('Audio content added to file ',"new.mp3")