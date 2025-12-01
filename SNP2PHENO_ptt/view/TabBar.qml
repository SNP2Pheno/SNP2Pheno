import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    property color barColor: "transparent"

    Layout.fillWidth: true

    color: barColor

    RowLayout {
        anchors.fill: parent
        spacing: 0

        Item {
            Layout.fillWidth: true
        }
        Tab {
            index: 0
            tabText: "TableView"
            sideTab: "left"
        }
        Tab {
            index: 1
            tabText: "Visualization"
            sideTab: "right"
        }
    }
}