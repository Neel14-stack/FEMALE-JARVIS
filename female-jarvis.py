import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import psutil
import pyjokes
import os
import pyautogui
import random
import wolframalpha
import json
import requests
from urllib.request import urlopen
import time


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
wolframalpha_app_id = 'WP95H3-XG95L64J93'

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time_():
    Time = datetime.datetime.now().strftime("%I:%M:%S") #For 12 hour clock
    print(Time)
    speak("The Current Time is")
    speak(Time)

def date_():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    print(datetime.date.today())
    speak("Today's date is")
    speak(day)
    speak(month)
    speak(year)

def wishme():  

    #Greetings
    hour = datetime.datetime.now().hour

    if hour>=6 and hour<12:
        speak("Good morning Neel")
    elif hour>=12 and hour<18:
        speak("Good Afternoon Neel")
    elif hour>=18 and hour<24:
        speak("Good evening Neel")
    else:
        speak("Good Night Neel")
    
    speak("Welcome back")
    #time_()
    #date_()    
    speak("Jarvis at your sevice. Please tell me how can I help you today!")

def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        print("Recognizing.....")
        query = r.recognize_google(audio,language = "en-US")
        print(query)

    except Exception as e:
        print(e)
        print("Say that again please.....")
        return "None"
    return query

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    #for this function, we must enable low security in our gmail.

    server.login('username@gmail.com','password')
    server.sendmail('username@gail.com',to,content)
    server.close()

def cpu():
    usage = str(psutil.cpu_percent())
    speak('CPU is at'+usage)
    battery = psutil.sensors_battery()
    speak('Battery is at')
    speak(battery.percent)

def joke():
    speak(pyjokes.get_joke())

def screenshot():
    img = pyautogui.screenshot()
    img.save('C:/Users/NMR/Pictures/Jarvis_SS/screenshot.png')





if __name__ == "__main__":

    print("JARVIS AT YOUR SERVICE.......")
    print(datetime.datetime.now())
    wishme()

    while True:
        query = TakeCommand().lower()

        """
        All command will be stored in lower case in query
        for easy recognition
        """

        if 'time' in query: #tell us about time
            time_()

        elif 'date' in query: #tell us about date
            date_()

        elif 'how are you' in query:
            speak('I am Fine, How are you.')
            ans = TakeCommand().lower()
            if 'fine' in ans:
                speak('Glad to here it')
            elif 'not' in ans:
                speak('feel sorry to hear it')
            
        elif 'wikipedia' in query:
            speak("Searching.....")
            query = query.replace('wikipedia', '')
            result = wikipedia.summary(query,sentences = 3)
            speak('According to Wikipedia')
            print(result)
            speak(result)
        
        elif 'send email' in query:
            try:
                speak("What should I say ?")
                content = TakeCommand()
                #provide receiver mail

                speak("Who is the Receiver?")
                reciever = input(("Enter the Receiver Email ID: "))
                to = reciever
                sendEmail(to, content)
                speak(content)
                speak("Email has been sent.")

            except Exception as e:
                print(e)
                speak("Unable to send Email")
            
        elif 'search in chrome' in query:
            speak("What should I search?")
            chromepath = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            search = TakeCommand().lower()
            wb.get(chromepath).open_new_tab(search+'.com') #only the website with .com will open

        elif 'search youtube' in query:
            speak('What should I serach in Youtube?')
            search_term = TakeCommand().lower()
            speak('Here we go to YOUTUBE!')
            wb.open('https://www.youtube.com/results?search_query='+search_term)

        elif 'search google' in query:
            speak('What should I search?')
            search_term = TakeCommand().lower()
            speak('Searching...')
            wb.open('https://www.google.com/search?q='+search_term)
        
        elif 'cpu' in query:
            cpu()
        
        elif 'joke' in query:
            joke()

        elif 'go offline' in query:
            speak('Going Offline Sir!')
            quit()

        elif 'open' in query:
            speak('Opening please wait...')
            fxn = r'D:/Movies\WEBSERIES/fairy tail'
            os.startfile(fxn)

        elif 'write a note' in query:
            speak('What should I write, Sir!')
            notes = TakeCommand()
            file = open('notes.txt','w')
            speak('Sir should I include Date and Time also?')
            ans = TakeCommand()
            if 'yes' in ans or 'sure' in ans:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(':-')
                file.write(notes)
                speak('Done Taking Notes, Sir!')
            else:
                file.write(notes)

        elif 'show notes' in query:
            speak('Showing Notes')
            file = open('notes.txt','r')
            print(file.read())
            speak(file.read())
            
        elif 'screenshot' in query:
            screenshot()

        elif 'play music' in query:
            song_dir = 'C:/Users/NMR/Music/music'
            music = os.listdir(song_dir)
            speak('What should I play?')
            ans = TakeCommand().lower()
            no = int(ans.replace('number', ''))
            os.startfile(os.path.join(song_dir,music[no]))

        elif 'remember that' in query:
            speak('What should I remember?')
            memory = TakeCommand()
            speak('You asked me to remember that'+memory)
            remember = open('memory.txt','w')
            remember.write(memory)
            remember.close()

        elif 'do you remember anything' in query:
            remember = open('memory.txt','r')
            speak('You asked me to remember that'+remember.read())

        elif 'where is' in query:
            query = query.replace('where is', '')
            location = query
            speak('User asked to locate'+location)
            wb.open_new_tab('https://www.google.com/maps/place/'+location)

        elif 'news' in query:
            try:
                jsonobj = urlopen("https://newsapi.org/v2/everything?q=tesla&from=2021-05-22&sortBy=publishedAt&apiKey=8b520920c0a64d1b9bab9aee04ca6227")        
                data = json.load(jsonobj)
                i = 1

                speak("Here are some top headlines from the Tesla Company")
                print("===========TOP HEADLINES==========="+"\n")
                for item in data['articles']:
                    print(str(i)+'. '+item['title']+'\n')
                    print(item['description']+'\n')
                    speak(item['title'])
                    i +=1
                
            except Exception as e:
                print(str(e))

        elif 'calculate' in query:
            client = wolframalpha.Client(wolframalpha_app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx +1:]
            res= client.query(''.join(query))
            answer= next(res.results).text
            print('The Answer is : '+answer)
            speak('The Answer is '+answer)

        elif 'what is ' in query or 'who is ' in query:
            speak('Please wait Sir Let me check...')
            client = wolframalpha.Client(wolframalpha_app_id)
            res = client.query(query)
            res = client.query(query)            

            try:
                print(next(res.results).text)
                speak(next(res.results).text)
            except StopIteration:
                print('No Results')

        elif 'stop listening' in query:
            speak('For how much time you want me to stop listening to your commands?')
            ans = int(TakeCommand())
            time.sleep(ans)
            print(ans)

        elif 'log out' in query:
            os.system("shutdown -l")
        elif 'restart' in query:
            os.system("shutdown /r /t l")           
        elif 'shutdown' in query:
            os.system("shutdown /s /t l")
