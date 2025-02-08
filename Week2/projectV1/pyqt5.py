import sys
import pygame
from PyQt5.QtWidgets import QApplication, QMainWindow, QLCDNumber, QPushButton, QListWidget, QFileDialog, QSlider, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt, QTimer, QTime, QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setWindowTitle("My Smart Home")
        self.setGeometry(0, 0, 900, 550)
        self.setWindowIcon(QIcon("icons_home.png"))

        # تعيين لون الخلفية
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("touch"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # شاشة عرض الساعة الرقمية
        self.clock_display = QLCDNumber(self)
        self.clock_display.setGeometry(20, 20, 320, 120)
        self.clock_display.setStyleSheet("color: #7E9D9E; background: #1B3435; border: 2px solid #7E9D9E;")
        self.clock_display.setDigitCount(8)

        # مؤقت لتحديث الساعة كل ثانية
        timer = QTimer(self)
        timer.timeout.connect(self.update_clock)
        timer.start(1000)
        self.update_clock()

        # إضافة الأزرار
        self.add_button = self.create_toggle_button("Add", "icons_headphones.png", 800, 20)
        self.add_button.clicked.connect(self.add_mp3_to_playlist)

        self.play_button = self.create_toggle_button("Play", "icons_speaker.png", 800, 120)
        self.play_button.clicked.connect(self.toggle_play)

        self.repeat_button = self.create_toggle_button("Repeat", "icons_repeat.png", 800, 220)
        self.repeat_button.clicked.connect(self.toggle_repeat)

        # شريط مستوى الصوت
        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setGeometry(500, 320, 300, 30)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.change_volume)

        # قائمة تشغيل MP3
        self.playlist = QListWidget(self)
        self.playlist.setGeometry(500, 20, 300, 300)
        self.playlist.setStyleSheet("background-color: transparent; border: 1px solid #7E9D9E;color:#FFEE58;")

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
        """إنشاء زر Toggle"""
        button = QPushButton(self)
        button.setGeometry(x, y, 90, 100)
        button.setCheckable(True)
        button.setStyleSheet("""
            QPushButton {
                background-color: #1B3435;
                color: #7E9D9E;
                text-align: center;
                border: 1px solid #7E9D9E;
            }
            QPushButton:checked {
                background-color: #3A4F4F;
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
            self.stop_playback()
        else:
            self.play_music()

    def play_music(self):
        if not self.playlist.selectedItems():
            return

        self.current_track = self.playlist.selectedItems()[0].text()

        try:
            pygame.mixer.music.load(self.current_track)
            pygame.mixer.music.play(loops=-1 if self.is_repeating else 0)
        except Exception as e:
            print(f"Error loading or playing music: {e}")
            return

        self.is_playing = True
        self.play_button.setText(" ")

    

    def stop_playback(self):
        """إيقاف التشغيل الحالي"""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.play_button.setText(" ")

    def toggle_repeat(self):
        """تبديل حالة التكرار"""
        self.is_repeating = not self.is_repeating

    def change_volume(self):
        """تغيير مستوى الصوت"""
        volume = self.volume_slider.value() / 100
        pygame.mixer.music.set_volume(volume)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
