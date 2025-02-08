import sys
import vlc
import yt_dlp
import pygame
import requests
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,QWidget, QVBoxLayout, QLabel, QLCDNumber, QListWidget, QFileDialog, QSlider,QComboBox,QFrame,QHBoxLayout
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer, QTime, QSize, QThread, pyqtSignal, QDateTime, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import speech_recognition as sr

# تفاصيل API الطقس
API_KEY = "9b461f6d62d59555b0471ff99ca0c782"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"



# --------------------- Main Window ---------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Merget System for User Interface using Raspberry Pi.")
        self.setGeometry(0, 0, 900, 550)
        self.setWindowIcon(QIcon("icons_home.png"))
        #self.setStyleSheet("background-color: #1B3435;")


        # تعيين لون الخلفية
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#001819"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # زر Home لفتح نافذة Smart Home
        self.open_button = QPushButton(self)
        self.open_button.setIcon(QIcon("iconsr_home.png"))
        self.open_button.setIconSize(QSize(250, 150))
        self.open_button.setGeometry(130, 160, 150, 150)
        self.open_button.setStyleSheet("background-color: transparent; border: none;")
        self.open_button.clicked.connect(self.open_sub_window)

        # زر TV لفتح نافذة Smart TV
        self.open_buttontv = QPushButton(self)
        self.open_buttontv.setIcon(QIcon("icons_tv.png"))
        self.open_buttontv.setIconSize(QSize(150, 150))
        self.open_buttontv.setGeometry(370, 180, 150, 150)
        self.open_buttontv.setStyleSheet("background-color: transparent; border: none;")
        self.open_buttontv.clicked.connect(self.open_sub_window2)


        # زر  لفتح نافذة car
        self.open_buttontv = QPushButton(self)
        self.open_buttontv.setIcon(QIcon("car.png"))
        self.open_buttontv.setIconSize(QSize(150, 150))
        self.open_buttontv.setGeometry(589, 180, 150, 150)
        self.open_buttontv.setStyleSheet("background-color: transparent; border: none;")
        self.open_buttontv.clicked.connect(self.open_sub_window4)


    def open_sub_window(self):
        self.sub_window = SubWindow()
        self.sub_window.show()
        self.close()

    def open_sub_window2(self):
        self.sub_window2 = TVWindow()
        self.sub_window2.show()
        self.close()

    def open_sub_window4(self):
        self.sub_window2 = SmartControlHub()
        self.sub_window2.show()
        self.close()


    


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)



    # الحدث لإغلاق النافذة عند الضغط على زر من الكيبورد
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:  # عند الضغط على زر Esc
            self.close()                 # إغلاق النافذة
        elif event.key() == Qt.Key_Q:    # عند الضغط على زر Q
            self.close()                 # إغلاق النافذة أيضًا
        else:
            super().keyPressEvent(event)  # تنفيذ الحدث الافتراضي

