import QtQuick 2.15
import QtCore
import QtQuick.Window 2.2
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs
import Qt.labs.settings 1.0
import MyApp 1.0
import Qt.labs.folderlistmodel 2.1
import Qt.labs.qmlmodels 1.0


ApplicationWindow {
    id: window
    visible: true
    width: 1000
    height: 600
    title: "SNP2PHENO"

    // Neue Beispiel-Daten (als Krankheiten mit Markern)
    property var preExistingList: [
        {
            name: "Diabetes",
            markers: [
                { snp: "rs1234, rs2345", effect: "Increases risk (insulin resistance)", severity: 2 },
                { snp: "rs3456", effect: "Decreases risk (improves metabolism)", severity: 1 },
                { snp: "rs6789", effect: "Decreases risk (better vasodilation)", severity: 1 },
                { snp: "rs7890", effect: "Increases risk (vascular stiffness)", severity: 2 }
            ]
        },
        {
            name: "Alzheimer's",
            markers: [
                { snp: "rs4567", effect: "No significant effect", severity: 0 },
                { snp: "rs5678", effect: "Increases risk (amyloid plaque buildup)", severity: 2 }
            ]
        },
        {
            name: "Hypertension",
            markers: [
                { snp: "rs6789", effect: "Decreases risk (better vasodilation)", severity: 1 },
                { snp: "rs7890", effect: "Increases risk (vascular stiffness)", severity: 2 }
            ]
        }
    ]
    property var fileItems: []
    property bool infoVisible: false
    // F�r die Krankheitsdetails wird jetzt ein Array erwartet
    property var selectedInfo: []
    property string selectedName: ""
    property var parsedFiles: ({})

    VcfToSnp {
        id: vcfToSnp
    }

    Connections {
        target: vcfParser
        onSnpListChanged: {
            console.log("snpListChanged ausgel�st: " + vcfParser.snpList);
            fileItems = vcfParser.snpList;
        }
    }

    // Header
    Rectangle {
        id: header
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: 60
        color: "#17415D"
        Row {
            anchors.centerIn: parent
            spacing: 10
            Rectangle {
                id: logo
                width: 40
                height: 40
                color: "white"
                Text {
                    anchors.centerIn: parent
                    text: "Logo"
                    font.pixelSize: 12
                }
            }
            Text {
                text: "SNP2PHENO"
                font.pixelSize: 24
                color: "white"
            }
        }
    }

    // Hauptinhalt
    Row {
        id: mainRow
        anchors {
            top: header.bottom
            left: parent.left
            right: parent.right
            bottom: debugConsoleView.top
        }
        spacing: 10

        // Linker Bereich: Enth�lt nun die tabContentBox
        Rectangle {
            id: leftBox
            width: parent.width * 0.6 - 10
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            color: "#5f9eb3"
            Column {
                id: leftColumn
                anchors.fill: parent
                anchors.margins: 10
                spacing: 10

                Row {
                    id: tabButtonsRow
                    spacing: 5
                    Button {
                        id: appearanceBtn
                        text: "Appearance"
                        background: Rectangle {
                            radius: 5
                            bottomLeftRadius: 0
                            bottomRightRadius: 0
                            color: appearanceBtn.isClicked ? "#9cccd9" : "#bff4f5"
                        }
                        onClicked: {
                            // Inhalt ggf. �ndern
                        }
                    }
                    Button {
                        id: diseasesBtn
                        text: "Diseases"
                        background: Rectangle {
                            radius: 5
                            bottomLeftRadius: 0
                            bottomRightRadius: 0
                            color: appearanceBtn.isClicked ? "#9cccd9" : "#bff4f5"
                        }
                        onClicked: {
                            // Inhalt ggf. �ndern
                        }
                    }
                    Button {
                        id: otherBtn
                        text: "Other"
                        background: Rectangle {
                            radius: 5
                            bottomLeftRadius: 0
                            bottomRightRadius: 0
                            color: appearanceBtn.isClicked ? "#9cccd9" : "#bff4f5"
                        }
                        onClicked: {
                            // Inhalt ggf. �ndern
                        }
                    }
                }

                Rectangle {
                    id: tabContentBox
                    anchors {
                        top: tabButtonsRow.bottom
                        left: parent.left
                        right: parent.right
                        bottom: parent.bottom
                    }
                    color: "#dfe6e9"
                    RowLayout {
                        id: mainRowContent
                        anchors.fill: parent
                        spacing: 10

                        // Linke Seite: Krankheitsliste
                        ColumnLayout {
                            id: listLayout
                            Layout.preferredWidth: infoVisible ? parent.width / 2 : parent.width
                            Layout.fillHeight: true
                            spacing: 10

                            TextField {
                                id: searchBar
                                placeholderText: "Search diseases..."
                                Layout.fillWidth: true
                                onTextChanged: {
                                    filteredModel.clear();
                                    for (var i = 0; i < preExistingList.length; i++) {
                                        var disease = preExistingList[i];
                                        if (disease.name.toLowerCase().includes(searchBar.text.toLowerCase())) {
                                            filteredModel.append({ "name": disease.name, "index": i });
                                        }
                                    }
                                }
                            }

                            ListView {
                                id: diseaseListView
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                model: filteredModel
                                clip: true
                                delegate: Rectangle {
                                    width: diseaseListView.width
                                    height: 40
                                    color: ListView.isCurrentItem ? "blue" : (mouseArea.containsMouse ? "lightblue" : "white")
                                    border.color: "darkgray"
                                    border.width: 2

                                    Text {
                                        text: name
                                        anchors.centerIn: parent
                                        color: ListView.isCurrentItem ? "white" : "black"
                                        font.pixelSize: 16
                                    }

                                    MouseArea {
                                        id: mouseArea
                                        anchors.fill: parent
                                        hoverEnabled: true
                                        onClicked: {
                                            diseaseListView.currentIndex = index;
                                            selectedName = name;
                                            selectedInfo = preExistingList[index].markers;
                                            infoVisible = true;
                                            infoModel.clear();
                                            for (var i = 0; i < selectedInfo.length; i++) {
                                                infoModel.append(selectedInfo[i]);
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        // Rechte Seite: Tabelle mit genetischen Markern
                        Rectangle {
                            id: infoBox
                            visible: infoVisible
                            Layout.preferredWidth: parent.width / 2
                            Layout.fillHeight: true
                            color: "white"
                            border.color: "black"
                            border.width: 2

                            ColumnLayout {
                                anchors.fill: parent
                                anchors.margins: 10
                                spacing: 10

                                RowLayout {
                                    Layout.fillWidth: true
                                    spacing: 10

                                    Text {
                                        text: "Genetic markers for \"" + selectedName + "\""
                                        font.bold: true
                                        font.pixelSize: 18
                                        Layout.fillWidth: true
                                        //width: parent.width - 10
                                        elide: Text.ElideRight
                                    }
                                    Button {
                                        text: "Close"
                                        onClicked: infoVisible = false
                                    }
                                }

                                // Tabellenkopf
                                Row {
                                    id: headerRow
                                    width: parent.width
                                    Layout.fillWidth: true
                                    height: 30
                                    spacing: 0

                                    Repeater {
                                        model: ["SNPs", "Effect", "Severity"]
                                        Rectangle {
                                            width: headerRow.width / 3
                                            height: 30
                                            color: "#f0f0f0"
                                            border.color: "black"
                                            border.width: 1

                                            Text {
                                                text: modelData
                                                anchors.centerIn: parent
                                                font.bold: true
                                            }
                                        }
                                    }
                                }

                                // Tabelleninhalt
                                ListView {
                                    id: infoListView
                                    width: headerRow.width
                                    Layout.fillHeight: true
                                    Layout.fillWidth: true
                                    model: infoModel
                                    clip: true
                                    delegate: Row {
                                        width: infoListView.width
                                        height: 40
                                        spacing: 0

                                        // SNP-Spalte
                                        Rectangle {
                                            width: infoListView.width / 3
                                            height: 40
                                            color: index % 2 === 0 ? "#ffffff" : "#f8f8f8"
                                            border.color: "black"
                                            border.width: 1

                                            Text {
                                                text: snp
                                                anchors.centerIn: parent
                                                width: parent.width - 10
                                                elide: Text.ElideRight
                                            }
                                        }

                                        // Effekt-Spalte
                                        Rectangle {
                                            width: infoListView.width / 3
                                            height: 40
                                            color: index % 2 === 0 ? "#ffffff" : "#f8f8f8"
                                            border.color: "black"
                                            border.width: 1

                                            Text {
                                                text: effect
                                                anchors.centerIn: parent
                                                width: parent.width - 10
                                                elide: Text.ElideRight
                                            }
                                        }

                                        // Schwere-Spalte
                                        Rectangle {
                                            width: infoListView.width / 3
                                            height: 40
                                            color: index % 2 === 0 ? "#ffffff" : "#f8f8f8"
                                            border.color: "black"
                                            border.width: 1

                                            Text {
                                                text: severity === 0 ? "No effect" : severity === 1 ? "Protective" : "Risk factor"
                                                anchors.centerIn: parent
                                                color: severity === 0 ? "black" : severity === 1 ? "green" : "red"
                                                font.bold: severity !== 0
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

        // Rechter Bereich: VCF File Viewer (unver�ndert)
        // Rechter Bereich: VCF File Viewer + SNP Liste
Rectangle {
    id: rightBox
    width: parent.width * 0.4 - 10
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    //Helper für layout
    //border.width: 10
    color: "#9cccd9"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        // Oberer Bereich: VCF File Viewer (bestehender Inhalt)
        Rectangle {
            id: topHalf
            Layout.fillWidth: true
            Layout.preferredHeight: rightBox.height / 2 - 5
            color: "lightgrey"
            ColumnLayout {
                anchors.fill: parent
                spacing: 10

                Button {
                    text: "Ordner mit VCF-Dateien ausw�hlen"
                    onClicked: folderDialog.open()
                }

//VCF LISTE EINLESEN
                ListView {
                    id: vcfListView
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    model: folderModel

                    // Initialisierung des parsedFiles-Objekts
                    property var parsedFiles: ({})

                    delegate: Rectangle {
                        id: fileDelegate
                        width: vcfListView.width
                        height: 40
                        border.width: 1
                        border.color: "gray"
                        color: (vcfListView.parsedFiles[filePath] === true) ? "lightgreen" : (mouseArea.containsMouse ? "lightgray" : "white")

                        RowLayout {
                            anchors.fill: parent
                            spacing: 10
                            anchors.margins: 5

                            Text {
                                Layout.fillWidth: true
                                text: fileName
                                font.pixelSize: 16
                                color: "black"
                                elide: Text.ElideRight
                            }

                            Rectangle {
                                id: button_Edit_AFQ
                                visible: vcfListView.parsedFiles[filePath] === true
                                width: 30
                                height: 30
                                color: "transparent"
                                border.color: "darkgreen"
                                border.width: 1
                                radius: 4
                                Layout.alignment: Qt.AlignRight

                                Image {
                                    anchors.centerIn: parent
                                    width: 24
                                    height: 24
                                    source: "./images/SNP_AFQ_ICON.jpg"
                                    fillMode: Image.PreserveAspectFit
                                }

                                MouseArea {
                                    anchors.fill: parent
                                    cursorShape: Qt.PointingHandCursor
                                    onClicked: {
                                        console.log("AFQ-Button geklickt für:", filePath)
                                        windowLauncher.openAFQEditor()
                                    }
                                }
                            }
                        }

                        MouseArea {
                            id: mouseArea
                            anchors.fill: parent
                            hoverEnabled: true
                            propagateComposedEvents: true // Allow child MouseAreas to receive events
                            onClicked: {
                                vcfListView.currentIndex = index
                                mouse.accepted = false // Let the event propagate to children
                            }
                            onDoubleClicked: {
                                console.log("Parsing file:", filePath);
                                vcfParser.startParsing(filePath);

                                var updatedParsedFiles = vcfListView.parsedFiles;
                                updatedParsedFiles[filePath] = true;
                                vcfListView.parsedFiles = updatedParsedFiles;
                            }
                        }
                    }
                }
                //Listview
            }
        }

        // Unterer Bereich: SNP Liste (fileItems)
        Rectangle {
            id: bottomHalf
    Layout.minimumHeight: 100  // Mindesth�he sicherstellen

            Layout.fillWidth: true
            Layout.preferredHeight: rightBox.height / 2 - 5
    Layout.bottomMargin: 70

            color: "darkgrey"


            ScrollView {
                anchors.fill: parent
                anchors.margins: 10
                ScrollBar.vertical.policy: ScrollBar.AsNeeded

                ListView {
                    id: fileListView
                    anchors.margins: 10
                    clip: true
                    model: fileItems = ["test","test","test","test","test","test","test","test"]
                    delegate: Rectangle {
                        id: delegateRect
                        property bool isHovered: false
                        width: fileListView.width
                        height: 40
                        color: ListView.isCurrentItem ? "blue" : (isHovered ? "lightblue" : "white")
                        border.width: 2
                        border.color: "darkgray"

                        Text {
                            text: modelData
                            anchors.centerIn: parent
                            color: ListView.isCurrentItem ? "white" : (isHovered ? "red" : "black")
                            font.pixelSize: 16
                        }

                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true
                            onClicked: fileListView.currentIndex = index
                            onEntered: delegateRect.isHovered = true
                            onExited: delegateRect.isHovered = false
                        }
                    }
                }
            }
        }
    }
}
    }       
    // Debug-Konsole am unteren Rand
    Rectangle {
        id: debugConsoleView
        anchors {
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
        height: 150
        color: "black"
        border.width: 4
        border.color: "red"

        ScrollView {
            id: consoleScroll
            anchors.fill: parent
            ScrollBar.vertical.policy: ScrollBar.AsNeeded

            TextArea {
                id: consoleTextArea
                Layout.fillWidth: true
                Layout.fillHeight: true
                readOnly: true
                wrapMode: Text.Wrap
                font.pixelSize: 14
                color: "green"
                background: null
                text: debugConsole.log
                onTextChanged: {
                    consoleTextArea.cursorPosition = consoleTextArea.text.length;
                }
            }
        }
    }

    // FileDialog f�r .vcf Dateien
    FileDialog {
        id: fileDialog_vcf
        title: "Select .vcf file"
        nameFilters: ["*.vcf", "*.txt"]
        currentFolder: StandardPaths.writableLocation(StandardPaths.HomeLocation)
        onAccepted: {
            if (selectedFiles.length > 0) {
                var fileUrlStr = selectedFiles[0];
                vcfParser.startParsing(fileUrlStr);
            } else {
                console.log("No file selected");
            }
        }
    }

    // FileDialog f�r SNP Listen
    FileDialog {
        id: fileDialog_snp
        title: "Select SNP list"
        nameFilters: ["*.txt"]
        onAccepted: {
            // Verarbeitung der SNP Liste
        }
    }

    // Modelle f�r Krankheitsliste und Info-Tabelle
    ListModel {
        id: filteredModel
        Component.onCompleted: {
            for (var i = 0; i < preExistingList.length; i++) {
                filteredModel.append({ "name": preExistingList[i].name, "index": i });
            }
        }
    }

    ListModel {
        id: infoModel
    }

    // FolderDialog zur Auswahl eines Ordners mit VCF-Dateien
    FolderDialog {
        id: folderDialog
        title: "Ordner mit VCF-Dateien ausw�hlen"
        currentFolder: StandardPaths.writableLocation(StandardPaths.HomeLocation)
        onAccepted: {
            folderModel.folder = selectedFolder
            // Bei Ordnerwechsel zur�cksetzen
            parsedFiles = {}
        }
    }

    // FolderListModel zur Anzeige der VCF-Dateien
    FolderListModel {
        id: folderModel
        folder: ""
        nameFilters: ["*.vcf"]
        showDirs: false
        property string filePath: fileURL
    }
}
