import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Basic 2.15

Rectangle {
    color: "transparent"

    ColumnLayout {
        anchors.fill: parent

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
        Item {
            Layout.fillHeight: true
        }
    }
}