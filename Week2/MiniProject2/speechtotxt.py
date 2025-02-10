import speech_recognition as sr

def voice_to_text():
    recognizer = sr.Recognizer()
    
    while True:  # Continuous loop
        with sr.Microphone() as source:
            print("\nListening... Speak now! (Press Ctrl+C to exit)")
            
            recognizer.adjust_for_ambient_noise(source)
            
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                print("You said:", text)
                
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand what you said.")
            except sr.RequestError:
                print("Sorry, there was an error with the speech recognition service.")
            except KeyboardInterrupt:
                print("\nExiting...")
                break

if __name__ == "__main__":
    voice_to_text()