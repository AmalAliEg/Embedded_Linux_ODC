import sys
import vlc
import yt_dlp
import pygame
import requests
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget, 
                           QVBoxLayout, QLabel, QLCDNumber, QListWidget, 
                           QFileDialog, QSlider, QComboBox, QFrame, QHBoxLayout,
                           QGridLayout)
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QFont
from PyQt5.QtCore import (Qt, QTimer, QTime, QSize, QThread, pyqtSignal, 
                         QDateTime, QUrl)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import speech_recognition as sr

# Weather API details
API_KEY = "9b461f6d62d59555b0471ff99ca0c782"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

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
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Smart Control Hub")
        self.setGeometry(0, 0, 900, 550)
        
        # Initialize main widget and layouts
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.horizontal_layout = QHBoxLayout(self.central_widget)
        
        # Left Panel
        self.setup_left_panel()
        
        # Right Panel (Maps)
        self.setup_right_panel()
        
        # Initialize variables
        self.BLUE_COLOR = "#3498db"
        self.ORANGE_COLOR = "#ff9933"
        self.lights_active = False
        self.gps_active = False
        self.map_view = None
        
        # Setup components
        self.setup_datetime()
        self.setup_voice_recognition()
        
        # Connect buttons
        self.connect_buttons()

    def setup_left_panel(self):
        self.left_panel = QFrame()
        self.left_panel.setFrameShape(QFrame.StyledPanel)
        self.vertical_layout = QVBoxLayout(self.left_panel)
        
        # Date and Time Section
        self.setup_datetime_section()
        
        # Voice Control Section
        self.setup_voice_control()
        
        # Control Buttons
        self.setup_control_buttons()
        
        self.horizontal_layout.addWidget(self.left_panel)

    def setup_datetime_section(self):
        self.date_time_frame = QFrame()
        self.date_time_layout = QHBoxLayout(self.date_time_frame)
        
        self.date_label = QLabel("Date:")
        self.day_label = QLabel("Day:")
        
        self.date_time_layout.addWidget(self.date_label)
        self.date_time_layout.addWidget(self.day_label)
        
        self.vertical_layout.addWidget(self.date_time_frame)

    def setup_voice_control(self):
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


    def setup_control_buttons(self):
        self.control_buttons_frame = QFrame()
        self.control_buttons_layout = QGridLayout(self.control_buttons_frame)
        
        self.lights_on_button = QPushButton("Lights On")
        self.gps_on_button = QPushButton("GPS On")
        self.lights_off_button = QPushButton("Lights Off")
        self.gps_off_button = QPushButton("GPS Off")
        
        # Back button
        self.back_button = QPushButton("Back", self)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #093A3E;
                color: #7E9D9E;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
                border: 2px solid #7E9D9E;
            }
            QPushButton:hover {
                background-color: #10555B;
            }
        """)
        self.back_button.clicked.connect(self.back_to_main)
        
        self.control_buttons_layout.addWidget(self.lights_on_button, 0, 0)
        self.control_buttons_layout.addWidget(self.gps_on_button, 0, 1)
        self.control_buttons_layout.addWidget(self.lights_off_button, 1, 0)
        self.control_buttons_layout.addWidget(self.gps_off_button, 1, 1)
        self.control_buttons_layout.addWidget(self.back_button, 2, 0, 1, 2)
        
        self.vertical_layout.addWidget(self.control_buttons_frame)

    def setup_right_panel(self):
        self.maps_frame = QFrame()
        self.maps_frame.setMinimumSize(400, 0)
        self.maps_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
            }
        """)
        self.maps_layout = QVBoxLayout(self.maps_frame)
        self.horizontal_layout.addWidget(self.maps_frame)

    def setup_datetime(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)
        self.update_datetime()

    def update_datetime(self):
        current_datetime = QDateTime.currentDateTime()
        date_text = current_datetime.toString("dd-MM-yyyy")
        day_text = current_datetime.toString("dddd")
        
        self.date_label.setText(f"Date: {date_text}")
        self.day_label.setText(f"Day: {day_text}")

    def setup_voice_recognition(self):
        self.voice_thread = VoiceThread()
        self.voice_thread.command_detected.connect(self.handle_voice_command)
        self.voice_thread.listening_status.connect(self.update_mic_status)
        self.voice_thread.start()

    def connect_buttons(self):
        self.lights_on_button.clicked.connect(lambda: self.handle_lights("on"))
        self.lights_off_button.clicked.connect(lambda: self.handle_lights("off"))
        self.gps_on_button.clicked.connect(lambda: self.handle_gps("on"))
        self.gps_off_button.clicked.connect(lambda: self.handle_gps("off"))

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

    def back_to_main(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def closeEvent(self, event):
        self.voice_thread.stop()
        self.voice_thread.wait()
        self.timer.stop()
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_Q:
            self.close()
        else:
            super().keyPressEvent(event)

            #part3
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Merget System for User Interface using Raspberry Pi.")
        self.setGeometry(0, 0, 900, 550)
        self.setWindowIcon(QIcon("icons_home.png"))

        # Set background color
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#001819"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # Home button for Smart Home
        self.open_button = QPushButton(self)
        self.open_button.setIcon(QIcon("iconsr_home.png"))
        self.open_button.setIconSize(QSize(250, 150))
        self.open_button.setGeometry(130, 160, 150, 150)
        self.open_button.setStyleSheet("background-color: transparent; border: none;")
        self.open_button.clicked.connect(self.open_sub_window)

        # TV button for Smart TV
        self.open_buttontv = QPushButton(self)
        self.open_buttontv.setIcon(QIcon("icons_tv.png"))
        self.open_buttontv.setIconSize(QSize(150, 150))
        self.open_buttontv.setGeometry(370, 180, 150, 150)
        self.open_buttontv.setStyleSheet("background-color: transparent; border: none;")
        self.open_buttontv.clicked.connect(self.open_sub_window2)

        # Car button for Smart Car
        self.open_buttoncar = QPushButton(self)
        self.open_buttoncar.setIcon(QIcon("car.png"))
        self.open_buttoncar.setIconSize(QSize(150, 150))
        self.open_buttoncar.setGeometry(589, 180, 150, 150)
        self.open_buttoncar.setStyleSheet("background-color: transparent; border: none;")
        self.open_buttoncar.clicked.connect(self.open_sub_window4)

    def open_sub_window(self):
        self.sub_window = SubWindow()
        self.sub_window.show()
        self.close()

    def open_sub_window2(self):
        self.sub_window2 = TVWindow()
        self.sub_window2.show()
        self.close()

    def open_sub_window4(self):
        self.sub_window4 = SmartControlHub()
        self.sub_window4.show()
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_Q:
            self.close()
        else:
            super().keyPressEvent(event)

class TVWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("My Smart TV")
        self.setGeometry(0, 0, 900, 550)
        self.setStyleSheet("background-color: #001819;")

        # VLC instance
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()

        # Main widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
    
        # Video frame
        self.video_frame = QFrame(self)
        self.video_frame.setStyleSheet("background-color: black; border: 2px solid #7E9D9E;")
        self.video_frame.setFixedSize(800, 450)

        # Title Label
        self.title_label = QLabel("Smart TV", self)
        self.title_label.setStyleSheet("color: #7E9D9E; font-size: 24px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)

        # Buttons layout
        button_layout = QHBoxLayout()

        # Channel buttons
        self.channel_buttons = []
        self.video_links = [
            "https://www.youtube.com/watch?v=bNyUyrR0PHo",
            "https://www.youtube.com/watch?v=edd_JfhC7i4",
            "https://www.youtube.com/watch?v=zq8xgqZxb0k",
            "https://www.youtube.com/watch?v=0FBiyFpV__g",
            "https://www.youtube.com/watch?v=x5MkVTvOViQ",
        ]

        # Button Style
        button_style = """
            QPushButton {
                background-color: #093A3E;
                color: #7E9D9E;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
                border: 2px solid #7E9D9E;
            }
            QPushButton:hover {
                background-color: #10555B;
            }
            QPushButton:pressed {
                background-color: #092E31;
            }
        """

        #part 4
        # Continue TVWindow class
        for i in range(5):
            btn = QPushButton(f"Channel {i+1}", self)
            btn.setStyleSheet(button_style)
            btn.clicked.connect(lambda _, idx=i: self.play_video(idx))
            button_layout.addWidget(btn)
            self.channel_buttons.append(btn)

        # Exit button
        self.exit_button = QPushButton("Back", self)
        self.exit_button.setStyleSheet(button_style)
        self.exit_button.clicked.connect(self.back_to_main)
        button_layout.addWidget(self.exit_button)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.video_frame)
        layout.addLayout(button_layout)
        self.central_widget.setLayout(layout)

        # Set VLC output to PyQt widget
        if sys.platform.startswith("linux"):
            self.media_player.set_xwindow(int(self.video_frame.winId()))
        elif sys.platform == "win32":
            self.media_player.set_hwnd(int(self.video_frame.winId()))

    def get_youtube_url(self, url):
        """Fetch the direct video URL from YouTube"""
        ydl_opts = {'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['url']

    def play_video(self, channel_index):
        """Play selected channel"""
        youtube_url = self.video_links[channel_index]
        direct_url = self.get_youtube_url(youtube_url)

        media = self.instance.media_new(direct_url)
        self.media_player.set_media(media)
        self.media_player.play()

    def close_app(self):
        """Stop video and close the application"""
        self.media_player.stop()
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)

    def back_to_main(self):
        self.media_player.stop()
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_Q:
            self.close()
        else:
            super().keyPressEvent(event)

class SubWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("My Smart Home")
        self.setGeometry(0, 0, 900, 550)

        # Set background color
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#001819"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # Digital clock display
        self.clock_display = QLCDNumber(self)
        self.clock_display.setGeometry(20, 20, 320, 120)
        self.clock_display.setStyleSheet("color: #7E9D9E; background: #1B3435; border: 2px solid #7E9D9E;")
        self.clock_display.setDigitCount(8)

        # Setup timer for clock
        timer = QTimer(self)
        timer.timeout.connect(self.update_clock)
        timer.start(1000)
        self.update_clock()

        # City selection combo box
        self.setup_city_combo()
        
        # Weather display
        self.setup_weather_display()

        # Music player components
        self.setup_music_player()

        # Initialize pygame
        pygame.mixer.init()
        self.is_playing = False
        self.is_repeating = False
        self.current_track = None

    def setup_city_combo(self):
        self.city_combo = QComboBox(self)
        cities = ["Cairo", "German", "Saudi Arabia", "New York", "London", "Tokyo", "Paris"]
        self.city_combo.addItems(cities)
        self.city_combo.setStyleSheet("""
            background-color: #1B3435;
            color: #7E9D9E;
            font-size: 18px;
            border-radius: 5px;
            padding: 5px;
        """)
        self.city_combo.setGeometry(20, 200, 320, 40)
        self.city_combo.currentIndexChanged.connect(self.on_city_selected)

    def setup_weather_display(self):
        # City label
        self.city_label = QLabel("Weather in Cairo", self)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_label.setFont(QFont("Arial", 12))
        self.city_label.setStyleSheet("color: #7E9D9E;")
        self.city_label.setGeometry(70, 200, 350, 350)

        # Weather display area
        self.weather_display = QLabel(self)
        self.weather_display.setGeometry(20, 245, 390, 300)
        self.weather_display.setStyleSheet("border: 2px solid #7E9D9E; color: #FFD700;")

        # Weather icon
        self.weather_icon = QLabel(self.weather_display)
        self.weather_icon.setAlignment(Qt.AlignCenter)
        self.weather_icon.setFixedSize(150, 150)
        self.weather_icon.setStyleSheet("background: transparent;")

        # Temperature label
        self.result_label = QLabel("Fetching weather...", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.result_label.setStyleSheet("color: #FFD700;")
        self.result_label.setGeometry(20, 400, 300, 40)

        # Initial weather update
        self.get_weather("Cairo")
        weather_timer = QTimer(self)
        weather_timer.timeout.connect(lambda: self.get_weather(self.city_combo.currentText()))
        weather_timer.start(1800000)  # Update every 30 minutes


        #part5
    def setup_music_player(self):
        # Add MP3 button
        self.add_button = self.create_toggle_button("Add", "icons_headphones.png", 800, 20)
        self.add_button.clicked.connect(self.add_mp3_to_playlist)

        # Play/Pause button
        self.play_button = self.create_toggle_button("Play", "icons_speaker.png", 800, 120)
        self.play_button.clicked.connect(self.toggle_play)

        # Repeat button
        self.repeat_button = self.create_toggle_button("Repeat", "icons_repeat.png", 800, 220)
        self.repeat_button.clicked.connect(self.toggle_repeat)

        # Home button
        self.home_button = self.create_toggle_button("Home", "icons_house.png", 800, 320)
        self.home_button.clicked.connect(self.open_sub_window3)

        # Back button
        self.back_button = self.create_toggle_button("Back", "icons_back.png", 800, 420)
        self.back_button.clicked.connect(self.back_to_main)

        # Volume slider
        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setGeometry(500, 320, 300, 30)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.change_volume)

        # Playlist
        self.playlist = QListWidget(self)
        self.playlist.setGeometry(500, 20, 300, 300)
        self.playlist.setStyleSheet("background-color: transparent; border: 1px solid #7E9D9E; color:#FFEE58;")

        # Background image
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(500, 20, 300, 300)
        self.bg_label.setPixmap(QPixmap("icons_music_note.jpg"))
        self.bg_label.setScaledContents(True)
        self.bg_label.lower()

    def create_toggle_button(self, text, icon_path, x, y):
        button = QPushButton(self)
        button.setGeometry(x, y, 90, 100)
        button.setCheckable(True)
        button.setStyleSheet("""
            QPushButton {
                background-color: #1B3435;
                color: #1B3435;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #3A4F4F;
            }
            QPushButton:checked {
                background-color: #ED6C02;
                border: 2px solid #FFD700;
            }
        """)

        layout = QVBoxLayout(button)
        button.setLayout(layout)

        label = QLabel(text, button)
        label.setStyleSheet("color: #7E9D9E;")
        label.setAlignment(Qt.AlignCenter)

        icon_label = QLabel(button)
        icon_label.setPixmap(QIcon(icon_path).pixmap(QSize(50, 50)))
        icon_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)
        layout.addWidget(icon_label)

        return button

    def update_clock(self):
        current_time = QTime.currentTime().toString('HH:mm:ss')
        self.clock_display.display(current_time)

    def add_mp3_to_playlist(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select MP3 Files", "", "MP3 Files (*.mp3)")
        for file in files:
            self.playlist.addItem(file)

    def toggle_play(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.play_button.setText(" ")
        else:
            if self.playlist.selectedItems():
                track = self.playlist.selectedItems()[0].text()
                pygame.mixer.music.load(track)
                pygame.mixer.music.play()
                self.is_playing = True
                self.play_button.setText(" ")

    def toggle_repeat(self):
        self.is_repeating = not self.is_repeating

    def change_volume(self):
        volume = self.volume_slider.value() / 100
        pygame.mixer.music.set_volume(volume)

    def get_weather(self, city_name):
        params = {"q": city_name, "appid": API_KEY, "units": "metric"}
        try:
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                temp = data["main"]["temp"]
                weather = data["weather"][0]["description"]
                
                # Update weather display
                pixmap = QPixmap("cloudy.png")
                self.weather_icon.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
                self.city_label.setText(f"Weather in {city_name}")
                self.result_label.setText(f"🌡 {temp}°C | {weather.capitalize()}")
            else:
                self.result_label.setText("❌ Failed to fetch weather.")
        except Exception as e:
            self.result_label.setText("❌ Error fetching weather data")

    def on_city_selected(self):
        selected_city = self.city_combo.currentText()
        self.get_weather(selected_city)

    def open_sub_window3(self):
        self.sub_window3 = SubWindow3()
        self.sub_window3.show()
        self.close()

    def back_to_main(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_Q:
            self.close()
        else:
            super().keyPressEvent(event)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()