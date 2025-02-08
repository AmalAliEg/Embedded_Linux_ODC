import sys
from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


# Add this to main.py
from PySide6.QtCore import QObject, Slot

class CarController(QObject):
    @Slot()
    def toggleCarLight(self, state):
        print(f"Car light {'on' if state else 'off'}")
    
    @Slot()
    def toggleGPS(self, state):
        print(f"GPS {'opened' if state else 'closed'}")


def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    # Create and register car controller
    car_controller = CarController()
    engine.rootContext().setContextProperty("carController", car_controller)
    
    # Load QML file
    engine.load(QUrl.fromLocalFile("main.qml"))
    
    if not engine.rootObjects():
        sys.exit(-1)
        
    return app.exec()
    
