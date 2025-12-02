import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Basic 2.15

Rectangle {
    property string tabText: "undefined"
    property string sideTab: "undefined" // the sidetab property, tells the ab whether it's on one of the ends of the tabbar
    property int radius: 5
    property int index: 0

    Layout.preferredWidth: 100
    Layout.preferredHeight: parent.height
    Layout.alignment: Qt.AlignLeft
    color: "transparent"

    Button {
        id: button
        text: parent.tabText
        width: parent.width
        height: parent.height

        background: Rectangle {
            topLeftRadius:     sideTab === "left"  ? parent.parent.radius : 0
            bottomLeftRadius:  sideTab === "left"  ? parent.parent.radius : 0
            topRightRadius:    sideTab === "right" ? parent.parent.radius : 0
            bottomRightRadius: sideTab === "right" ? parent.parent.radius : 0

            color: button.pressed || button.hovered || contentContainer.selectedIndex === index ? "#AED2DC" : "#26515D"
        }
        onClicked: {
            contentContainer.selectedIndex = index
        }
    }
}