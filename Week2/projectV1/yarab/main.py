import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
import folium
import io

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Load the UI file
        uic.loadUi('CarScreenNew.ui', self)
        
        # Find the map view widget
        self.mapView = self.findChild(QWebEngineView, 'mapView')
        
        # Initialize and display the map
        self.initialize_map()
        
    def initialize_map(self):
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
        
        # Save map to data string
        data = io.BytesIO()
        m.save(data, close_file=False)
        
        # Display the map in QWebEngineView
        self.mapView.setHtml(data.getvalue().decode())

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())