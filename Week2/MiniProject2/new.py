import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QGridLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl, QTimer, QDateTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
import speech_recognition as sr

class VoiceThread(QThread):
    command_detected = pyqtSignal(str)
    listening_status = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self._running = True
        
    def run(self):
        while self._running:
            try:
                with sr.Microphone() as source:
                    self.listening_status.emit(True)
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source)
                    text = self.recognizer.recognize_google(audio)
                    self.command_detected.emit(text.lower())
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError:
                print("Could not request results")
            except Exception as e:
                print(f"Error in voice recognition: {e}")
            
    def stop(self):
        self._running = False

class SmartControlHub(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Control Hub")
        self.setGeometry(0, 0, 900, 550)
        
        # Main layout setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.horizontal_layout = QHBoxLayout(central_widget)
        
        # Left panel setup
        self.left_panel = QWidget()
        self.vertical_layout = QVBoxLayout(self.left_panel)
        
        # Voice Control Section
        self.voice_control_frame = QFrame()
        self.voice_layout = QVBoxLayout(self.voice_control_frame)
        
        self.mic_button = QPushButton()
        self.mic_button.setMinimumSize(64, 64)
        self.mic_button.setObjectName("micButton")
        self.mic_button.setStyleSheet("""
            QPushButton#micButton {
                background-color: #3498db;
                border-radius: 32px;
            }
            QPushButton#micButton:hover {
                background-color: #ff9933;
            }
        """)
        
        self.voice_layout.addWidget(self.mic_button, alignment=Qt.AlignCenter)
        self.vertical_layout.addWidget(self.voice_control_frame)
        
        # Control Buttons
        self.control_buttons_frame = QFrame()
        self.control_buttons_layout = QGridLayout(self.control_buttons_frame)
        
        self.lights_on_button = QPushButton("Lights On")
        self.gps_on_button = QPushButton("GPS On")
        self.lights_off_button = QPushButton("Lights Off")
        self.gps_off_button = QPushButton("GPS Off")
        
        self.control_buttons_layout.addWidget(self.lights_on_button, 0, 0)
        self.control_buttons_layout.addWidget(self.gps_on_button, 0, 1)
        self.control_buttons_layout.addWidget(self.lights_off_button, 1, 0)
        self.control_buttons_layout.addWidget(self.gps_off_button, 1, 1)
        
        self.vertical_layout.addWidget(self.control_buttons_frame)
        
        self.horizontal_layout.addWidget(self.left_panel)
        
        # Initialize variables
        self.BLUE_COLOR = "#3498db"
        self.ORANGE_COLOR = "#ff9933"
        
        self.lights_active = False
        self.gps_active = False
        
        # Connect buttons
        self.lights_on_button.clicked.connect(lambda: self.handle_lights("on"))
        self.lights_off_button.clicked.connect(lambda: self.handle_lights("off"))
        self.gps_on_button.clicked.connect(lambda: self.handle_gps("on"))
        self.gps_off_button.clicked.connect(lambda: self.handle_gps("off"))
        
        # Initialize voice recognition
        self.setup_voice_recognition()

    def setup_voice_recognition(self):
        self.voice_thread = VoiceThread()
        self.voice_thread.command_detected.connect(self.handle_voice_command)
        self.voice_thread.listening_status.connect(self.update_mic_status)
        self.voice_thread.start()

    def handle_voice_command(self, command):
        # Handle voice commands and update button colors
        if "lights on" in command:
            self.handle_lights("on")
            self.lights_on_button.setStyleSheet(f"background-color: {self.ORANGE_COLOR};")
            self.lights_off_button.setStyleSheet(f"background-color: {self.BLUE_COLOR};")
        elif "lights off" in command:
            self.handle_lights("off")
            self.lights_off_button.setStyleSheet(f"background-color: {self.ORANGE_COLOR};")
            self.lights_on_button.setStyleSheet(f"background-color: {self.BLUE_COLOR};")
        elif "gps on" in command:
            self.handle_gps("on")
            self.gps_on_button.setStyleSheet(f"background-color: {self.ORANGE_COLOR};")
            self.gps_off_button.setStyleSheet(f"background-color: {self.BLUE_COLOR};")
        elif "gps off" in command:
            self.handle_gps("off")
            self.gps_off_button.setStyleSheet(f"background-color: {self.ORANGE_COLOR};")
            self.gps_on_button.setStyleSheet(f"background-color: {self.BLUE_COLOR};")

    def update_mic_status(self, is_listening):
        self.mic_button.setStyleSheet(
            f"QPushButton#micButton {{ background-color: {'#ff9933' if is_listening else '#3498db'}; border-radius: 32px; }}"
        )

    def handle_lights(self, state):
        self.lights_active = state == "on"
        self.lights_on_button.setEnabled(not self.lights_active)
        self.lights_off_button.setEnabled(self.lights_active)

    def handle_gps(self, state):
        self.gps_active = state == "on"
        self.gps_on_button.setEnabled(not self.gps_active)
        self.gps_off_button.setEnabled(self.gps_active)

    def closeEvent(self, event):
        self.voice_thread.stop()
        self.voice_thread.wait()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SmartControlHub()
    window.show()
    sys.exit(app.exec_())