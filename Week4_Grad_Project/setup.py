from setuptools import setup

setup(
    name='SmartProject',
    version='1.0',
    packages=[''],
    install_requires=[
        'PyQt5',
        'opencv-python',
        'python-vlc',
        'yt-dlp',
        'SpeechRecognition',
        'PyQtWebEngine',
        'paho-mqtt',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'smartproject=MainScreen:main',
        ],
    }
)