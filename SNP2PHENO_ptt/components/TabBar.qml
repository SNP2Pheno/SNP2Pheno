import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    property color barColor: "transparent"

    width: parent.width
    height: parent.height
    color: barColor

    Rectangle {
        color: "transparent"
        width: parent.width
        height: parent.height

        RowLayout {
            anchors.fill: parent
            spacing: 2

            Tab {
                tabText: "Diseases"
            }
            Tab {
                tabText: "Appearance"
            }
            Tab {

            }

            Item {
                Layout.fillWidth: true
            }
        }
    }
}