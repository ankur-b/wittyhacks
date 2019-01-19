from gtts import gTTS
from playsound import playsound
from io import BytesIO
my_variable = 'hello'
mp3_fp = BytesIO(b"")
tts = gTTS(my_variable, 'en')
tts.write_to_fp(mp3_fp)
playsound(mp3_fp)
