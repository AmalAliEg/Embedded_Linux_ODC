import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLCDNumber, QComboBox, QPushButton, QSlider, QListWidget, QFileDialog, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QTime, QSize
from PyQt5.QtGui import QPalette, QColor, QFont, QPixmap, QIcon
import pygame.mixer
import requests
import RoomsScreen
import MainScreen
API_KEY = "9b461f6d62d59555b0471ff99ca0c782"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
# --------------------- Smart Home Window ---------------------
class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
       
        self.setGeometry(0, 0, 1024, 600)
        self.setStyleSheet("background-color: #001819;")


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
        self.city_combo.setGeometry(20, 250, 320, 40)  # (x, y, العرض, الارتفاع)

        # **🌤 عرض الطقس**
        self.city_label = QLabel("Weather in Cairo", self)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_label.setFont(QFont("Arial", 12))
        self.city_label.setStyleSheet("color: #7E9D9E;")
        self.city_label.setGeometry(70, 200, 350, 550)

        # مساحة ثابتة لعرض الطقس
        self.weather_display = QLabel(self)
        self.weather_display.setGeometry(20, 350, 390, 300)
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
        self.result_label.setGeometry(20, 500, 300, 40)

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
        self.add_button = self.create_toggle_button("Add", "icons_headphones.png", 900, 20)
        self.add_button.clicked.connect(self.add_mp3_to_playlist)

        # زر تشغيل/إيقاف الموسيقى
        self.play_button = self.create_toggle_button("Play", "icons_speaker.png", 900, 120)
        self.play_button.clicked.connect(self.toggle_play)

        # زر تكرار الموسيقى
        self.repeat_button = self.create_toggle_button("Repeat", "icons_repeat.png", 900, 220)
        self.repeat_button.clicked.connect(self.toggle_repeat)

      
        self.home_button = self.create_toggle_button("Home", "icons_house.png", 900, 320)
        self.home_button.clicked.connect(self.open_sub_window3)

        # زر العودة إلى النافذة الرئيسية

        self.back_button = self.create_toggle_button("Back", "icons_back.png", 900, 420)
        self.back_button.clicked.connect(self.back_to_main)


        # شريط مستوى الصوت
        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setGeometry(590, 320, 300, 30)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.change_volume)

        # قائمة تشغيل MP3
        self.playlist = QListWidget(self)
        self.playlist.setGeometry(590, 20, 300, 300)
        self.playlist.setStyleSheet("background-color: transparent; border: 1px solid #7E9D9E; color:#FFEE58;")



         # تعيين صورة كخلفية
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(590, 20, 300, 300)
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

            # # url cloud
            pixmap = QPixmap(f"http://openweathermap.org/img/wn/{icon_code}@2x.png")  # استخدم URL للأيقونة
            self.weather_icon.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))

            pixmap = QPixmap("cloudy.png")  # Put image path here
            self.weather_icon.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))

            # تحديث النصوص
            self.city_label.setText(f"Weather in {city_name}")
            self.result_label.setText(f"🌡 {temp}°C | {weather.capitalize()}")
        else:
            self.result_label.setText("❌ Failed to fetch weather.")


   
#Exit page and go home page
    def back_to_main(self):
        self.main_window = MainScreen.MainWindow()
        self.main_window.show()
        self.close()

    def open_sub_window3(self):
        self.sub_window3 = RoomsScreen.RoomWindow()
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




# Running the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec_())
