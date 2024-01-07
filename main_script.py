# importing speech recognition package from google api
import speech_recognition as sr
import playsound  # to play saved mp3 file
from gtts import gTTS  # google text to speech
import os  # to save/open files
#import wolframalpha  # to calculate strings into formula
from selenium import webdriver  # to control browser operations
import webbrowser
from datetime import date, timedelta

from palmDup import talk_to_palm
from spotifyDup import play_song
from eventDup import add_event
from taskDup import add_task
num = 1

def assistant_speaks(output):
    global num

    # num to rename every audio file
    # with different name to remove ambiguity
    num += 1
    print("PerSon : ", output)

    toSpeak = gTTS(text=output, lang='en', slow=False)
    # saving the audio file given by google text to speech
    file = str(num)+".mp3"
    toSpeak.save(file)

    # playsound package is used to play the same file.
    playsound.playsound(file, True)
    os.remove(file)


def get_audio():

    rObject = sr.Recognizer()
    audio = ''

    with sr.Microphone() as source:
        print("Speak...")

        # recording the audio using speech recognition
        audio = rObject.listen(source, phrase_time_limit=5)
    print("Stop.")  # limit 5 secs

    try:

        text = rObject.recognize_google(audio, language='en-US')
        print("You : ", text)
        return text

    except:

        assistant_speaks("Could not understand your audio, PLease try again !")
        return 0

def process(operator, text):
    try:
        operation_and_data = operator.split('$')
        #print(operation_and_data)
        if  "playing music" in operation_and_data[0]:
            try:
                play_song(operation_and_data[1])
                assistant_speaks("Song is playing")
            except:
                assistant_speaks("Please try again")
        elif "prompting palm" in operation_and_data[0]:
            try:
                res = talk_to_palm(operation_and_data[1])

                if(res == None):
                    assistant_speaks("Please try again")
                else:
                    if(len(res) < 300):
                        assistant_speaks(res)
                    else:
                        assistant_speaks("Your result is ready")
                
            except:
                assistant_speaks("Please try again")
        elif "event" in operation_and_data[0]:
            try:
                data = operation_and_data[1].split('?')
                #(operation_and_data[1])
                add_event(data)
                assistant_speaks("Your event is added to your calendar")
            except:
                assistant_speaks("Please try again")
        elif "play video" in operation_and_data[0]:
            """ driver = webdriver.Chrome()
            driver.implicitly_wait(1)
            driver.maximize_window()
            data = operation_and_data[1].split()
            video_name = '+'.join(data)
            driver.get(
                "https://www.youtube.com/results?search_query=" + video_name) """
            try:
                data = operation_and_data[1].split()
                video_name = '+'.join(data)
                url = "https://www.youtube.com/results?search_query=" + video_name
                webbrowser.open_new_tab(url)
            except:
                assistant_speaks("Please try again")  

        elif  "task"in operation_and_data[0]:
            try:
                data = operation_and_data[1].split('?')
                add_task(data)
                assistant_speaks("Your task is added to your calendar")
            except:
                assistant_speaks("Please try again")   
        else:
            assistant_speaks("Please elaborate. Your command is unclear") 
    except:
        try:
            res = talk_to_palm("about" + text)
            if res != None:
                if(len(res) < 350):
                    assistant_speaks(res)
                    print(res)
                else:
                    print(res)
                    assistant_speaks("Result is ready")
        except:
            assistant_speaks("Please try again")

def get_operation(input):
    query = """
    Classify the following prompts into playing music, adding event to calendar,  adding task to calendar, prompting Palm, play video. Give output in the form of 'operation-name'. 
Examples-
input: "What is abcd" output: "prompting palm$what is abcd"
input:"Write xyz about abc" output:"prompting palm$write xyz about abc"
input: "play thunder song by imagine dragons" output: "playing music$thunder imagine dragons"
input: "I want to listen to believer" output: "playing music$believer imagine dragons"
input:"add an event to calendar on 28 October 2023 from 10AM to 12PM for Meeting" Output: "event$Meeting?Home?2023-10-28T15:30:00?2023-10-28T17:30:00"
input: "Write an essay on abcd" output: " prompting palm$please write an essay about abcd"
input: "I want to watch abcdef" output: "play video$abcdef"
input: "Play abcd video on youtube" output: "play video$abcd"
input: "Add a task to water the plants on 28 October 2023 at 10 AM" output: "task$Water plants?2023-10-28T10:00:00 "
input: "laptop" output:"prompting palm$what is laptop"
input: "Charles Babbage" output:"prompting palm$Who is Charles Babbage"
input: "xyz" output: "prompting palm$about xyz"
"""

    query2 = str("Input:Add an event today from 10AM to 12PM for a meeting Output:event$Meeting?Home?" + str(date.today()) + "T10:00:00?" + str(date.today()) + "T12:00:00")
    query3 = str("Input:Add an event tomorrow from 10AM to 12PM for a meeting Output:event$Meeting?Home?" + str(date.today() + timedelta(days=1)) + "T10:00:00?" + str(date.today() + timedelta(days=1)) + "T12:00:00")
    query4 = str("Input:Add an task today from 10AM for a meeting Output:task$Meeting?Home?" + str(date.today()) + "T10:00:00")
    query5 = str("Input:Add a task tomorrow from 10AM for a meeting Output:task$Meeting?Home?" + str(date.today() + timedelta(days=1)) + "T10:00:00")
    operation = talk_to_palm(query + query2 + query3 + query4 + query5 + input)
    if(operation != None):
        #print(operation)
        return operation

def final():  
    assistant_speaks("What's your name, Human?")
    name = 'Human'
    name = get_audio()
    assistant_speaks("Hello, " + str(name) + '.') 

    while (1):

        assistant_speaks("What can i do for you?")
        text = str(get_audio()).lower()

        if text == None or text == '0':
            print("Empty text")
            continue

        if "exit" in str(text) or "bye" in str(text) or "stop" in str(text):
            assistant_speaks("Ok bye, " + str(name) +'.')
            break

        # calling process text to process the query
        if(text != None):
            operation = get_operation(text)
            process(operation, text)
if __name__=="__main__":
    final()