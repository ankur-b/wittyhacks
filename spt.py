from gtts import gTTS
import os



mess = """Now choose your difficulty,,,...
Easy, where each correct answer gives you one point.......
          Medium, where each correct answer gives you three points.........
          and Hard, where each correct answer gives you five points.........
          Give correct answers in a row and get on a red hot streak to beat your friends and score more points......."""
language = 'en'
myobj = gTTS(text=mess, lang=language, slow=False)
myobj.save("Voice/chooseDiff.mp3")
# myobj1 = gTTS(text=mess1,lang=language,slow=False)
# myobj1.save("message1.mp3")
os.system("mpg123 Voice/chooseDiff.mp3")
#os.system("mpg123 message1.mp3")
