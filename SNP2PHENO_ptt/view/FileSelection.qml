import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Basic 2.15
import QtQuick.Dialogs

Rectangle {
    id: root

    Layout.fillHeight: true
    color: "transparent"

    property var selectedFiles: []

    FileDialog {
        id: fileDialog
        title: qsTr("Select files or folder")
        fileMode: FileDialog.OpenFiles
        nameFilters: ["All Fileformats (*.txt *.vcf)", "VCF (*.vcf)", "TXT / 23andMe (*.txt)"]

        onAccepted: {
            root.selectedFiles = selectedFiles
            console.log("Selected files:", selectedFiles)
        }
    }

    ColumnLayout {
        anchors.fill: parent

        Button {
            id: button
            text: "Select files or folder"
            Layout.preferredHeight: 40
            Layout.fillWidth: true

            background: Rectangle {
                radius: 5
                color: button.pressed || button.hovered ? "#AED2DC" : "#26515D"
            }
            onClicked: fileDialog.open()
        }

        Item {
            Layout.fillHeight: true
            Layout.fillWidth: true
        }
    }
}