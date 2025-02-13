import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QGridLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl, QTimer, QDateTime
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon
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
                    audio = self.recognizer.listen(source)
                    text = self.recognizer.recognize_google(audio)
                    self.command_detected.emit(text.lower())
            except:
                pass
            
    def stop(self):
        self._running = False

class SmartControlHub(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Control Hub")
        self.setGeometry(0, 0, 900, 550)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLabel {
                color: white;
                font-size: 16px;
            }
        """)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.horizontal_layout = QHBoxLayout(self.central_widget)
        
        # Left Panel
        self.left_panel = QFrame()
        self.left_panel.setFrameShape(QFrame.StyledPanel)
        self.vertical_layout = QVBoxLayout(self.left_panel)
        
        # Date and Time Section
        self.date_time_frame = QFrame()
        self.date_time_layout = QHBoxLayout(self.date_time_frame)
        
        self.date_label = QLabel("Date:")
        self.day_label = QLabel("Day:")
        
        self.date_time_layout.addWidget(self.date_label)
        self.date_time_layout.addWidget(self.day_label)
        
        self.vertical_layout.addWidget(self.date_time_frame)
        
        # Voice Control Section
        self.voice_control_frame = QFrame()
        self.voice_layout = QVBoxLayout(self.voice_control_frame)
        
        self.mic_button = QPushButton()
        self.mic_button.setMinimumSize(64, 64)
        self.mic_button.setIcon(QIcon("speakerIcon.png"))

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
        
        # Right Panel (Maps)
        self.maps_frame = QFrame()
        self.maps_frame.setMinimumSize(400, 0)
        self.maps_frame.setStyleSheet("""
            QFrame#mapsFrame {
                background-color: white;
                border-radius: 10px;
            }
        """)
        self.maps_layout = QVBoxLayout(self.maps_frame)
        
        self.horizontal_layout.addWidget(self.maps_frame)
        
        # Initialize variables
        self.BLUE_COLOR = "#3498db"
        self.ORANGE_COLOR = "#ff9933"
        
        self.lights_active = False
        self.gps_active = False
        
        self.map_view = None
        
        # Setup date and time display
        self.setup_datetime()
        
        # Connect buttons
        self.lights_on_button.clicked.connect(lambda: self.handle_lights("on"))
        self.lights_off_button.clicked.connect(lambda: self.handle_lights("off"))
        self.gps_on_button.clicked.connect(lambda: self.handle_gps("on"))
        self.gps_off_button.clicked.connect(lambda: self.handle_gps("off"))
        
        # Initialize voice recognition
        self.setup_voice_recognition()

    def setup_datetime(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)
        self.update_datetime()

    def update_datetime(self):
        current_datetime = QDateTime.currentDateTime()
        date_text = current_datetime.toString("dd-MM-yyyy")
        time_text = current_datetime.toString("hh:mm:ss AP")
        day_text = current_datetime.toString("dddd")
        
        self.date_label.setText(f"Date: {date_text}")
        self.day_label.setText(f"Day: {day_text}")

    def setup_voice_recognition(self):
        self.voice_thread = VoiceThread()
        self.voice_thread.command_detected.connect(self.handle_voice_command)
        self.voice_thread.listening_status.connect(self.update_mic_status)
        self.voice_thread.start()

    def handle_voice_command(self, command):
        if "lights on" in command:
            self.handle_lights("on")
        elif "lights off" in command:
            self.handle_lights("off")
        elif "gps on" in command:
            self.handle_gps("on")
        elif "gps off" in command:
            self.handle_gps("off")

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
        
        if self.gps_active:
            self.setup_google_maps()
        else:
            if self.map_view:
                self.map_view.setParent(None)
                self.map_view = None

    def setup_google_maps(self):
        if not self.map_view:
            self.map_view = QWebEngineView()
            self.maps_layout.addWidget(self.map_view)
            self.map_view.setUrl(QUrl("https://www.google.com/maps"))

    def closeEvent(self, event):
        self.voice_thread.stop()
        self.voice_thread.wait()
        self.timer.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SmartControlHub()
    window.show()
    sys.exit(app.exec_())