import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import QTimer, Qt
from datetime import datetime

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Create central widget and layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)
        
        # Create labels with alignment
        self.dateLabel = QtWidgets.QLabel()
        self.dayLabel = QtWidgets.QLabel()
        
        # Set alignment and style
        self.dateLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dayLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add labels to layout
        layout.addWidget(self.dateLabel)
        layout.addWidget(self.dayLabel)
        
        # Set window properties
        self.setWindowTitle("Smart Control Hub")
        self.setGeometry(100, 100, 400, 200)
        
        # Update time immediately
        self.update_datetime()
        
        # Set up timer after UI is created
        QTimer.singleShot(0, self.setup_timer)
        
    def setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)
        
    def update_datetime(self):
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        day_str = now.strftime("%A")
        
        self.dateLabel.setText(f"Date: {date_str}")
        self.dayLabel.setText(f"Day: {day_str}")

def main():
    # Create application
    app = QtWidgets.QApplication(sys.argv)
    
    # Create and show window
    window = MainWindow()
    window.show()
    
    # Start event loop
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())