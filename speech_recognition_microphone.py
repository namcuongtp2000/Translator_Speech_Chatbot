import speech_recognition as sr
def speech2text():
    recognizer = sr.Recognizer()

    ''' recording the sound '''

    with sr.Microphone() as source:
        print("Adjusting noise ")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Recording for 5 seconds")
        recorded_audio = recognizer.listen(source, timeout=5)
        print("Done recording")

    ''' Recorgnizing the Audio '''
    try:
        print("Recognizing the text")
        smsg = recognizer.recognize_google(
            recorded_audio, 
            language="en-US"
        )
        print("Decoded Text : {}".format(smsg))

    except Exception as ex:
        print(ex)
    