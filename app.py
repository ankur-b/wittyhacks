import os
import speech_recognition as sr
import sqlite3
import main
import cv2
import requests

from random import randrange, sample
from gtts import gTTS

#import pyttsx3

# engine = pyttsx3.init()
# engine.setProperty("voice","armenian")
# rate = engine.getProperty("rate")
# engine.setProperty("rate",rate - 30)

user = ""


with open("ID.md", "r") as f:
    idNo = f.read()
    idNo = int(idNo)+1
    f.close()

conn = sqlite3.connect("Challengers.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS challengers (Id INTEGER PRIMARY KEY, Username TEXT NOT NULL UNIQUE, Score INTEGER DEFAULT 0)")
c.close()
conn.close()

def speak(mess):
    print("Speaking")
    language = "en"
    myobj = gTTS(text=mess, lang=language, slow=False)
    myobj.save("Voice/message.mp3")
    os.system("mpg123 Voice/message.mp3")

# def speak(mess):
#     print("Speaking")
#     engine.say(mess)
#     engine.runAndWait()

def listen():
    try:
        print("Listening")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        text = r.recognize_google(audio)
        print(text)
        return text
    except:
        listen()
def register(name):
    conn = sqlite3.connect("Challengers.db")
    c = conn.cursor()
    mainloop = 0
    while mainloop == 0:
        c.execute("SELECT * FROM challengers WHERE Username = ?",(name,))
        names = c.fetchone()
        if names:
            os.system("mpg123 Voice/challengerConfirmation.mp3")
            while True:
                choice = listen()
                if choice == "yes":
                    inp = "You are back, "+ name+"!!!!!!! Good to see you again......."
                    speak(inp)
                    global user
                    user = name
                    mainloop = 1
                    break
                elif choice == "no":
                    os.system("mpg123 Voice/newName.mp3")
                    name = listen()
                    break
                else:
                    os.system("mpg123 Voice/yesOrNo.mp3")
        else:
            c.execute("INSERT INTO challengers VALUES(?,?,0)",(idNo,name,))
            conn.commit()
            user = name
            os.system("mpg123 Voice/newBoi.mp3")
            with open("ID.md", "w") as f:
                f.write(str(idNo))
                f.close()
            mainloop = 1
    c.close()
    conn.close()

def Questions(res, diff):
    score = 0
    streak = 0
    options = ["a","b","c","d"]
    os.system("mpg123 Voice/qnaIntro.mp3")
    for i in range(5):
        while True:
            speak("So, Question number "+str(i+1)+"is......"+res[i]["question"])
            optionList = res[i]["incorrect_answers"]
            optionList.insert(randrange(len(optionList)+1), res[i]["correct_answer"])
            for j in range(4):
                speak("Option number "+options[j]+" is......"+ optionList[j]+"......")
            os.system("mpg123 Voice/chooseAns.mp3")
            ans = listen()
            if ans == "repeat":
                os.system("mpg123 Voice/okay.mp3")
                continue
            if ans not in options:
                os.system("mpg123 tryAgain.mp3")
                continue
            if optionList[options.index(ans)] == res[i]["correct_answer"]:
                if diff == "easy":
                    score += (streak + 1)
                    streak += 1
                elif diff == "medium":
                    score += (streak + 3)
                    streak += 2
                else:
                    score += (streak + 5)
                    streak += 3
                os.system("mpg123 Voice/correctAns.mp3")
                break
            else:
                os.system("mpg123 Voice/incorrectAns.mp3")
                streak = 0
                break
    speak ("Your overall score in this round is "+str(score))
    conn = sqlite3.connect("Challengers.db")
    c = conn.cursor()
    global user
    c.execute("UPDATE challengers SET Score = Score + ? WHERE Username = ?", (score, user,))
    conn.commit()
    c.close()
    conn.close()
    os.system("mpg123 Voice/redirect.mp3")

img = cv2.imread("black.jpg")
cv2.namedWindow("image", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.imshow("image",img)
cv2.waitKey(0)
os.system("mpg123 Voice/welcomeMessage.mp3")
player = listen()
print (player)
while player == None:
    player = listen()
register(player)


posNew = ["new game","start a new game","start new game","start game","new","game","start the new gme"]
posLead = ["show leaderboard","ranking","my rank","leaderboard","show leaderboards","leaderboards","show my rank","my ranking","view leaderboard","view leaderboards","view ranking"
          "view my ranking","show the leaderboard"]
posCredits = ["show credits","view credits","credits"]
posLog = ["logout","exit","quit","leave","sign out","log out","log off"]
Categs = ["general knowledge","sports","mythology","politics","geography"]
i = 0
dic = {"sports":"21", "general knowledge":"9", "mythology":"20","politics":"24","geography":"22"}
diffLevels = ["easy","medium","hard"]


os.system("mpg123 Voice/mainMenu.mp3")
rep = 0
while True:
    choice = listen()
    if choice == "repeat":
        os.system("mpg123 Voice/mainMenu.mp3")
        continue
    elif choice in posLog:
        os.system("mpg123 Voice/quit.mp3")
        user = ""
        break
    elif choice in posCredits:
        os.system("mpg123 Voice/credits.mp3")
        os.system("mpg123 Voice/redirect.mp3")
    elif choice in posLead:
        conn = sqlite3.connect("Challengers.db")
        c = conn.cursor()
        c.execute("SELECT * FROM challengers ORDER BY Score DESC")
        allUsers = c.fetchall()
        print(allUsers)
        print(user)
        c.execute("SELECT * FROM challengers WHERE Username = ?",(user,))
        currUser = c.fetchone()
        print(currUser)
        pos = allUsers.index(currUser)
        speak("You are on rank " + str(pos + 1))
        os.system("mpg123 Voice/next.mp3")
    elif choice in posNew:
        os.system("mpg123 Voice/newGame.mp3")
        mov = ""
        choice = "no"
        while choice != "yes":
            mov = ""
            while mov != "Up":
                speak(Categs[i])
                mov = main.dir()
                if mov == "Left":
                    if i != 4: i += 1
                    else: i = 0
                elif mov == "Right":
                    if i != 0: i -= 1
                    else: i = 4
                #if input() == "z":
                 #   break
            speak("You have chosen "+Categs[i]+"..... Do you confirm...... Yes or no.......")
            choice = listen()
            if choice == "no":
                continue
            else:
                break
        os.system("mpg123 Voice/chooseDiff.mp3")
        choice = ""
        att = 0
        while choice not in diffLevels:
            if att > 0:
                os.system("mpg123 Voice/tryAgain.mp3")
            choice = listen()
            att += 1

        response = requests.get("https://opentdb.com/api.php?amount=5&category=" + str(dic[Categs[i]]) +"&difficulty="+choice+"&type=multiple")
        data = response.json()
        result = data["results"]
        print(result)
        Questions(result, choice)
    else:
        os.system("mpg123 Voice/notFound.mp3")
cv2.destroyAllWindows()
