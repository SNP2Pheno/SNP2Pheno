import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "components"

ApplicationWindow {
    id: window
    visible: true
    width: 910
    minimumWidth: 910
    height: 600
    minimumHeight: 600
    title: "SNP2PHENO"
    color: "#17415D"

    GridLayout {
        id: mainLayout
        anchors.fill: parent
        anchors.margins: 2
        columns: 4
        rows: 3
        rowSpacing: 2
        columnSpacing: 2

        TabBar {
            id: tabBar
            barColor: "#345972"
            Layout.columnSpan: 4
            Layout.preferredHeight: 40
            Layout.alignment: Qt.AlignTop | Qt.AlignHCenter
            Layout.fillWidth: true
            Layout.fillHeight: false
        }

        Item {
            Layout.columnSpan: 3
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumHeight: 60
            Layout.minimumWidth: 600
            Layout.alignment: Qt.AlignCenter

            Rectangle {
                anchors.centerIn: parent
                anchors.fill: parent
                border.width: 1
                border.color: "#081721"
                color: "#F3F5F7"
            }
        }
        Item {
            Layout.fillHeight: true
            Layout.preferredWidth: 300
            Layout.minimumWidth: 300
            Layout.alignment: Qt.AlignCenter

            Rectangle {
                anchors.centerIn: parent
                anchors.fill: parent
                border.width: 1
                border.color: "#081721"
                color: "#F3F5F7"
            }
        }

    }
}
