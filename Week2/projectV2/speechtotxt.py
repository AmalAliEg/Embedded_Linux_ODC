import speech_recognition as sr
import time
import warnings
warnings.filterwarnings("ignore")

def setup_recognizer():
    """Initialize and configure the recognizer"""
    recognizer = sr.Recognizer()
    # Adjust recognition parameters for better command recognition
    recognizer.energy_threshold = 3000
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.6
    recognizer.phrase_threshold = 0.3
    return recognizer

def process_command(text):
    """Process the recognized text to identify GPS commands"""
    text = text.lower().strip()
    
    # Check for GPS commands
    if "gps" in text:
        if "on" in text or "open" in text:
            return "GPS ON"
        elif "off" in text or "close" in text:
            return "GPS OFF"
    
    return "Command not recognized. Please say 'GPS ON' or 'GPS OFF'"

def listen_for_command():
    """Listen for GPS commands"""
    recognizer = setup_recognizer()
    
    while True:
        try:
            with sr.Microphone() as source:
                print("\nListening for GPS command... (Say 'GPS ON' or 'GPS OFF')")
                
                # Adjust for ambient noise
                print("Adjusting for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Listen for audio
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                
                # Try to recognize the speech
                try:
                    text = recognizer.recognize_google(audio, language='en-US')
                    print(f"Recognized speech: {text}")
                    
                    # Process the command
                    result = process_command(text)
                    print(f"Command result: {result}")
                    
                    # If a valid command was recognized, return it
                    if result in ["GPS ON", "GPS OFF"]:
                        return result
                    
                except sr.UnknownValueError:
                    print("Could not understand audio. Please try again.")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                
        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("\nPlease try again...")
        time.sleep(1)

def main():
    print("=== GPS Voice Command System ===")
    print("You can say:")
    print("- 'GPS ON' to turn on GPS")
    print("- 'GPS OFF' to turn off GPS")
    
    while True:
        try:
            # Listen for command
            command = listen_for_command()
            
            # Process the command
            if command == "GPS ON":
                print("\nExecuting: Turning GPS ON")
                # Add your GPS ON logic here
                
            elif command == "GPS OFF":
                print("\nExecuting: Turning GPS OFF")
                # Add your GPS OFF logic here
            
            # Ask if user wants to continue
            response = input("\nDo you want to give another command? (yes/no): ").lower()
            if response != 'yes':
                break
                
        except KeyboardInterrupt:
            print("\nProgram terminated by user")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            continue

if __name__ == "__main__":
    main()