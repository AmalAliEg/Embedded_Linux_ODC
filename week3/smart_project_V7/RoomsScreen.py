import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,QVBoxLayout, QLabel, QMessageBox, QWidget  ,QListWidget      

from PyQt5.QtGui import QIcon, QPalette, QColor,QDesktopServices
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtBluetooth import QBluetoothDeviceDiscoveryAgent, QBluetoothSocket, QBluetoothUuid,QBluetoothAddress,QBluetoothServiceInfo




import HomeScreen


# --------------------- Room Home ---------------------
class RoomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, 1024, 600)
        self.setStyleSheet("background-color: #001819;")

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


#----------------------bluetooth_button-------------------------------------
  #Back button home
        layout = QVBoxLayout()
        
               

        
         # زر البلوتوث
        self.bluetooth_button = QPushButton( )
        
        self.bluetooth_button.setStyleSheet("background-color: transparent;  color : #7E9D9E;")
        self.bluetooth_button = self.create_toggle_button("Bluetooth", "bluetooth.png", 20, 130)
        self.bluetooth_button.clicked.connect(self.toggle_devices_list)



        # قائمة عرض الأجهزة المتاحة
        self.devices_list = QListWidget(self)
        self.devices_list.setStyleSheet("background-color: #002B36; color: #7E9D9E; border: 1px solid #7E9D9E;")
        self.devices_list.setGeometry(20, 240, 300, 200)  # (x, y, العرض, الارتفاع)
        self.devices_list.setVisible(False)  # تبدأ مخفية
        self.devices_list.itemClicked.connect(self.connect_to_device)
      

        # إعداد البحث عن البلوتوث
        self.discovery_agent = QBluetoothDeviceDiscoveryAgent()
        self.discovery_agent.deviceDiscovered.connect(self.add_device)
         # إعداد البحث عن البلوتوث
        self.discovery_agent = QBluetoothDeviceDiscoveryAgent()
        self.discovery_agent.setInquiryType(QBluetoothDeviceDiscoveryAgent.GeneralUnlimitedInquiry)  # ← أضف هذا السطر بعد إنشاء discovery_agent
        self.discovery_agent.deviceDiscovered.connect(self.add_device)

        # مقبس البلوتوث للاتصال بالجهاز
       
        self.socket = QBluetoothSocket(QBluetoothServiceInfo.RfcommProtocol)



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



#--------------------------bluetooth-----------------------------------

       

    
    def toggle_devices_list(self):
        """إظهار أو إخفاء قائمة الأجهزة عند الضغط على الزر"""
        if self.devices_list.isVisible():
            self.devices_list.setVisible(False)
        else:
            self.devices_list.clear()  # تفريغ القائمة قبل البحث
            self.devices_list.setVisible(True)  # إظهار القائمة
            self.discovery_agent.stop()  # إيقاف أي بحث قديم
            self.discovery_agent.start()  # بدء البحث عن أجهزة البلوتوث
            QMessageBox.information(self, "Bluetooth", "Searching for Bluetooth devices...")

    def add_device(self, device):
        """إضافة الجهاز إلى القائمة فقط إذا كان يحتوي على اسم معروف"""
        device_name = device.name()
        device_address = device.address().toString()

        # تجنب إضافة أجهزة مكررة
        for index in range(self.devices_list.count()):
            if device_address in self.devices_list.item(index).text():
                return  # الجهاز موجود بالفعل، لا تضف مرة أخرى

        # عرض فقط الأجهزة التي تحتوي على اسم (تجنب الأجهزة غير المعروفة)
        if device_name and "Unknown" not in device_name:
            self.devices_list.addItem(f"{device_name} - {device_address}")

    def connect_to_device(self, item):
        """الاتصال بجهاز بلوتوث معين"""
        device_info = item.text().split(" - ")
        device_address = device_info[1]
        #self.socket = QBluetoothSocket(QBluetoothServiceInfo.RfcommProtocol)

        self.socket = QBluetoothSocket(QBluetoothServiceInfo.L2capProtocol)

        self.socket.error.connect(self.handle_bluetooth_error)


        # الإشارات
        self.socket.connected.connect(self.on_connected)
        self.socket.disconnected.connect(self.on_disconnected)

        print(f"🔄 Trying to connect to: {device_info[0]} - {device_address}") 

        # محاولة الاتصال
        self.socket.connectToService(QBluetoothAddress(device_address), QBluetoothUuid(QBluetoothUuid.Rfcomm))

    def handle_bluetooth_error(self, error):
        """التعامل مع الأخطاء أثناء الاتصال"""
        QMessageBox.critical(self, "Bluetooth Error", f"Error Code: {error}")
        print(f"❌ Bluetooth Error: {error}")
        
       

    def on_connected(self):
        """تنفيذ عند نجاح الاتصال"""
        print("✅ Bluetooth Connected Successfully!")
        QMessageBox.information(self, "Bluetooth", "Connected successfully!")

    def on_disconnected(self):
        """تنفيذ عند قطع الاتصال"""
        print("🔌 Bluetooth Disconnected")
        QMessageBox.warning(self, "Bluetooth", "Disconnected from device!")
    # def connect_to_device(self, item):
    #     try:
    #         device_info = item.text().split(" - ")
    #         device_address = device_info[1]
            
    #         # طباعة معلومات الجهاز للتأكد من القيم
    #         print(f"Trying to connect to: {device_info[0]} - {device_address}")

    #         # إنشاء مقبس بلوتوث جديد عند كل اتصال
    #         self.socket = QBluetoothSocket(QBluetoothServiceInfo.RfcommProtocol)
    #         self.socket.error.connect(self.handle_bluetooth_error)  # مراقبة الأخطاء
    #         self.socket.connected.connect(self.on_connected)  # التأكد من نجاح الاتصال
    #         self.socket.disconnected.connect(self.on_disconnected)  # مراقبة الفصل
            
    #         self.socket.connectToService(QBluetoothAddress(device_address), QBluetoothUuid(QBluetoothUuid.Rfcomm))


    #     except Exception as e:
    #         print(f"Bluetooth connection failed: {e}")
    #         QMessageBox.critical(self, "Bluetooth Error", f"Failed to connect: {e}")

    #     self.devices_list.setVisible(False)  # إخفاء القائمة بعد الاختيار


   

   


   
#Back button home
    def back_to_home(self):
        self.main_window = HomeScreen.HomeWindow()
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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoomWindow()
    window.show()
    sys.exit(app.exec_())




