import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    color: "transparent"

    Image {
        width: Math.min(parent.width, parent.height)
        height: Math.min(parent.width, parent.height)
        anchors.centerIn: parent
        source: "../images/LOGOV6.png"
    }
}