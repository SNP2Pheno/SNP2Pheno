import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    Layout.fillWidth: true
    Layout.fillHeight: true
    color: "#ffffff"

    property var rows: controller ? controller.results : []
    property var headers: rows.length > 0 ? Object.keys(rows[0]) : []

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 0

        // Header Row
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 40
            color: "#f0f0f0"
            border.color: "#cccccc"
            border.width: 1

            Row {
                anchors.fill: parent
                spacing: 0

                Repeater {
                    model: headers.length
                    Rectangle {
                        width: tableContainer.width / headers.length
                        height: 40
                        color: "#f0f0f0"
                        border.color: "#cccccc"
                        border.width: 1

                        Text {
                            anchors.centerIn: parent
                            text: headers[index] || ""
                            font.bold: true
                            font.pixelSize: 14
                        }
                    }
                }
            }
        }

        // Scrollable Table Content
        ScrollView {
            id: tableContainer
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true

            Column {
                width: tableContainer.width
                spacing: 0

                Repeater {
                    model: rows.length

                    Rectangle {
                        property int rowIndex: index
                        width: tableContainer.width
                        height: 40
                        color: "transparent"

                        Row {
                            spacing: 0

                            Repeater {
                                model: headers.length

                                Rectangle {
                                    property int colIndex: index
                                    width: tableContainer.width / headers.length
                                    height: 40
                                    color: rowIndex % 2 === 0 ? "#ffffff" : "#f8f8f8"
                                    border.color: "#cccccc"
                                    border.width: 1

                                    Text {
                                        anchors.centerIn: parent
                                        text: {
                                            if (rows[rowIndex] && headers[colIndex]) {
                                                var value = rows[rowIndex][headers[colIndex]]
                                                return value !== undefined && value !== null ? value.toString() : ""
                                            }
                                            return ""
                                        }
                                        font.pixelSize: 13
                                        elide: Text.ElideRight
                                        width: parent.width - 10
                                        horizontalAlignment: Text.AlignHCenter
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
