import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    property color barColor: "transparent"

    width: parent.width
    height: parent.height
    color: barColor

    RowLayout {
        anchors.fill: parent

        Item {
            Layout.fillWidth: true
        }

        Item {
            id: logoImage
            width: parent.width
            Layout.preferredHeight: 60
            Image {
                width: parent.height
                height: parent.height
                anchors.centerIn: parent
                fillMode: Image.PreserveAspectFit
                source: "../images/LOGOV6.png"
            }
        }

        Item {
            Layout.fillWidth: true
        }
    }
}