import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Basic 2.15
import QtQuick.Dialogs

Rectangle {
    id: root

    Layout.fillHeight: true
    color: "transparent"

    FileDialog {
        id: fileDialog
        title: qsTr("Select files")
        fileMode: FileDialog.OpenFiles
        nameFilters: ["All Fileformats (*.txt *.vcf)", "VCF (*.vcf)", "TXT / 23andMe (*.txt)"]

        onAccepted: {
            var paths = []
            for (var i = 0; i < selectedFiles.length; ++i) {
                var urlString = selectedFiles[i].toString()
                urlString = decodeURIComponent(urlString)
                paths.push(urlString)
            }
            controller.addSelectedFiles(paths)
        }
    }

    ColumnLayout {
        width: parent.width
        height: parent.height

        Button {
            id: button
            text: "Select files"
            Layout.preferredHeight: 40
            Layout.fillWidth: true

            background: Rectangle {
                radius: 5
                color: button.pressed || button.hovered ? "#AED2DC" : "#1D5586"
            }
            onClicked: fileDialog.open()
        }

        Flickable {
            Layout.fillWidth: true
            Layout.fillHeight: true
            contentHeight: buttonColumn.implicitHeight
            contentWidth: width
            clip: true

            interactive: contentHeight > height

            ColumnLayout {
                id: buttonColumn
                width: parent.width
                spacing: mainLayout.rowSpacing

                Repeater {
                    model: controller.selectedFiles

                    Button {
                        id: button

                        property string fileName: {
                            let path = modelData.toString()
                            const idx = path.lastIndexOf("/")
                            return idx >= 0 ? path.slice(idx + 1) : path
                        }

                        contentItem: Rectangle {
                            id: contentRectangle
                            property int contentHeight: 18

                            anchors.fill: parent
                            anchors.margins: (parent.height - contentHeight) / 2

                            color: "transparent"

                            RowLayout {
                                anchors.fill: parent

                                Image {
                                    source: "../images/file_icon.png"
                                    Layout.preferredHeight: contentRectangle.contentHeight
                                    Layout.preferredWidth: contentRectangle.contentHeight
                                    fillMode: Image.PreserveAspectFit
                                    Layout.alignment: Qt.AlignVCenter
                                }

                                Item {
                                    id: textContainer
                                    Layout.fillWidth: true
                                    Layout.alignment: Qt.AlignVCenter
                                    implicitHeight: buttonText.implicitHeight

                                    Flickable {
                                        id: flick
                                        anchors.fill: parent
                                        clip: true

                                        contentWidth: buttonText.implicitWidth
                                        contentHeight: height
                                        interactive: contentWidth > width

                                        contentX: (contentWidth > width ? (contentWidth - width) / 2 : 0)

                                        Text {
                                            id: buttonText
                                            anchors.verticalCenter: parent.verticalCenter
                                            width: flick.contentWidth
                                            text: button.fileName
                                            font: button.font
                                            color: "black"
                                            horizontalAlignment: Text.AlignHCenter
                                        }
                                    }
                                }
                            }
                        }

                        Layout.preferredHeight: 40
                        Layout.fillWidth: true

                        background: Rectangle {
                            id: bg
                            radius: 5
                            color: parent.colorForStatus(controller.requestFileStatus(modelData.toString()))
                        }

                        function colorForStatus(status) {
                            switch (status) {
                                case 0:  // idle
                                    return "white"
                                case 1:  // parsing
                                    return "lightgrey"
                                case 2:  // parsed successfully
                                    return "green"
                                case 3:  // parsed error
                                    return "#E72326"
                                default:
                                    return "white"
                            }
                        }

                        Connections {
                            target: controller
                            function onFileStatusChanged(fileName) {
                                if (fileName === modelData.toString()) {
                                    let status = controller.requestFileStatus(modelData.toString());
                                    bg.color = colorForStatus(status)
                                }
                            }
                        }

                        onDoubleClicked: {
                            controller.startParsing(modelData.toString())
                        }

                        onClicked: {
                            controller.showResult(modelData.toString())
                        }
                    }
                }
            }
        }

        Button {
            id: deleteButton
            text: "Clear selected files"
            Layout.preferredHeight: 40
            Layout.fillWidth: true

            background: Rectangle {
                radius: 5
                color: deleteButton.pressed || deleteButton.hovered ? "#E72326" : "#C71619"
            }
            onClicked: controller.clearSelectedFiles()
        }
    }
}