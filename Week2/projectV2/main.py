from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import speech_recognition as sr
import sys
import time

# Test Commands Button Widget
class TestCommandsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        
        # Create test buttons
        self.light_on_btn = QPushButton("Test 'Light On' Command")
        self.light_off_btn = QPushButton("Test 'Light Off' Command")
        self.gps_on_btn = QPushButton("Test 'GPS On' Command")
        self.gps_off_btn = QPushButton("Test 'GPS Off' Command")
        
        # Add buttons to layout
        layout.addWidget(self.light_on_btn)
        layout.addWidget(self.light_off_btn)
        layout.addWidget(self.gps_on_btn)
        layout.addWidget(self.gps_off_btn)
        
        self.setLayout(layout)

class VoiceThread(QThread):
    command_detected = pyqtSignal(str)
    listening_status = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.is_running = True

    def run(self):
        while self.is_running:
            with sr.Microphone() as source:
                self.listening_status.emit(True)
                print("Listening...")
                try:
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source)
                    self.listening_status.emit(False)
                    
                    text = self.recognizer.recognize_google(audio)
                    print("Detected:", text)
                    self.command_detected.emit(text)
                    
                except sr.UnknownValueError:
                    print("Could not understand the audio")
                except sr.RequestError:
                    print("Could not request results from service")
                except Exception as e:
                    print(f"Error: {str(e)}")

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
        
        # Create and setup test commands widget
        self.test_widget = TestCommandsWidget()
        self.test_widget.setWindowTitle("Test Commands")
        self.test_widget.resize(200, 150)
        
        # Connect test buttons
        self.test_widget.light_on_btn.clicked.connect(
            lambda: self.handle_voice_command("light on"))
        self.test_widget.light_off_btn.clicked.connect(
            lambda: self.handle_voice_command("light off"))
        self.test_widget.gps_on_btn.clicked.connect(
            lambda: self.handle_voice_command("gps on"))
        self.test_widget.gps_off_btn.clicked.connect(
            lambda: self.handle_voice_command("gps off"))
        
        # Show test widget
        self.test_widget.show()
        
        # Initialize voice recognition thread
        self.voice_thread = VoiceThread()
        self.voice_thread.command_detected.connect(self.handle_voice_command)
        self.voice_thread.listening_status.connect(self.update_mic_status)
        
        # Start voice recognition
        self.voice_thread.start()

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
            print("Lights turned ON")
        else:
            self.lightsOnButton.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.BLUE_COLOR};
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                }}
            """)
            self.lights_active = False
            print("Lights turned OFF")

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
            print("GPS turned ON")
        else:
            self.gpsOnButton.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.BLUE_COLOR};
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                }}
            """)
            self.mapsFrame.hide()
            self.gps_active = False
            print("GPS turned OFF")

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
        color = self.ORANGE_COLOR if is_listening else self.BLUE_COLOR
        self.micButton.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 32px;
            }}
        """)

    def closeEvent(self, event):
        self.voice_thread.stop()
        self.voice_thread.wait()
        self.test_widget.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SmartControlHub()
    window.show()
    sys.exit(app.exec_())