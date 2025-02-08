from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

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
        
        # Connect buttons to functions (for testing without voice)
        self.lightsOnButton.clicked.connect(lambda: self.handle_lights("on"))
        self.lightsOffButton.clicked.connect(lambda: self.handle_lights("off"))
        self.gpsOnButton.clicked.connect(lambda: self.handle_gps("on"))
        self.gpsOffButton.clicked.connect(lambda: self.handle_gps("off"))

        # Set up mic button with the SVG icon
        self.micButton.setIcon(QIcon("mic_icon.svg"))
        self.micButton.setIconSize(QSize(32, 32))
        self.micButton.setText("")
        

    def handle_lights(self, command):
        if command == "on":
            # Change Lights On button to orange
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
            # Change Lights On button back to blue
            self.lightsOnButton.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.BLUE_COLOR};
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                }}
            """)
            self.lights_active = False

    def handle_gps(self, command):
        if command == "on":
            # Change GPS On button to orange
            self.gpsOnButton.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.ORANGE_COLOR};
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                }}
            """)
            self.mapsFrame.show()  # Show maps frame
            self.gps_active = True
        else:
            # Change GPS On button back to blue
            self.gpsOnButton.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.BLUE_COLOR};
                    color: white;
                    border-radius: 5px;
                    padding: 10px;
                }}
            """)
            self.mapsFrame.hide()  # Hide maps frame
            self.gps_active = False

    def handle_voice_command(self, command):
        """
        Handle voice commands and update UI accordingly
        This will be called from your voice recognition system
        """
        command = command.lower()
        
        if "light on" in command:
            self.handle_lights("on")
        elif "light off" in command:
            self.handle_lights("off")
        elif "gps on" in command:
            self.handle_gps("on")
        elif "gps off" in command:
            self.handle_gps("off")

    def update_mic_status(self, is_listening):
        """
        Update microphone button color based on listening status
        """
        color = self.ORANGE_COLOR if is_listening else self.BLUE_COLOR
        self.micButton.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 32px;
            }}
        """)

# Main application
if __name__ == '__main__':
    app = QApplication([])
    window = SmartControlHub()
    window.show()
    app.exec_()