# importing speech recognition package from google api
import speech_recognition as sr
import playsound  # to play saved mp3 file
from gtts import gTTS  # google text to speech
import os  # to save/open files
import wolframalpha  # to calculate strings into formula
from selenium import webdriver  # to control browser operations

num = 1


def assistant_speaks(output):
    global num

    # num to rename every audio file
    # with different name to remove ambiguity
    num += 1

    toSpeak = gTTS(text=output, lang='en', slow=False)
    # saving the audio file given by google text to speech
    file = str(num)+".mp3"
    toSpeak.save(file)

    # playsound package is used to play the same file.
    print("Assistant : ", output)
    playsound.playsound(file, True)

    os.remove(file)


def process_text(input):
    try:
        if "search" in input or "play" in input:
            # a basic w
           # eb crawler using selenium
            # print("Here")
            search_web(input)
            return

        elif "who are you" in input or "define yourself" in input:
            speak = '''Hello, I am Person. Your personal Assistant.
			I am here to make your life easier. You can command me to perform
			various tasks such as calculating sums, searching google  or play youtube songs etcetra.'''
            assistant_speaks(speak)
            return

        elif "who made you" in input or "created you" in input:
            speak = "I have been created by Semicolon Programmer."
            assistant_speaks(speak)
            return

        elif "calculate" in input.lower():

            # write your wolframalpha app_id here
            app_id = ""
            client = wolframalpha.Client(app_id)

            indx = input.lower().split().index('calculate')
            query = input.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            assistant_speaks("The answer is " + answer)
            return

        else:

            assistant_speaks(
                "I could't understand,Please Try Again? or do you want to exit Than say Yes.")
            ans = get_audio()
            if 'yes' in str(ans) or 'yeah' in str(ans):
                return str(ans)
            process_text(ans)
    except:

        assistant_speaks(
            "I could't understand,Please Try Again? or do you wants to exit Than say Yes.")
        ans = get_audio()
        if 'yes' in str(ans) or 'yeah' in str(ans):
            return str(ans)
        process_text(ans)


def search_web(input):

    driver = webdriver.Firefox()
    driver.implicitly_wait(1)
    driver.maximize_window()

    if "youtube" in input.lower():

        assistant_speaks("Opening in youtube")
        indx = input.lower().split().index('youtube')
        query = input.split()[indx + 1:]
        url = "http://www.youtube.com/results?search_query=" + '+'.join(query)
        driver.get(url)

        return

    elif 'wikipedia' in input.lower():

        assistant_speaks("Opening Wikipedia")
        indx = input.lower().split().index('wikipedia')
        query = input.split()[indx + 1:]
        driver.get("https://en.wikipedia.org/wiki/" + '_'.join(query))
        return

    else:

        if 'google' in input:

            indx = input.lower().split().index('google')
            query = input.split()[indx + 1:]
            #print("https://www.google.com/search?q=" + '+'.join(query))
            driver.get("https://www.google.com/search?q=" + '+'.join(query))

        elif 'search' in input:

            indx = input.lower().split().index('search')
            query = input.split()[indx + 1:]
            driver.get("https://www.google.com/search?q=" + '+'.join(query))

        else:

            driver.get("https://www.google.com/search?q=" +
                       '+'.join(input.split()))

        return

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


# Driver Code
if __name__ == "__main__":
    name = 0
    while(name == 0):
        assistant_speaks("What's your name, Human?")
        name = 'Human'
        name = get_audio()
    assistant_speaks("Hello, " + str(name) + '.')        
    while(1):        
        
        assistant_speaks("What can i do for you?")
        text = get_audio()
        #print(text)

        if text == 0:
            continue
        else:
            text = text.lower()

        if "exit" in str(text) or "bye" in str(text) or "sleep" in str(text):
            assistant_speaks("Ok bye, " + name+'.')
            break

            # calling process text to process the query
        ans = process_text(text)
        if "yes" in str(ans):
                assistant_speaks("Ok bye, " + name+'.')
                break
           
