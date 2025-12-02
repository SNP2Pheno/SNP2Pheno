import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: contentRoot
    Layout.fillWidth: true
    Layout.fillHeight: true
    color: "#ffffff"

    property var rows: controller ? controller.results : []
    property var headers: rows.length > 0 ? Object.keys(rows[0]) : []

    property int headerHeight: 40
    property int rowHeight: 40
    property int columnWidth: Math.max(width / headers.length, 120) // <- 120px is minimum column width

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // Table header
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: contentRoot.headerHeight
            color: "#f0f0f0"
            border.color: "#cccccc"
            border.width: 1

            Flickable {
                id: headerFlick
                anchors.fill: parent
                contentWidth: Math.max(contentRoot.width, contentRoot.headers.length * contentRoot.columnWidth)
                contentHeight: contentRoot.headerHeight
                interactive: false
                clip: true

                Row {
                    width: headerFlick.contentWidth
                    height: contentRoot.headerHeight
                    spacing: 0

                    Repeater {
                        model: headers.length
                        Rectangle {
                            width: contentRoot.columnWidth
                            height: contentRoot.headerHeight
                            color: "#f0f0f0"
                            border.color: "#cccccc"
                            border.width: 1

                            Text {
                                anchors.centerIn: parent
                                text: headers[index] || ""
                                font.bold: true
                                font.pixelSize: 14
                                horizontalAlignment: Text.AlignHCenter
                                elide: Text.ElideRight
                                width: parent.width
                            }
                        }
                    }
                }
            }
        }

        // Table content
        Flickable {
            id: contentFlick
            Layout.fillWidth: true
            Layout.fillHeight: true
            contentWidth: Math.max(contentRoot.width, contentRoot.headers.length * contentRoot.columnWidth)
            contentHeight: contentRoot.rows.length * contentRoot.rowHeight
            clip: true

            onContentXChanged: {
                headerFlick.contentX = contentFlick.contentX
            }

            Column {
                width: contentFlick.contentWidth
                spacing: 0

                Repeater {
                    model: rows
                    Row {
                        property var rowData: modelData
                        width: contentFlick.contentWidth
                        height: contentRoot.rowHeight
                        spacing: 0

                        Repeater {
                            model: headers.length
                            Rectangle {
                                width: contentRoot.columnWidth
                                height: contentRoot.rowHeight
                                color: (rows.indexOf(rowData)) % 2 === 0 ? "#ffffff" : "#f8f8f8"
                                border.color: "#cccccc"
                                border.width: 1

                                Text {
                                    anchors.centerIn: parent
                                    text: {
                                        var value = rowData[headers[index]]
                                        return value !== undefined && value !== null ? value.toString() : ""
                                    }
                                    font.pixelSize: 13
                                    horizontalAlignment: Text.AlignHCenter
                                    elide: Text.ElideRight
                                    width: parent.width
                                }
                            }
                        }
                    }
                }
            }

            ScrollBar.vertical: ScrollBar { }
            ScrollBar.horizontal: ScrollBar { }
        }
    }
}
