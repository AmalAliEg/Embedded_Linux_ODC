from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl, QTimer, QDateTime
from PyQt5.QtWebEngineWidgets import QWebEngineView
import speech_recognition as sr
import sys

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
        uic.loadUi('smart_control_hub.ui', self)
        
        self.BLUE_COLOR = "#3498db"
        self.ORANGE_COLOR = "#ff9933"
        
        self.lights_active = False
        self.gps_active = False
        
        # Initialize map view
        self.map_view = None
        
        # Setup date and time display
        self.setup_datetime()
        
        # Connect buttons
        self.lightsOnButton.clicked.connect(lambda: self.handle_lights("on"))
        self.lightsOffButton.clicked.connect(lambda: self.handle_lights("off"))
        self.gpsOnButton.clicked.connect(lambda: self.handle_gps("on"))
        self.gpsOffButton.clicked.connect(lambda: self.handle_gps("off"))
        
        # Connect the Back button
        self.backButton.clicked.connect(self.handle_back_button)
        
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
        
        self.dateLabel.setText(f"Date: {date_text}")
        self.dayLabel.setText(f"Day: {day_text}")

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
        elif "back" in command:  # Handle voice command for "back"
            self.handle_back_button()

    def update_mic_status(self, is_listening):
        self.micButton.setStyleSheet(
            f"QPushButton#micButton {{ background-color: {self.ORANGE_COLOR if is_listening else self.BLUE_COLOR}; border-radius: 32px; }}"
        )

    def handle_lights(self, state):
        self.lights_active = state == "on"
        self.lightsOnButton.setEnabled(not self.lights_active)
        self.lightsOffButton.setEnabled(self.lights_active)

    def handle_gps(self, state):
        self.gps_active = state == "on"
        self.gpsOnButton.setEnabled(not self.gps_active)
        self.gpsOffButton.setEnabled(self.gps_active)
        
        if self.gps_active:
            self.setup_google_maps()
        else:
            if self.map_view:
                self.map_view.setParent(None)
                self.map_view = None

    def setup_google_maps(self):
        if not self.map_view:
            self.map_view = QWebEngineView()
            self.mapsLayout.addWidget(self.map_view)
            # Load the direct Google Maps URL
            self.map_view.setUrl(QUrl("https://www.google.com/maps"))

    def handle_back_button(self):
        """
        Handle the functionality of the Back button.
        For example, navigate to a previous screen or reset the UI.
        """
        print("Back button clicked")  # Replace with actual functionality
        # Example: Turn off GPS and lights when the back button is pressed
        self.handle_gps("off")
        self.handle_lights("off")

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