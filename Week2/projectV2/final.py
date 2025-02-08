
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import speech_recognition as sr
import sys

class VoiceThread(QThread):
    command_detected = pyqtSignal(str)
    listening_status = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.is_running = True
        
        # Adjust these settings for your microphone
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 2000  # Lower threshold for built-in mic
        self.recognizer.pause_threshold = 0.5
        self.recognizer.phrase_threshold = 0.3

    def find_builtin_mic(self):
        try:
            mics = sr.Microphone.list_microphone_names()
            print("\nAvailable Microphones:")
            for idx, mic in enumerate(mics):
                print(f"{idx}: {mic}")
                # Look for ALC3246 or built-in audio
                if "alc3246" in mic.lower() or "built-in" in mic.lower():
                    return idx
            return None
        except Exception as e:
            print(f"Error finding microphone: {e}")
            return None

    def run(self):
        # Try to find the built-in microphone
        mic_index = self.find_builtin_mic()
        if mic_index is not None:
            print(f"Using microphone index: {mic_index}")
        else:
            print("Using default microphone")

        while self.is_running:
            try:
                # Use specific microphone if found, otherwise use default
                mic_config = {"device_index": mic_index} if mic_index is not None else {}
                with sr.Microphone(**mic_config) as source:
                    self.listening_status.emit(True)
                    print("Listening...")
                    
                    # Adjust for ambient noise
                    print("Adjusting for ambient noise...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    print(f"Energy threshold set to: {self.recognizer.energy_threshold}")
                    
                    try:
                        print("Ready for command...")
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        self.listening_status.emit(False)
                        
                        print("Processing audio...")
                        text = self.recognizer.recognize_google(audio)
                        print(f"Detected: {text}")
                        self.command_detected.emit(text)
                        
                    except sr.WaitTimeoutError:
                        print("Listening timeout - restarting")
                        self.listening_status.emit(False)
                        continue
                    except sr.UnknownValueError:
                        print("Could not understand the audio")
                        self.listening_status.emit(False)
                        continue
                    except sr.RequestError as e:
                        print(f"Could not request results; {e}")
                        self.listening_status.emit(False)
                        continue
                        
            except Exception as e:
                print(f"Microphone error: {e}")
                self.listening_status.emit(False)
                time.sleep(2)  # Wait before retrying
                continue

    def stop(self):
        self.is_running = False


class SmartControlHub(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the UI file
        uic.loadUi('smart_control_hub.ui', self)
        
        # Define colors
        self.BLUE_COLOR = "#3498db"
        self.ORANGE_COLOR = "#ff9933"
        
        # Initialize button states
        self.lights_active = False
        self.gps_active = False
        
        # Initialize voice recognition thread
        self.voice_thread = VoiceThread()
        self.voice_thread.command_detected.connect(self.handle_voice_command)
        self.voice_thread.listening_status.connect(self.update_mic_status)
        
        # Start voice recognition
        self.voice_thread.start()

        # Connect buttons to functions (for manual testing)
        self.lightsOnButton.clicked.connect(lambda: self.handle_lights("on"))
        self.lightsOffButton.clicked.connect(lambda: self.handle_lights("off"))
        self.gpsOnButton.clicked.connect(lambda: self.handle_gps("on"))
        self.gpsOffButton.clicked.connect(lambda: self.handle_gps("off"))

    def handle_lights(self, command):
        if command == "on":
            self.lightsOnButton.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.ORANGE_COLOR};
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                }}
            """)
            self.lights_active = True
        else:
            self.lightsOnButton.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.ORANGE_COLOR};
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                }}
            """)
            self.lights_active = False

    def handle_gps(self, command):
        if command == "on":
            self.gpsOnButton.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.ORANGE_COLOR};
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                }}
            """)
            self.mapsFrame.show()
            self.gps_active = True
        else:
            self.gpsOnButton.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.ORANGE_COLOR};
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                }}
            """)
            self.mapsFrame.hide()
            self.gps_active = False

    def handle_voice_command(self, command):
        """Handle voice commands and update UI accordingly"""
        command = command.lower()
        print(f"Processing command: {command}")
        
        if "light on" in command:
            self.handle_lights("on")
        elif "light off" in command:
            self.handle_lights("off")
        elif "gps on" in command:
            self.handle_gps("on")
        elif "gps off" in command:
            self.handle_gps("off")

    def update_mic_status(self, is_listening):
        """Update microphone button color based on listening status"""
        color = self.ORANGE_COLOR if is_listening else self.BLUE_COLOR
        self.micButton.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 32px;
            }}
        """)

    def closeEvent(self, event):
        """Clean up when closing the application"""
        self.voice_thread.stop()
        self.voice_thread.wait()
        event.accept()


def test_microphone():

    print("\nTesting Microphone Setup...")

    

    try:

        # Initialize recognizer

        r = sr.Recognizer()

        

        # List available microphones

        mics = sr.Microphone.list_microphone_names()

        print("\nAvailable Microphones:")

        for idx, mic in enumerate(mics):

            print(f"{idx}: {mic}")

        

        # Test recording

        print("\nTesting microphone recording...")

        with sr.Microphone() as source:

            print("Please speak a test phrase...")

            audio = r.listen(source, timeout=5)

            print("Audio captured!")

            

            # Try to recognize

            text = r.recognize_google(audio)

            print(f"Recognized text: {text}")

            

            return True

            

    except Exception as e:

        print(f"Microphone test failed: {e}")

        return False

        
# Main application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Test microphone before starting the application

    if test_microphone():

        print("Microphone test successful! Starting application...")

        window = SmartControlHub()

        window.show()

        sys.exit(app.exec_())

    else:

        print("Microphone test failed! Please check your microphone settings.")

        sys.exit(1)