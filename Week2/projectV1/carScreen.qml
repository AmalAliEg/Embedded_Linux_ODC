import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.15
// Uncomment if using QtLocation for a real map integration
// import QtLocation 5.6
// import QtPositioning 5.6

Window {
    id: mainWindow
    width: 800
    height: 480
    visible: true
    title: "Multi-Functional Touchscreen Hub"

    // Current active screen index: 0-Car, 1-Home, 2-Entertainment
    property int currentScreen: 0

    Rectangle {
        anchors.fill: parent
        color: "#20232a"

        // Side navigation panel
        Column {
            id: navPanel
            spacing: 10
            width: 120
            anchors {
                left: parent.left
                top: parent.top
                bottom: parent.bottom
                margins: 10
            }
            Repeater {
                model: ["Car", "Home", "Entertainment"]
                delegate: Button {
                    text: modelData
                    checkable: true
                    checked: (index === mainWindow.currentScreen)
                    onClicked: mainWindow.currentScreen = index
                    background: Rectangle {
                        radius: 5
                        color: control.checked ? "#61dafb" : "#3a3f47"
                    }
                }
            }
        }

        // Main content area with animated transitions between screens
        StackView {
            id: stackView
            anchors {
                top: parent.top
                bottom: parent.bottom
                left: navPanel.right
                right: parent.right
                margins: 10
            }
            initialItem: carScreen

            // Define transitions for smooth animated screen changes
            transitions: Transition {
                NumberAnimation { properties: "x"; duration: 300; easing.type: Easing.InOutQuad }
                FadeTransition { duration: 300 }
            }
        }
    }

    // Component for Car Screen
    Component {
        id: carScreen
        Rectangle {
            id: carPage
            color: "#282c34"
            anchors.fill: parent
            radius: 10

            // Header with title and simulated voice command buttons
            Column {
                spacing: 10
                anchors.top: parent.top
                anchors.horizontalCenter: parent.horizontalCenter
                padding: 20

                Text {
                    text: "Car Dashboard"
                    font.pointSize: 28
                    color: "#ffffff"
                }

                Row {
                    spacing: 10
                    Button {
                        text: "Car Light On"
                        onClicked: {
                            // Placeholder: Insert code to activate car light
                            console.log("Car light turned on")
                        }
                    }
                    Button {
                        text: "Car Light Off"
                        onClicked: {
                            // Placeholder: Insert code to deactivate car light
                            console.log("Car light turned off")
                        }
                    }
                    Button {
                        text: "Open GPS"
                        onClicked: {
                            // Placeholder: Insert code to open GPS
                            console.log("GPS opened")
                        }
                    }
                    Button {
                        text: "Close GPS"
                        onClicked: {
                            // Placeholder: Insert code to close GPS
                            console.log("GPS closed")
                        }
                    }
                }
            }

            // Display simulated car data with animations
            Row {
                spacing: 20
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter

                // Speed Gauge
                Column {
                    spacing: 5
                    Rectangle {
                        width: 100; height: 100; radius: 50
                        color: "#61dafb"
                        border.color: "#ffffff"
                        border.width: 2
                        Text {
                            anchors.centerIn: parent
                            text: speedDisplay.text
                            font.pointSize: 24
                            color: "#000000"
                        }
                        // Simulate an animated gauge needle using rotation animation
                        RotationAnimator on rotation {
                            from: 0
                            to: 360 * (parseInt(speedDisplay.text) / 240)  // assuming max speed 240 km/h
                            duration: 1000
                        }
                    }
                    Text {
                        id: speedDisplay
                        text: "80"  // simulated speed value
                        font.pointSize: 18
                        color: "#ffffff"
                        horizontalAlignment: Text.AlignHCenter
                    }
                    Text {
                        text: "Speed (km/h)"
                        font.pointSize: 14
                        color: "#bbbbbb"
                        horizontalAlignment: Text.AlignHCenter
                    }
                }

                // RPM Gauge
                Column {
                    spacing: 5
                    Rectangle {
                        width: 100; height: 100; radius: 50
                        color: "#98c379"
                        border.color: "#ffffff"
                        border.width: 2
                        Text {
                            anchors.centerIn: parent
                            text: rpmDisplay.text
                            font.pointSize: 24
                            color: "#000000"
                        }
                        RotationAnimator on rotation {
                            from: 0
                            to: 360 * (parseInt(rpmDisplay.text) / 8000)  // assuming max RPM 8000
                            duration: 1000
                        }
                    }
                    Text {
                        id: rpmDisplay
                        text: "3500"  // simulated RPM value
                        font.pointSize: 18
                        color: "#ffffff"
                        horizontalAlignment: Text.AlignHCenter
                    }
                    Text {
                        text: "RPM"
                        font.pointSize: 14
                        color: "#bbbbbb"
                        horizontalAlignment: Text.AlignHCenter
                    }
                }

                // Fuel Level Gauge
                Column {
                    spacing: 5
                    Rectangle {
                        width: 100; height: 100; radius: 50
                        color: "#e5c07b"
                        border.color: "#ffffff"
                        border.width: 2
                        Text {
                            anchors.centerIn: parent
                            text: fuelDisplay.text
                            font.pointSize: 24
                            color: "#000000"
                        }
                        RotationAnimator on rotation {
                            from: 0
                            to: 360 * (parseInt(fuelDisplay.text) / 100)  // assuming fuel level in percentage
                            duration: 1000
                        }
                    }
                    Text {
                        id: fuelDisplay
                        text: "55"  // simulated fuel level (%)
                        font.pointSize: 18
                        color: "#ffffff"
                        horizontalAlignment: Text.AlignHCenter
                    }
                    Text {
                        text: "Fuel (%)"
                        font.pointSize: 14
                        color: "#bbbbbb"
                        horizontalAlignment: Text.AlignHCenter
                    }
                }
            }

            // Navigation Map (placeholder)
            Rectangle {
                id: mapPlaceholder
                width: parent.width * 0.8
                height: 150
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 20
                color: "#3e4451"
                radius: 10
                border.color: "#ffffff"
                border.width: 1

                Text {
                    anchors.centerIn: parent
                    text: "Navigation Map (GPS Data)"
                    font.pointSize: 16
                    color: "#ffffff"
                }
                // To integrate an actual map, consider using the QtLocation module.
            }
        }
    }

    // Component for Home Screen (Smart Home Control)
    Component {
        id: homeScreen
        Rectangle {
            color: "#282c34"
            anchors.fill: parent
            radius: 10

            Column {
                anchors.centerIn: parent
                spacing: 20
                Text {
                    text: "Smart Home Control"
                    font.pointSize: 28
                    color: "#ffffff"
                }
                // Add smart home control elements as needed
                Button {
                    text: "Toggle Lights"
                    onClicked: console.log("Smart home lights toggled")
                }
                Button {
                    text: "Set Thermostat"
                    onClicked: console.log("Thermostat settings opened")
                }
            }
        }
    }

    // Component for Entertainment Screen (Smart TV interface)
    Component {
        id: entertainmentScreen
        Rectangle {
            color: "#282c34"
            anchors.fill: parent
            radius: 10

            Column {
                anchors.centerIn: parent
                spacing: 20
                Text {
                    text: "Smart TV Entertainment"
                    font.pointSize: 28
                    color: "#ffffff"
                }
                // Add TV control elements as needed
                Button {
                    text: "Play Movie"
                    onClicked: console.log("Movie started")
                }
                Button {
                    text: "Open Streaming App"
                    onClicked: console.log("Streaming app opened")
                }
            }
        }
    }

    // Change StackView content when the navigation selection changes
    onCurrentScreenChanged: {
        if (currentScreen === 0)
            stackView.replace(carScreen)
        else if (currentScreen === 1)
            stackView.replace(homeScreen)
        else if (currentScreen === 2)
            stackView.replace(entertainmentScreen)
    }
}
