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

    // new sample data
    property var preExistingListDisease: [
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

    property var preExistingListAppearance: [
            {
                name: "brown hair",
                markers: [
                    { snp: "rs1234, rs2345", effect: "Increases risk (insulin resistance)", severity: 2 },
                    { snp: "rs3456", effect: "Decreases risk (improves metabolism)", severity: 1 },
                    { snp: "rs6789", effect: "Decreases risk (better vasodilation)", severity: 1 },
                    { snp: "rs7890", effect: "Increases risk (vascular stiffness)", severity: 2 }
                ]
            },
            {
                name: "blue eyes",
                markers: [
                    { snp: "rs4567", effect: "No significant effect", severity: 0 },
                    { snp: "rs5678", effect: "Increases risk (amyloid plaque buildup)", severity: 2 }
                ]
            },
            {
                name: "brown eyes",
                markers: [
                    { snp: "rs6789", effect: "Decreases risk (better vasodilation)", severity: 1 },
                    { snp: "rs7890", effect: "Increases risk (vascular stiffness)", severity: 2 }
                ]
            }
    ]

    property var fileItems: []
    property bool infoVisible: false
    property var selectedInfo: []
    property string selectedName: ""
    property var parsedFiles: ({})

    VcfToSnp {
        id: vcfToSnp
    }

    Connections {
        target: vcfParser
        onSnpListChanged: {
            console.log("snpListChanged ausgelöst: " + vcfParser.snpList);
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
        color: "#102F4A"
        Row {
            anchors.centerIn: parent
            spacing: 10
            Rectangle {
                id: logo
                width: 40
                height: 40
                color: "transparent"
                Image {
                    anchors.centerIn: parent
                    width: parent.width
                    height: parent.height
                    source: "images/LOGOV6.png"
                }
            }
            Text {
                text: "SNP2PHENO"
                font.pixelSize: 24
                color: "white"
            }
        }
    }

    // main body
    Row {
        id: mainRow
        anchors {
            top: header.bottom
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
        spacing: 10

        // left area: only contains tabContentBox
        Rectangle {
            id: leftBox
            width: parent.width * 0.7 - 10
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            color: "#5F9EB3"
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
                            color: appearanceBtn.isClicked ? "#AED2DC" : "#26515D"
                        }
                        onClicked: {
                            //TODO: Add action to onClick
                        }
                    }
                    Button {
                        id: diseasesBtn
                        text: "Diseases"
                        background: Rectangle {
                            radius: 5
                            bottomLeftRadius: 0
                            bottomRightRadius: 0
                            color: appearanceBtn.isClicked ? "#AED2DC" : "#26515D"
                        }
                        onClicked: {
                            //TODO: Add action to onClick
                        }
                    }
                    Button {
                        id: otherBtn
                        text: "Other"
                        background: Rectangle {
                            radius: 5
                            bottomLeftRadius: 0
                            bottomRightRadius: 0
                            color: appearanceBtn.isClicked ? "#AED2DC" : "#26515D"
                        }
                        onClicked: {
                            //TODO: Add action to onClick
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
                    color: "#AED2DC"
                    radius: 5
                    topLeftRadius: 0
                    RowLayout {
                        id: mainRowContent
                        anchors.fill: parent
                        spacing: 10

                        // left area: disease area
                        ColumnLayout {
                            id: listLayout
                            Layout.preferredWidth: infoVisible ? parent.width / 2 : parent.width
                            Layout.fillHeight: true
                            spacing: 10

                            TextField {
                                id: searchBar
                                placeholderText: "Search diseases..."
                                Layout.fillWidth: true
                                Layout.margins: 5
                                Layout.topMargin: 15

                                background: Rectangle {
                                    radius: 2
                                    implicitWidth: 100
                                    implicitHeight: 24
                                    border.color: "#333"
                                    border.width: 1
                                }
                                
                                onTextChanged: {
                                    filteredModel.clear();
                                    for (var i = 0; i < preExistingListDisease.length; i++) {
                                        var disease = preExistingListDisease[i];
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
                                Layout.margins: 5

                                model: filteredModel
                                clip: true
                                delegate: Rectangle {
                                    radius: 5                                    
                                    width: diseaseListView.width
                                    height: 40
                                    color: ListView.isCurrentItem ? "#102F4A" : (mouseArea.containsMouse ? "#D0E6EC" : "white")
                                    border.color: "darkgray"
                                    border.width: 2

                                    Text {
                                        text: name
                                        anchors.centerIn: parent
                                        color: diseaseListView.currentIndex === index ? "white" : (mouseArea.containsMouse ? "#535353" : "black")
                                        font.pixelSize: 16
                                    }

                                    MouseArea {
                                        id: mouseArea
                                        anchors.fill: parent
                                        hoverEnabled: true
                                        onClicked: {
                                            diseaseListView.currentIndex = index;
                                            selectedName = name;
                                            selectedInfo = preExistingListDisease[index].markers;
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

                        // right area: area with genetic markers
                        Rectangle {
                            id: infoBox
                            visible: infoVisible
                            Layout.preferredWidth: parent.width / 1.5
                            Layout.fillHeight: true
                            color: "#487E9B"
                            border.color: "#AED2DC"
                            border.width: 4
                            radius: 5
                            topLeftRadius: 2
                            bottomLeftRadius: 2

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
                                        elide: Text.ElideRight
                                    }
                                    Button {
                                        text: "Close"
                                        onClicked: infoVisible = false
                                    }
                                }

                                // table header
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

                                // table content
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

                                        // SNP-column
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

                                        // effect column
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

                                        // severity column
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

        // right area: VCF File Viewer (unchanged)
        // right area: VCF File Viewer and SNP list
Rectangle {
    id: rightBox
    width: parent.width * 0.3 - 10
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    color: "#9cccd9"

    Rectangle {
        id: topHalf
        width: rightBox.width
        height: rightBox.height
        color: "#102F4A"

        Button {
            text: "Ordner mit VCF-Dateien auswählen"
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.margins: 10
            onClicked: folderDialog.open()
        }

        ListView {
            id: vcfListView
            anchors.top: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            model: folderModel
            delegate: Rectangle {
                id: fileDelegate
                width: vcfListView.width
                height: 40
                border.width: 1
                border.color: "gray"
                color: parsedFiles[filePath] ? "lightgreen" : (mouseArea.containsMouse ? "lightgray" : "white")

                Text {
                    anchors.centerIn: parent
                    text: fileName
                    font.pixelSize: 16
                    color: "black"
                    width: parent.width - 10
                    elide: Text.ElideRight
                }

                MouseArea {
                    id: mouseAreaVcfListView
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: vcfListView.currentIndex = index
                    onDoubleClicked: {
                        console.log("Parsing file:", filePath)
                        vcfParser.startParsing(filePath)
                        parsedFiles[filePath] = true
                    }
                }
            }
        }
    }
}
    }       


    // FileDialog for .vcf files
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

    // FileDialog for SNP lists
    FileDialog {
        id: fileDialog_snp
        title: "Select SNP list"
        nameFilters: ["*.txt"]
        onAccepted: {
            //TODO: process SNP list
        }
    }

    // model for disease list and info table
    ListModel {
        id: filteredModel
        Component.onCompleted: {
            for (var i = 0; i < preExistingListDisease.length; i++) {
                filteredModel.append({ "name": preExistingListDisease[i].name, "index": i });
            }
        }
    }

    ListModel {
        id: infoModel
    }

    // FolderDialog for selection of folder containing VCF files
    FolderDialog {
        id: folderDialog
        title: "Ordner mit VCF-Dateien ausw�hlen"
        currentFolder: StandardPaths.writableLocation(StandardPaths.HomeLocation)
        onAccepted: {
            folderModel.folder = selectedFolder
            //reset when switching folders
            parsedFiles = {}
        }
    }

    // FolderListModel to display VCF files
    FolderListModel {
        id: folderModel
        folder: ""
        nameFilters: ["*.vcf"]
        showDirs: false
        property string filePath: fileURL
    }
}
