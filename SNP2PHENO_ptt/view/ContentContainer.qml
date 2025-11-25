import QtQuick 2.15
import QtQuick.Layouts 1.15

Rectangle {
    Layout.fillWidth: true
    Layout.fillHeight: true
    Layout.rowSpan: 2

    color: "transparent"

    ColumnLayout{
        id: contentContainer
        width: parent.width
        height: parent.height

        property int selectedIndex: 0

        TabBar {}

        StackLayout {
            currentIndex: contentContainer.selectedIndex

            Layout.fillHeight: true
            Layout.fillWidth: true

            ContentTable{}
            ContentVisualization{}
        }
    }
}