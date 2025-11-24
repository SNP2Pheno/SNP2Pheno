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
            spacing: 0

            Item {
                Layout.fillWidth: true
            }
            Tab {
                tabText: "TableView"
                sideTab: "left"
            }
            Tab {
                tabText: "Visualization"
                sideTab: "right"
            }
        }
    }
}