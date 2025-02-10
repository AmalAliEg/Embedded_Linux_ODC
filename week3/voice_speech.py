import speech_recognition as sr

r=sr.Recognizer() #tha var that store the value from recongizer function which is on of the speech_recognition functions


#loop  to listen to the microphone continusly 
while True:
    #try where it try to understand the voice 
    try:
        #continue reads the microphone , where microphone is the source (input)
        with sr.Microphone() as source:
            #print a msg for the user 
            print("Say something!")
            #take what the user said add it to audio var using the Listen()
            audio=r.listen(source)
            #send this audio to google api to reconize it and add it in text
            text=r.recongizer_google(audio)
            #make the text in lower case
            text.lower
            #show msg to user 
            print("you said: {text}")


    #exception where run if there error with try 
    except:
        print("mic doesn't work!")
        r=sr.Recognizer() #tha var that store the value from recongizer function which is on of the speech_recognition functions
        continue


