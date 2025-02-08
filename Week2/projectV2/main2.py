from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import speech_recognition as sr
import sys

# Thread class for voice recognition
class VoiceThread(QThread):
    command_detected = pyqtSignal(str)  # Signal for detected command
    listening_status = pyqtSignal(bool)  # Signal for listening status

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.is_running = True

    def run(self):
        while self.is_running:
            with sr.Microphone() as source:
                self.listening_status.emit(True)  # Signal that we're listening
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source)
                try:
                    audio = self.recognizer.listen(source)
                    self.listening_status.emit(False)  # Signal that we're processing
                    
                    # Try to recognize the speech
                    text = self.recognizer.recognize_google(audio)
                    print("Detected:", text)
                    self.command_detected.emit(text)
                    
                except sr.UnknownValueError:
                    print("Could not understand the audio")
                except sr.RequestError:
                    print("Could not request results from service")

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

# Main application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SmartControlHub()
    window.show()
    sys.exit(app.exec_())