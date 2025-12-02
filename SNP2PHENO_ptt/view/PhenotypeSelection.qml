import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Basic 2.15

Rectangle {
    color: "transparent"

    Flickable {
        anchors.fill: parent
        contentHeight: buttonColumn.implicitHeight
        contentWidth: width
        clip: true

        interactive: contentHeight > height

        ScrollBar.vertical: ScrollBar {
            policy: ScrollBar.AsNeeded
        }

        ColumnLayout {
            id: buttonColumn
            width: parent.width
            spacing: 0

            Repeater {
                model: controller.availableActions
                Button {
                    id: button
                    text: modelData.replace("on", "")
                    Layout.preferredHeight: 40
                    Layout.fillWidth: true

                    background: Rectangle {
                        radius: 5
                        color: button.pressed || button.hovered ? "#AED2DC" : "#26515D"
                    }
                    onClicked: controller.invokeAction(modelData)
                }
            }
        }
    }
}