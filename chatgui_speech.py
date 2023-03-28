#Creating GUI with tkinter
import tkinter
from tkinter import *
from tkinter import messagebox as massage
from tkinter.filedialog import askopenfile
from tkinter import filedialog
from chatapp import chatbot_response
import speech_recognition as sr
import playsound
#playsound = 1.2.2
from summa import *
from gtts import gTTS
from pygoogletranslation import Translator
from langdetect import detect

def lang_detect(patterns):
    #global lang_detector
    lang_detector = detect(patterns)
    print("Translate from "+lang_detector)
    return lang_detector

def translate_to_en(patterns):
    global lang_src
    lang_src = lang_detect(patterns)
    try:
        translator = Translator()
        translation = translator.translate(patterns,src = '%s'%lang_src,dest = 'en')
        #preprocess to remove unnecessary result of pygoogletranslation 
        # initializing substrings
        sub1 = "text="
        sub2 = ", pronunciation"
        # getting index of substrings
        idx1 = str(translation).index(sub1)
        idx2 = str(translation).index(sub2)
        result_en = ''
        # getting elements in between
        for idx in range(idx1 + len(sub1) , idx2):
            result_en = result_en + str(translation)[idx]
        print(result_en)
        return result_en
    except StopIteration:
        pass

def translate_to_dest(patterns):
    try:
        translator_dest = Translator()
        translation = translator_dest.translate(patterns,src = 'en',dest = '%s'%lang_src)
        #preprocess to remove unnecessary result of pygoogletranslation 
        # initializing substrings
        sub3 = "text="
        sub4 = ", pronunciation"
        # getting index of substrings
        idx3 = str(translation).index(sub3)
        idx4 = str(translation).index(sub4)
        result_dest = ''
        # getting elements in between
        for idx in range(idx3 + len(sub3) , idx4):
            result_dest = result_dest + str(translation)[idx]
        print("Translate result: "+result_dest)
        return result_dest
    except StopIteration:
        pass

#Input speech
def listen(duration):
    base = sr.Recognizer()
    with sr.Microphone() as source:
        text = base.record(source, duration=duration)
        try:
            print("Recognizing the text")
            return base.recognize_google(text,language="en-US")
        except Exception as ex:
            print(ex)

#Output speech voice
id = 0   	
def speak(massage):
    lang_dest = lang_detect(massage)
    speech = gTTS(text=massage, lang= "%s"%lang_dest)
    filename="voice_%s_%d.mp3"%(lang_dest,id)
    speech.save(filename)
    playsound.playsound(filename)

def speak_en(massage):
    speech = gTTS(text=massage, lang= "en")
    filename="voice_en_%d.mp3"%id
    speech.save(filename)
    playsound.playsound(filename)

#Function
def activate_microphone_language(choice):
    choice = variable.get()
    base = sr.Recognizer()
    with sr.Microphone() as source:
        text = base.record(source, duration=5)
        try:
            print("Recognizing the text")
            text = base.recognize_google(text,language=choice)
        except Exception as ex:
            print(ex)
    smsg = str(text)
    smsg_en = translate_to_en(smsg)
    global id
    id = id+1
    print(smsg_en)
    EntryBox.insert(END, smsg)
    EntryBox.delete("0.0",END)
    if smsg_en != '':
        
        res = chatbot_response(smsg_en)
        result_trans = translate_to_dest(res)
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + smsg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        ChatLog.insert(END, "Bot: " + result_trans + '\n\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
        #Output speaker voice
        speak(str(result_trans))

def activate_microphone_en():
    text = listen(5)
    smsg = str(text)
    global id
    id = id+1
    print(smsg)
    EntryBox.insert(END, smsg)
    EntryBox.delete("0.0",END)
    if smsg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + smsg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        res = chatbot_response(smsg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
        #Output speaker voice
        print(res)
        speak(str(res))
        
def send():
    #Input
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    msg_en = translate_to_en(msg)
    
    global id
    id = id + 1
    #Execute
    if msg_en != '':
        res = chatbot_response(msg_en)
        print('response:'+res)
        result_dest = translate_to_dest(res)
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        ChatLog.insert(END, "Bot: " + result_dest + '\n\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
        speak(str(result_dest))

def search_google():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    if msg != '':
        try:
            from googlesearch import search
        except ImportError:
            print("No module named 'google' found")
        # to search
        ChatLog.insert(END, "You: " + msg + '\n\n')
        for j in search(msg, tld="co.in", num=10, stop=10, pause=2):
            print(j)
            #res = chatbot_response(msg)
            ChatLog.config(state=NORMAL)
            ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
            ChatLog.insert(END, j + '\n\n')
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)

def upload_text():
    try:
        file_path=filedialog.askopenfilename()
        uploaded= open(file_path)
        data = uploaded.read()
        global id
        id = id + 1
        if data != '':
            ChatLog.config(state=NORMAL)
            summarization = summarizer.summarize(data)
            ChatLog.insert(END, "Bot: " + summarization + '\n\n')
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)
            print(summarization)
            speak_en(str(summarization))
    except:
        pass
def summary():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    global id
    id = id + 1
    
    #Execute
    if msg != '':
        ChatLog.config(state=NORMAL)
        summarization = summarizer.summarize(msg)
        ChatLog.insert(END, "Bot: " + summarization + '\n\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
    print(summarization)
    speak_en(str(summarization))
    return summarization

base = Tk()
base.title("Modern Chatbot")
base.geometry("1366x768")
base.resizable(width=FALSE, height=FALSE)
#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.config(state=DISABLED)
#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set
# creating widget
language_list = ['en','vi','ja','fr','zh-CN','ko']
# set default country as United States
variable = StringVar()
variable.set(language_list[0])
dropdown = OptionMenu(
    base,
    variable,
    *language_list,
    command=activate_microphone_language
)
# positioning widget
dropdown.pack(expand=True)
dropdown.place(x=6, y = 566 )
#Create Button to send message
SendButton = Button(base, font=("Verdana",7,'bold'), text="Send", width="16", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )
ActiveButton = Button(base, font=("Verdana",7,'bold'), text="Activate Microphone", width="16", height=5,
                    bd=0, bg="#FFD700", activebackground="#3c9d9b",fg='#ffffff',
                    command= activate_microphone_en )
SummarizerButton = Button(base, font=("Verdana",7,'bold'), text="Summarize", width="16", height=5,
                    bd=0, bg="#1E90FF", activebackground="#3c9d9b",fg='#ffffff',
                    command= summary )
UploadSummarizeButton = Button(base, font=("Verdana",7,'bold'), text="Upload & summarize", width="16", height=5,
                    bd=0, bg="#EE2C2C", activebackground="#3c9d9b",fg='#ffffff',
                    command= upload_text )
SearchGoogleButton = Button(base, font=("Verdana",7,'bold'), text="Search Google", width="16", height=5,
                    bd=0, bg="#DEB887", activebackground="#3c9d9b",fg='#ffffff',
                    command= search_google )
#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
#EntryBox.bind("<Return>", send)
#Place all components on the screen
scrollbar.place(x=1346,y=10, height=400)
ChatLog.place(x=6,y=6, height=400, width=1345)
EntryBox.place(x=128, y=420, height=340, width=1230)
SendButton.place(x=6, y=420, height=30)
ActiveButton.place(x=6,y=456,height=30)
SummarizerButton.place(x=6,y=494,height=30)
UploadSummarizeButton.place(x=6, y=530, height=30 )
SearchGoogleButton.place(x= 6,y= 602, height= 30)
base.mainloop()
