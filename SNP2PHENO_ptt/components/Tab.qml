import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    property string tabText: "undefined"

    Layout.preferredWidth: 80
    Layout.preferredHeight: 40
    Layout.alignment: Qt.AlignLeft
    color: "transparent"

    border.width: 1
    border.color:"#081721"

    Text {
        text: parent.tabText
        color: "white"
        width: parent.width
        height: parent.height
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
}