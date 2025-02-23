# Embedded Linux ODC Project

This project is a user interface system designed for the Raspberry Pi, allowing users to interact with various modules such as Smart Home, Smart TV, and Car Infotainment. The system is built using Python and PyQt5 for the graphical interface, and it integrates with external APIs and hardware for functionality.
We have successfully integrated the application with the Raspberry Pi. Once the Raspberry Pi is powered on, the application automatically launches. Additionally, a customized logo appears during the booting process, providing a personalized touch to the system.

---

## Features

### 1. **Main Menu**
   - **Smart Home Module**: Control home appliances, view weather, and play music.
   - **Smart TV Module**: Stream live TV channels using YouTube links.
   - **Car Infotainment Module**: Manage car systems like lights, GPS, and reverse camera with lane detection.

### 2. **Smart Home Module**
   - **Weather Display**: Fetches and displays weather information for selected cities.
   - **Music Player**: Play, pause, and repeat MP3 files.
   - **Room Control**: Control lights and appliances in different rooms using MQTT.

### 3. **Smart TV Module**
   - **Live TV Channels**: Stream live TV channels using YouTube links.
   - **Channel Switching**: Easily switch between predefined channels.

### 4. **Car Infotainment Module**
   - **Reverse Camera**: Displays a live feed from the car's reverse camera with lane detection.
   - **GPS Navigation**: Integrates with Google Maps for navigation.
   - **Voice Control**: Control lights, GPS, and camera using voice commands.
   - **Lane Detection**: Guides the driver while reversing with dynamic guidelines.

---

## Setup Instructions

### Prerequisites
- Raspberry Pi with Raspbian OS.
- Python 3.x installed.
- Required Python libraries: `PyQt5`, `pygame`, `vlc`, `yt-dlp`, `paho-mqtt`, `opencv-python`, `speechrecognition`.

### Requirements
- 1024x600 display resolution

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/AmalAliEg/Embedded_Linux_ODC.git
   cd Embedded_Linux_ODC

2. Install the required Python libraries:
    ```python 
    pip install -r requirements.txt
3. Set up the Raspberry Pi:
    - Ensure the camera module is connected and enabled.
    - Configure the MQTT broker settings in the RoomsScreen.py file if needed.
4. Run the application:
    ```python 
    python MainScreen.py

## Future Work
- Integration with Yocto/Buildroot: 
        Replace Raspbian with a custom Linux distribution built using Yocto or Buildroot for better optimization and customization.

- Enhanced Voice Control: 
        Add more voice commands and improve speech recognition accuracy.

- IoT Integration: 
        Expand the Smart Home module to support more IoT devices and protocols.

-Advanced Lane Detection: 
        Improve the lane detection algorithm for better accuracy and reliability.
## Project Structure
- main.py: Entry point of the application.
- HomeScreen.py: Implements the Smart Home module.
- TvScreen.py: Implements the Smart TV module.
- CarScreen.py: Implements the Car Infotainment module.
- RoomsScreen.py: Handles room-specific controls using MQTT.
- utils.py: Utility functions for path managment.

## Contributors
1. Amal Ali
2. Huda Hussam
3. Mai El-shaheed

## Acknowledgments
    - **Huge thanks to Eng. Eslam Hefny** for his unwavering support, effort, time, and dedication to teaching us throughout this course. His guidance has been invaluable in helping us navigate complex topics and grow as developers.

    - **Special thanks to both Amit and Orange** for providing this incredible opportunity to skill up in Linux and embedded systems. This experience allowed us to dive into challenging topics and expand our knowledge in ways we never thought possible.

    We are grateful for the chance to work on this project, which has been a significant milestone in our learning journey. We hope this is just the first step toward many more achievements in our careers.