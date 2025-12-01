import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "view"

ApplicationWindow {
    id: window
    visible: true
    width: 910
    minimumWidth: 910
    height: 600
    minimumHeight: 600
    title: "SNP2PHENO"
    color: "#102F4A"

    GridLayout {
        id: mainLayout
        anchors.fill: parent
        anchors.margins: 2
        columns: 2
        rows: 2
        rowSpacing: 2
        columnSpacing: 2

        ContentContainer {
            Layout.fillWidth: true
        }

        FileSelection {
            Layout.preferredWidth: 200
        }

        Logo {
            Layout.preferredWidth: 200
            Layout.preferredHeight: 150
        }
    }
}
