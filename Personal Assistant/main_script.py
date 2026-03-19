# importing speech recognition package from google api
import speech_recognition as sr
import playsound  # to play saved mp3 file
from gtts import gTTS  # google text to speech
import os  # to save/open files
import tempfile
#import wolframalpha  # to calculate strings into formula
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
    output = str(output)
    print("PerSon : ", output)

    to_speak = gTTS(text=output, lang='en', slow=False)
    # Use a temporary file so concurrent runs do not overwrite the same mp3.
    fd, file_path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)

    try:
        to_speak.save(file_path)
        # playsound package is used to play the same file.
        playsound.playsound(file_path, True)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


def get_audio():

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Speak...")

            # recording the audio using speech recognition
            audio = recognizer.listen(source, phrase_time_limit=5)
        print("Stop.")  # limit 5 secs
    except OSError:
        assistant_speaks("Microphone is not available. Please check your audio device.")
        return None

    try:
        text = recognizer.recognize_google(audio, language='en-US')
        print("You : ", text)
        return text

    except sr.UnknownValueError:
        assistant_speaks("Could not understand your audio, please try again.")
        return None
    except sr.RequestError:
        assistant_speaks("Speech service is unavailable right now. Please try again.")
        return None


def _fallback_to_palm(text):
    try:
        res = talk_to_palm("about " + text)
        if res is not None:
            if len(res) < 350:
                assistant_speaks(res)
                print(res)
            else:
                print(res)
                assistant_speaks("Result is ready")
        else:
            assistant_speaks("Please try again")
    except Exception:
        assistant_speaks("Please try again")

def process(operator, text):
    if not operator or "$" not in operator:
        _fallback_to_palm(text)
        return

    operation_name, _, operation_data = operator.partition("$")
    operation_name = operation_name.strip().lower()
    operation_data = operation_data.strip()

    if "playing music" in operation_name:
        try:
            if not operation_data:
                raise ValueError("Missing song details")
            play_song(operation_data)
            assistant_speaks("Song is playing")
        except Exception:
            assistant_speaks("Please try again")
    elif "prompting palm" in operation_name:
        try:
            if not operation_data:
                raise ValueError("Missing prompt")
            res = talk_to_palm(operation_data)

            if res is None:
                assistant_speaks("Please try again")
            else:
                if len(res) < 300:
                    assistant_speaks(res)
                else:
                    assistant_speaks("Your result is ready")
        except Exception:
            assistant_speaks("Please try again")
    elif "event" in operation_name:
        try:
            if not operation_data:
                raise ValueError("Missing event details")
            data = operation_data.split('?')
            add_event(data)
            assistant_speaks("Your event is added to your calendar")
        except Exception:
            assistant_speaks("Please try again")
    elif "play video" in operation_name:
        try:
            if not operation_data:
                raise ValueError("Missing video details")
            data = operation_data.split()
            video_name = '+'.join(data)
            url = "https://www.youtube.com/results?search_query=" + video_name
            webbrowser.open_new_tab(url)
        except Exception:
            assistant_speaks("Please try again")
    elif "task" in operation_name:
        try:
            if not operation_data:
                raise ValueError("Missing task details")
            data = operation_data.split('?')
            add_task(data)
            assistant_speaks("Your task is added to your calendar")
        except Exception:
            assistant_speaks("Please try again")
    else:
        assistant_speaks("Please elaborate. Your command is unclear")

def get_operation(user_input):
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
    operation = talk_to_palm(query + query2 + query3 + query4 + query5 + user_input)
    if operation is not None:
        return operation
    return None

def final():  
    assistant_speaks("What's your name, Human?")
    name = 'Human'
    detected_name = get_audio()
    if detected_name:
        name = detected_name
    assistant_speaks("Hello, " + str(name) + '.') 

    while True:

        assistant_speaks("What can i do for you?")
        audio_text = get_audio()
        if not audio_text:
            print("Empty text")
            continue

        text = audio_text.lower()

        if "exit" in str(text) or "bye" in str(text) or "stop" in str(text):
            assistant_speaks("Ok bye, " + str(name) +'.')
            break

        # calling process text to process the query
        operation = get_operation(text)
        process(operation, text)


if __name__=="__main__":
    final()