# --------------------- Smart Home Window ---------------------
class SubWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("My Smart Home")
        self.setGeometry(0, 0, 900, 550)
        #self.setStyleSheet("background-color: #001819;")


        # تعيين لون الخلفية
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#001819"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # شاشة عرض الساعة الرقمية
        self.clock_display = QLCDNumber(self)
        self.clock_display.setGeometry(20, 20, 320, 120)
        self.clock_display.setStyleSheet("color: #7E9D9E; background: #1B3435; border: 2px solid #7E9D9E;")
        self.clock_display.setDigitCount(8)

        timer = QTimer(self)
        timer.timeout.connect(self.update_clock)
        timer.start(1000)
        self.update_clock()





        
                # **إضافة قائمة منسدلة لاختيار المدينة**
        self.city_combo = QComboBox(self)
        self.city_combo.addItem("Cairo")
        self.city_combo.addItem("German")
        self.city_combo.addItem("Saudi Arabia")
        self.city_combo.addItem("New York")
        self.city_combo.addItem("London")
        self.city_combo.addItem("Tokyo")
        self.city_combo.addItem("Paris")
        self.city_combo.setStyleSheet("""
            background-color: #1B3435;
            color: #7E9D9E;
            font-size: 18px;
            border-radius: 5px;
            padding: 5px;
        """)
        self.city_combo.currentIndexChanged.connect(self.on_city_selected)

        # تحديد مكان وحجم QComboBox باستخدام setGeometry
        self.city_combo.setGeometry(20, 200, 320, 40)  # (x, y, العرض, الارتفاع)

        # **🌤 عرض الطقس**
        self.city_label = QLabel("Weather in Cairo", self)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_label.setFont(QFont("Arial", 12))
        self.city_label.setStyleSheet("color: #7E9D9E;")
        self.city_label.setGeometry(70, 200, 350, 350)

        # مساحة ثابتة لعرض الطقس
        self.weather_display = QLabel(self)
        self.weather_display.setGeometry(20, 245, 390, 300)
        self.weather_display.setStyleSheet("""
            #background-color: #1B3435;
            border: 2px solid #7E9D9E;
            color: #FFD700;
        """)

        # عرض أيقونة الطقس
        self.weather_icon = QLabel(self.weather_display)
        self.weather_icon.setAlignment(Qt.AlignCenter)
        self.weather_icon.setFixedSize(150, 150)
        self.weather_icon.setStyleSheet("background: transparent;")

        # عرض درجة الحرارة
        self.result_label = QLabel("Fetching weather...", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.result_label.setStyleSheet("color: #FFD700;")
        self.result_label.setGeometry(20, 400, 300, 40)

        # تحديث الطقس عند بدء التشغيل
        self.get_weather("Cairo")
        weather_timer = QTimer(self)
        weather_timer.timeout.connect(lambda: self.get_weather(self.city_combo.currentText()))
        weather_timer.start(1800000)  # تحديث كل 30 دقيقة




        # إعداد pygame لتشغيل الصوتيات
        pygame.mixer.init()
        self.is_playing = False
        self.is_repeating = False

        # زر إضافة ملفات MP3
        self.add_button = self.create_toggle_button("Add", "icons_headphones.png", 800, 20)
        self.add_button.clicked.connect(self.add_mp3_to_playlist)

        # زر تشغيل/إيقاف الموسيقى
        self.play_button = self.create_toggle_button("Play", "icons_speaker.png", 800, 120)
        self.play_button.clicked.connect(self.toggle_play)

        # زر تكرار الموسيقى
        self.repeat_button = self.create_toggle_button("Repeat", "icons_repeat.png", 800, 220)
        self.repeat_button.clicked.connect(self.toggle_repeat)

      
        self.home_button = self.create_toggle_button("Home", "icons_house.png", 800, 320)
        self.home_button.clicked.connect(self.open_sub_window3)

        # زر العودة إلى النافذة الرئيسية

        self.back_button = self.create_toggle_button("Back", "icons_back.png", 800, 420)
        self.back_button.clicked.connect(self.back_to_main)


        # شريط مستوى الصوت
        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setGeometry(500, 320, 300, 30)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.change_volume)

        # قائمة تشغيل MP3
        self.playlist = QListWidget(self)
        self.playlist.setGeometry(500, 20, 300, 300)
        self.playlist.setStyleSheet("background-color: transparent; border: 1px solid #7E9D9E; color:#FFEE58;")



         # تعيين صورة كخلفية
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(500, 20, 300, 300)
        self.bg_label.setPixmap(QPixmap("icons_music_note.jpg"))
        self.bg_label.setScaledContents(True)
        self.bg_label.lower()

        
        # إعداد pygame
        pygame.mixer.init()
        self.is_playing = False
        self.is_repeating = False
        self.current_track = None

     

    def create_toggle_button(self, text, icon_path, x, y):
        """ إنشاء زر بتصميم Toggle """
        button = QPushButton(self)
        button.setGeometry(x, y, 90, 100)
        button.setCheckable(True)  # لجعل الزر قابل للتبديل
        button.setStyleSheet("""
            QPushButton {
                background-color: #1B3435;
                color: #1B3435;
                text-align: center;
            }
            
                             
            QPushButton:hover {
                background-color: #3A4F4F;  /* تأثير عند تمرير الماوس */
            }
            QPushButton:checked {
                background-color: #ED6C02;  /* تغيير لون الخلفية عند الضغط */
                
                border: 2px solid #FFD700;  /* تغيير لون الإطار عند الضغط */
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


    
    # دالة تحديث الطقس
    def on_city_selected(self):
        """Update weather when selecting a new city"""
        selected_city = self.city_combo.currentText()
        self.get_weather(selected_city)

    def get_weather(self, city_name):
        """Get and display weather data"""
        params = {"q": city_name, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            icon_code = data["weather"][0]["icon"]

            # # جلب أيقونة الطقس
            # pixmap = QPixmap(f"http://openweathermap.org/img/wn/{icon_code}@2x.png")  # استخدم URL للأيقونة
            # self.weather_icon.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))

            pixmap = QPixmap("cloudy.png")  # ضع مسار الصورة هنا
            self.weather_icon.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))

            # تحديث النصوص
            self.city_label.setText(f"Weather in {city_name}")
            self.result_label.setText(f"🌡 {temp}°C | {weather.capitalize()}")
        else:
            self.result_label.setText("❌ Failed to fetch weather.")


    #Control screen movement with mouse

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
#Exit page and go home page
    def back_to_main(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def open_sub_window3(self):
        self.sub_window3 = SubWindow3()
        self.sub_window3.show()
        self.close()

    # الحدث لإغلاق النافذة عند الضغط على زر من الكيبورد
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:  # عند الضغط على زر Esc
            self.close()                 # إغلاق النافذة
        elif event.key() == Qt.Key_Q:    # عند الضغط على زر Q
            self.close()                 # إغلاق النافذة أيضًا
        else:
            super().keyPressEvent(event)  # تنفيذ الحدث الافتراضي



# --------------------- room home ---------------------
class SubWindow3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, 900, 550)
        self.setStyleSheet("background-color: #001819;")

      


        #   # زر إضافة ملفات MP3
        # self.add_button = self.create_toggle_button("Add", "icons_headphones.png", 800, 20)
        # self.add_button.clicked.connect(self.add_mp3_to_playlist)

        #Back button home
        self.Home_button = self.create_toggle_button("Home", "icons_back.png", 20, 20)
        self.Home_button.clicked.connect(self.back_to_home)
#---------------------------family----------------------------------

        self.Family_button = QPushButton("Family", self)
        self.Family_button.setGeometry(120, 20, 90, 100)
        self.Family_button.setStyleSheet("background-color: transparent;  color : #7E9D9E; ")
        self.Floor_button = self.create_toggle_button("Floor", "icons_led.png", 220, 20)
        self.dining_room_button = self.create_toggle_button("dining room", "icons_dining_room.png", 320, 20)
        self.kitchen_button = self.create_toggle_button("kitchen", "icons-kitchen.png", 420, 20)
       

#---------------------------master----------------------------------


        self.master_button = QPushButton("Master", self)
        self.master_button.setGeometry(120, 130, 90, 100)
        self.master_button.setStyleSheet("background-color: transparent;  color : #7E9D9E; ")
        self.Bedroom_button = self.create_toggle_button("Bedroom", "icons_bed.png", 220, 130)
        self.shower_button = self.create_toggle_button("shower", "icons_shower.png", 320, 130)
        self.Clothes_room_button = self.create_toggle_button("Clothes", "icons_womens.png", 420, 130)
        self.Fan_button = self.create_toggle_button("Fan", "icons_fan.png", 520, 130)



#---------------------------garage----------------------------------


        self.garage_button = QPushButton("Garage", self)
        self.garage_button.setGeometry(120, 240, 90, 100)
        self.garage_button.setStyleSheet("background-color: transparent;  color : #7E9D9E; ")
        self.garagdoor_button = self.create_toggle_button("Garage Door", "icons_garage.png", 220, 240)
        self.led_button = self.create_toggle_button("LED", "icons_light.png", 320, 240)
        self.Clothes_room_button = self.create_toggle_button("Door", "icons-door.png", 420, 240)

    

    def create_toggle_button(self, text, icon_path, x, y):
        """ إنشاء زر بتصميم Toggle """
        button = QPushButton(self)
        button.setGeometry(x, y, 90, 100)
        button.setCheckable(True)  # لجعل الزر قابل للتبديل
        button.setStyleSheet("""
            QPushButton {
                
                background-color: #1B3435;
                color: #1B3435;
                text-align: center;
                border:none;
                
            }
            
                             
            QPushButton:hover {
                background-color: #3A4F4F;  /* تأثير عند تمرير الماوس */

            }
            QPushButton:checked {
                background-color: #ED6C02;  /* تغيير لون الخلفية عند الضغط */
                
                border: 2px solid #FFD700;  /* تغيير لون الإطار عند الضغط */
            }
 

        """)
        layout = QVBoxLayout()
        
      
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(icon_path).pixmap(QSize(50, 50)))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("background: transparent;")  # إزالة الخلفية الغامقة

        # **إنشاء النص**
        label = QLabel(text)
        label.setStyleSheet("color: #7E9D9E; background: transparent;")
        label.setAlignment(Qt.AlignCenter)

       
        
        layout.addWidget(label) 
        layout.addWidget(icon_label)  


  
        button.setLayout(layout)

        return button



    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)

   
#Back button home
    def back_to_home(self):
        self.main_window = SubWindow()
        self.main_window.show()
        self.close()


    # الحدث لإغلاق النافذة عند الضغط على زر من الكيبورد
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:  # عند الضغط على زر Esc
            self.close()                 # إغلاق النافذة
        elif event.key() == Qt.Key_Q:    # عند الضغط على زر Q
            self.close()                 # إغلاق النافذة أيضًا
        else:
            super().keyPressEvent(event)  # تنفيذ الحدث الافتراضي



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
 

        self.back_button = QPushButton("Back", self)
        self.back_button.setGeometry(20, 500, 100, 40)
        self.back_button.clicked.connect(self.back_to_main)
     
       

        # Connect buttons
        self.lightsOnButton.clicked.connect(lambda: self.handle_lights("on"))
        self.lightsOffButton.clicked.connect(lambda: self.handle_lights("off"))
        self.gpsOnButton.clicked.connect(lambda: self.handle_gps("on"))
        self.gpsOffButton.clicked.connect(lambda: self.handle_gps("off"))
        


        # Initialize voice recognition
        self.setup_voice_recognition()

    def back_to_main(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

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

    def update_mic_status(self, is_listening):
        self.micButton.setStyleSheet(
            f"QPushButton#micButton {{ background-color: {'#ff9933' if is_listening else '#3498db'}; border-radius: 32px; }}"
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

    def closeEvent(self, event):
        self.voice_thread.stop()
        self.voice_thread.wait()
        self.timer.stop()
        event.accept()







# --------------------- Smart TV Window ---------------------

class TVWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("My Smart TV")
        self.setGeometry(0, 0, 900, 550)
        self.setStyleSheet("background-color: #001819;")

        # # زر العودة إلى النافذة الرئيسية
        # self.back_button = QPushButton("Back", self)
        # self.back_button.setGeometry(20, 500, 100, 40)
        # self.back_button.clicked.connect(self.back_to_main)
     
    #  def __init__(self):
    #     super().__init__()
    #     self.setWindowTitle("Smart TV")
    #     self.setGeometry(100, 100, 800, 600)

    #     # Set background color
    #     palette = QPalette()
    #     palette.setColor(QPalette.Window, QColor("#001819"))  # Dark theme
    #     self.setAutoFillBackground(True)
    #     self.setPalette(palette)

        # VLC instance
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()

        # Main widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
    
        # Video frame
        self.video_frame = QFrame(self)
        self.video_frame.setStyleSheet("background-color: black; border: 2px solid #7E9D9E;")
        self.video_frame.setFixedSize(800, 450)  # Video area

        # Title Label
        self.title_label = QLabel("Smart TV", self)
        self.title_label.setStyleSheet("color: #7E9D9E; font-size: 24px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignCenter)

        # Buttons layout
        button_layout = QHBoxLayout()

        # Channel buttons
        self.channel_buttons = []
        self.video_links = [
            "https://www.youtube.com/watch?v=bNyUyrR0PHo",  # Channel 1
            "https://www.youtube.com/watch?v=edd_JfhC7i4",  # Channel 2
            "https://www.youtube.com/watch?v=zq8xgqZxb0k",  # Channel 3
            "https://www.youtube.com/watch?v=0FBiyFpV__g",  # Channel 4
            "https://www.youtube.com/watch?v=x5MkVTvOViQ",  # Channel 5
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
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()


   

    # الحدث لإغلاق النافذة عند الضغط على زر من الكيبورد
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:  # عند الضغط على زر Esc
            self.close()                 # إغلاق النافذة
        elif event.key() == Qt.Key_Q:    # عند الضغط على زر Q
            self.close()                 # إغلاق النافذة أيضًا
        else:
            super().keyPressEvent(event)  # تنفيذ الحدث الافتراضي






# --------------------- Smart TV Window ---------------------
class SubWindow4(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.setGeometry(0, 0, 900, 550)
        self.setStyleSheet("background-color: #001819;")

        # زر العودة إلى النافذة الرئيسية
        self.back_button = QPushButton("Back", self)
        self.back_button.setGeometry(20, 50, 100, 40)
        self.back_button.clicked.connect(self.back_to_main)





    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)

    def back_to_main(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()


   

    # الحدث لإغلاق النافذة عند الضغط على زر من الكيبورد
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:  # عند الضغط على زر Esc
            self.close()                 # إغلاق النافذة
        elif event.key() == Qt.Key_Q:    # عند الضغط على زر Q
            self.close()                 # إغلاق النافذة أيضًا
        else:
            super().keyPressEvent(event)  # تنفيذ الحدث الافتراضي



# --------------------- Run Application ---------------------
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
