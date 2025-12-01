import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    Layout.fillWidth: true
    Layout.fillHeight: true
    Layout.rowSpan: 2

    color: "transparent"

    GridLayout{
        rows: 2
        columns: 2
        id: contentContainer
        width: parent.width
        height: parent.height

        property int selectedIndex: 0

        TabBar {
            Layout.columnSpan: 2
        }

        ColumnLayout {
            Layout.preferredWidth: 150
            Layout.fillHeight: true

            Text {
                text: "Test"
            }
        }

        StackLayout {
            currentIndex: contentContainer.selectedIndex

            Layout.fillHeight: true
            Layout.fillWidth: true

            ContentTable{}
            ContentVisualization{}
        }
    }
}