import os
import sys
import vlc
import yt_dlp
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QFrame, QMessageBox)
import MainScreen
from utils import resource_path

# Force X11 backend instead of Wayland
os.environ["QT_QPA_PLATFORM"] = "xcb"
# Reduce VLC verbosity
os.environ["VLC_VERBOSE"] = "-1"

class TVWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, 1024, 600)
        self.setStyleSheet("background-color: #001819;")

        # VLC instance with specific parameters
        vlc_args = [
            '--quiet',
            '--no-xlib',
            '--vout=any',
            '--file-caching=1000',
            '--network-caching=1000',
            '--video-filter=postproc'
        ]
        
        try:
            self.instance = vlc.Instance(vlc_args)
            self.media_player = self.instance.media_player_new()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to initialize VLC: {str(e)}")
            return

        # Create main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # Video frame
        self.video_frame = QFrame()
        self.video_frame.setStyleSheet("background-color: black; border: 2px solid #7E9D9E;")
        self.video_frame.setFixedSize(1024, 450)  # Modified size
        self.main_layout.addWidget(self.video_frame)  # Add video frame to layout

        # Channel buttons
        self.button_layout = QHBoxLayout()
        self.channels = [
            ("icons/aljazeera.png", "https://www.youtube.com/watch?v=bNyUyrR0PHo"),
            ("icons/cartoon_network.png", "https://www.youtube.com/watch?v=zq8xgqZxb0k"),
            ("icons/dreamTrips.jpg", "https://www.youtube.com/watch?v=0FBiyFpV__g"),
            ("icons/national.png", "https://www.youtube.com/watch?v=x5MkVTvOViQ"),
            ("icons/CNC.png", "https://www.youtube.com/watch?v=rfDx1HMvXbQ"),
            ("icons/discovery.png", "https://www.youtube.com/watch?v=FlzMedKfQOs")
        ]

        for index, (icon, url) in enumerate(self.channels):
            button = self.create_channel_button(icon, index)
            self.button_layout.addWidget(button)
        
        self.main_layout.addLayout(self.button_layout)

        # Back button
        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon(resource_path("icons/icons_back.png")))
        self.back_button.setIconSize(QSize(100, 50))  # Increased icon size
        self.back_button.setFixedSize(100, 50)
        self.back_button.setStyleSheet("background-color: transparent; border: none; padding: 0px;")
        self.back_button.clicked.connect(self.back_to_main)
        self.main_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)  # Add back button to layout

        # Set up video output
        if sys.platform.startswith('linux'):
            self.media_player.set_xwindow(int(self.video_frame.winId()))
        else:
            self.media_player.set_hwnd(int(self.video_frame.winId()))

    def create_channel_button(self, icon_path, channel_index):
        button = QPushButton()
        button.setFixedSize(100, 100)  # Set button size
        button.setIcon(QIcon(resource_path(icon_path)))
        button.setIconSize(QSize(100, 100))  # Increased icon size
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0px;
            }
        """)
        button.clicked.connect(lambda: self.play_video(channel_index))
        return button

    def play_video(self, channel_index):
        try:
            # Stop current playback
            self.media_player.stop()
            
            youtube_url = self.channels[channel_index][1]
            
            # Configure yt-dlp
            ydl_opts = {
                'format': 'best[height<=720]',  # Limit resolution
                'quiet': True,
                'no_warnings': True
            }
            
            # Get direct URL
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=False)
                url = info['url']
            
            # Create and play media
            media = self.instance.media_new(url)
            media.add_option('network-caching=1000')
            media.add_option('clock-jitter=0')
            media.add_option('clock-synchro=0')
            
            self.media_player.set_media(media)
            self.media_player.video_set_scale(0)  # Auto scale
            self.media_player.audio_set_volume(70)
            self.media_player.play()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to play video: {str(e)}")

    def closeEvent(self, event):
        try:
            self.media_player.stop()
        except:
            pass
        event.accept()

    def back_to_main(self):
        try:
            self.media_player.stop()
        except:
            pass
        self.main_window = MainScreen.MainWindow()
        self.main_window.show()
        self.close()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Escape, Qt.Key_Q):
            self.close()
        else:
            super().keyPressEvent(event)

if __name__ == "__main__":
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create and show window
    try:
        window = TVWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Application error: {str(e)}")
        sys.exit(1)