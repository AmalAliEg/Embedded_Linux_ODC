import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
import folium
import os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Control Hub")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and main layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QHBoxLayout(central_widget)
        
        # Create left panel
        left_panel = QtWidgets.QFrame()
        left_panel.setMaximumWidth(400)
        left_panel.setStyleSheet("QFrame { background-color: #2c3e50; border-radius: 15px; padding: 10px; }")
        left_layout = QtWidgets.QVBoxLayout(left_panel)
        
        # Create date and day labels
        self.dateLabel = QtWidgets.QLabel("Date:")
        self.dayLabel = QtWidgets.QLabel("Day:")
        
        # Style the labels
        label_style = "color: white; font-size: 16px;"
        self.dateLabel.setStyleSheet(label_style)
        self.dayLabel.setStyleSheet(label_style)
        
        # Add labels to left panel
        left_layout.addWidget(self.dateLabel)
        left_layout.addWidget(self.dayLabel)
        
        # Create right panel for map
        right_panel = QtWidgets.QFrame()
        right_panel.setStyleSheet("QFrame { background-color: #2c3e50; border-radius: 15px; padding: 10px; }")
        right_layout = QtWidgets.QVBoxLayout(right_panel)
        
        # Create map view
        self.mapView = QWebEngineView()
        right_layout.addWidget(self.mapView)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        
        # Initialize map
        self.initialize_map()
        
    def initialize_map(self):
        try:
            # Create a map centered at Cairo
            m = folium.Map(
                location=[30.0444, 31.2357],  # Cairo coordinates
                zoom_start=13,
                tiles='OpenStreetMap'
            )
            
            # Add a marker for current location
            folium.Marker(
                [30.0444, 31.2357],
                popup='Current Location',
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
            
            # Save map to a temporary HTML file
            temp_file = 'temp_map.html'
            m.save(temp_file)
            
            # Load the HTML file in QWebEngineView
            self.mapView.setUrl(QUrl.fromLocalFile(os.path.abspath(temp_file)))
            
        except Exception as e:
            print(f"Error initializing map: {e}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())