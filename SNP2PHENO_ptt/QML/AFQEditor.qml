import QtQuick 2.15
import QtCore
import QtQuick.Window 2.2
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs
import Qt.labs.settings 1.0
import Qt.labs.folderlistmodel 2.1
import Qt.labs.qmlmodels 1.0
import QueryApp 1.0

ApplicationWindow {
    id: window
    visible: true
    width: 900
    height: 600
    title: qsTr("Phenotyping Tool")

    ListModel {
        id: snpModel
        // Updated default values with gene column
        /*        ListElement {
                    snp: "rs312262906"; allele: "A"; noOfAlleles: "2"; gene: "HERC2"
                }
                ListElement {
                    snp: "rs11547464"; allele: "A"; noOfAlleles: "NA"; gene: "OCA2"
                }
                ListElement {
                    snp: "rs885479"; allele: "T"; noOfAlleles: "0"; gene: "TYR"
                }


         */
    }




    ListModel {
        id: resultModel
    }

    SnpDatabase {
        id: snpDb
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        // Box 1: Load SNPs
        Rectangle {
            id: load_and_select_snp
            Layout.fillWidth: true
            Layout.preferredHeight: 400
            color: "#00b894"

            FileDialog {
                id: fileDialog_snp
                title: "Select SNP list"
                nameFilters: ["*.txt"]
                onAccepted: {
                    if (selectedFiles.length > 0) {
                        var fileUrlStr = selectedFiles[0];
                        console.log("Selected file: " + fileUrlStr);
                        var content = readFile(fileUrlStr);
                        if (content.length > 0) {
                            var snps = content.split(";");
                            snpModel.clear();
                            for (var i = 0; i < snps.length; ++i) {
                                var snpTrimmed = snps[i].trim();
                                if (snpTrimmed.length > 0) {
                                    var results = snpDb.querySnp(snpTrimmed);
                                    if (results.length > 0) {
                                        for (var j = 0; j < results.length; ++j) {
                                            var result = results[j];
                                            snpModel.append({
                                                snp: result.snp,
                                                allele: result.allele,
                                                noOfAlleles: "NA",
                                                gene: result.gene || "NA"
                                            });
                                        }
                                    } else {
                                        snpModel.append({
                                            snp: snpTrimmed,
                                            allele: "NA",
                                            noOfAlleles: "NA",
                                            gene: "NA"
                                        });
                                    }
                                }
                            }
                        }
                    } else {
                        console.log("No file selected");
                    }
                }

                function readFile(fileUrl) {
                    var xhr = new XMLHttpRequest();
                    xhr.open("GET", fileUrl, false);
                    xhr.send();
                    if (xhr.status === 200 || xhr.status === 0) {
                        return xhr.responseText;
                    } else {
                        console.log("Error reading file: " + xhr.status);
                        return "";
                    }
                }
            }

            ColumnLayout {
                id: mainLayout
                anchors.fill: parent
                spacing: 0

                Button {
                    text: "Load SNP List"
                    onClicked: fileDialog_snp.open()
                    Layout.alignment: Qt.AlignLeft
                    Layout.leftMargin: 5
                    Layout.topMargin: 5
                    Layout.bottomMargin: 5
                }

                GridLayout {
                    id: headerLayout
                    // Update columns to 4
                    columns: 4
                    rowSpacing: 0
                    columnSpacing: 0

                    // Update column widths
                    property int alleleColumnWidth: 70
                    property int noOfAllelesColumnWidth: 200
                    property int snpColumnWidth: (parent.width - (noOfAllelesColumnWidth + alleleColumnWidth)) * 0.8
                    property int geneColumnWidth: (parent.width - (noOfAllelesColumnWidth + alleleColumnWidth)) * 0.2

                    Rectangle {
                        Layout.preferredWidth: headerLayout.geneColumnWidth
                        Layout.preferredHeight: 30
                        color: "#f0f0f0"
                        border.color: "black"
                        border.width: 1
                        Text {
                            text: "Gene"; anchors.centerIn: parent; font.bold: true
                        }
                    }

                    // Add new header for Gene column
                    Rectangle {
                        Layout.preferredWidth: headerLayout.snpColumnWidth
                        Layout.preferredHeight: 30
                        color: "#f0f0f0"
                        border.color: "black"
                        border.width: 1
                        Text {
                            text: "SNP"; anchors.centerIn: parent; font.bold: true
                        }
                    }
                    Rectangle {
                        Layout.preferredWidth: headerLayout.alleleColumnWidth
                        Layout.preferredHeight: 30
                        color: "#f0f0f0"
                        border.color: "black"
                        border.width: 1
                        Text {
                            text: "Allele"; anchors.centerIn: parent; font.bold: true
                        }
                    }
                    Rectangle {
                        Layout.preferredWidth: headerLayout.noOfAllelesColumnWidth
                        Layout.preferredHeight: 30
                        color: "#f0f0f0"
                        border.color: "black"
                        border.width: 1
                        Text {
                            text: "No. of Alleles"; anchors.centerIn: parent; font.bold: true
                        }
                    }

                }

                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    ListView {
                        id: snpListView
                        width: parent.width
                        height: parent.height
                        model: snpModel
                        clip: true
                        boundsBehavior: Flickable.StopAtBounds

                        delegate: GridLayout {
                            id: rowLayout
                            // Update columns to 4
                            columns: 4
                            rowSpacing: 0
                            columnSpacing: 0

                            property int rowIndex: index

                            Rectangle {
                                Layout.fillWidth: true
                                Layout.preferredWidth: headerLayout.geneColumnWidth
                                Layout.preferredHeight: 40
                                color: model.allele === "NA" ? "#FFFFE0" :
                                        rowLayout.rowIndex % 2 === 0 ? "#FFFFFF" : "#E3F2FD"
                                border.color: "black"
                                border.width: 1
                                Text {
                                    text: gene
                                    anchors.centerIn: parent
                                    elide: Text.ElideRight
                                    width: parent.width - 10
                                }
                            }





                            // SNP column
                            Rectangle {
                                Layout.fillWidth: true
                                Layout.preferredWidth: headerLayout.snpColumnWidth
                                Layout.preferredHeight: 40
                                color: model.allele === "NA" ? "#FFFFE0" :
                                        rowLayout.rowIndex % 2 === 0 ? "#FFFFFF" : "#E3F2FD"
                                border.color: "black"
                                border.width: 1
                                Text {
                                    text: snp
                                    anchors.centerIn: parent
                                    elide: Text.ElideRight
                                    width: parent.width - 10
                                }
                            }

                            // Allele column
                            Rectangle {
                                Layout.fillWidth: true
                                Layout.preferredWidth: headerLayout.alleleColumnWidth
                                Layout.preferredHeight: 40
                                color: model.allele === "NA" ? "#FFFFE0" :
                                        rowLayout.rowIndex % 2 === 0 ? "#FFFFFF" : "#E3F2FD"
                                border.color: "black"
                                border.width: 1
                                Text {
                                    text: {
                                        if (allele === "NA") return "NA";
                                        var parts = allele.split('-');
                                        return parts.length > 1 ? parts[parts.length-1] : allele;
                                    }
                                    anchors.centerIn: parent
                                    elide: Text.ElideRight
                                    width: parent.width - 10
                                }
                            }

                            // No. of Alleles column
                            Rectangle {
                                Layout.fillWidth: true
                                Layout.preferredWidth: headerLayout.noOfAllelesColumnWidth
                                Layout.preferredHeight: 40
                                color: model.allele === "NA" ? "#FFFFE0" :
                                        rowLayout.rowIndex % 2 === 0 ? "#FFFFFF" : "#E3F2FD"
                                border.color: "black"
                                border.width: 1

                                RowLayout {
                                    anchors.centerIn: parent
                                    spacing: 4
                                    visible: allele !== "NA"

                                    Component.onCompleted: {
                                        if (!["0", "1", "2", "NA"].includes(noOfAlleles)) {
                                            snpModel.set(rowLayout.rowIndex, {noOfAlleles: "0"})
                                        }
                                    }

                                    Repeater {
                                        id: optionRepeater
                                        model: ["0", "1", "2", "NA"]

                                        delegate: Button {
                                            id: control
                                            text: modelData
                                            checkable: true
                                            checked: noOfAlleles === modelData

                                            onClicked: {
                                                snpModel.set(rowLayout.rowIndex, {noOfAlleles: modelData})
                                            }

                                            background: Rectangle {
                                                radius: 4
                                                implicitWidth: 40
                                                implicitHeight: 24
                                                border.width: 1
                                                color: control.checked ? "#448AFF" : "#EEEEEE"
                                                opacity: control.checked ? 1 : 0.5
                                            }
                                            font.bold: control.checked
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        // Box 2: Predict Button
        Rectangle {
            id: predict_gene_expression_button
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            color: "#74b9ff"

            Button {
                anchors.centerIn: parent
                text: "Predict Gene Expression"
                onClicked: {
                    resultModel.clear()
                    var totalEffect = 0.0
                    for (var i = 0; i < snpModel.count; ++i) {
                        var item = snpModel.get(i)
                        if (item.allele !== "NA" && item.noOfAlleles !== "NA") {
                            var dosage = parseInt(item.noOfAlleles)
                            var effectInfo = snpDb.queryEffect(item.allele)

                            if (effectInfo && effectInfo.beta !== undefined) {
                                var beta = effectInfo.beta
                                var gene = effectInfo.gene
                                var effect = beta * dosage
                                totalEffect += effect

                                resultModel.append({
                                    snp: item.snp,
                                    allele: item.allele,
                                    noOfAlleles: dosage,
                                    gene: gene,
                                    trait: effectInfo.trait,
                                    beta: beta.toFixed(4),
                                    effect: effect.toFixed(4)
                                })
                            }
                        }
                    }


                }
            }
        }


        // Box 3: Results
        Rectangle {
            id: resultDisplay
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "#dfe6e9"

            ColumnLayout {
                anchors.fill: parent
                spacing: 0

                // Header row
                GridLayout {
                    id: resultHeaderLayout
                    Layout.fillWidth: true
                    columns: 6
                    rowSpacing: 0
                    columnSpacing: 0

                    property real colWidth: parent.width / 6

                    Rectangle {
                        Layout.preferredWidth: resultHeaderLayout.colWidth
                        Layout.preferredHeight: 30
                        color: "#f0f0f0"
                        border.color: "black"
                        border.width: 1
                        Text {
                            text: "Disease/Trait"; anchors.centerIn: parent; font.bold: true
                        }
                    }
                    Rectangle {
                        Layout.preferredWidth: resultHeaderLayout.colWidth
                        Layout.preferredHeight: 30
                        color: "#f0f0f0"
                        border.color: "black"
                        border.width: 1
                        Text {
                            text: "SNP"; anchors.centerIn: parent; font.bold: true
                        }
                    }
                    Rectangle {
                        Layout.preferredWidth: resultHeaderLayout.colWidth
                        Layout.preferredHeight: 30
                        color: "#f0f0f0"
                        border.color: "black"
                        border.width: 1
                        Text {
                            text: "Gene"; anchors.centerIn: parent; font.bold: true
                        }
                    }
                    Rectangle {
                        Layout.preferredWidth: resultHeaderLayout.colWidth
                        Layout.preferredHeight: 30
                        color: "#f0f0f0"
                        border.color: "black"
                        border.width: 1
                        Text {
                            text: "β"; anchors.centerIn: parent; font.bold: true
                        }
                    }
                    Rectangle {
                        Layout.preferredWidth: resultHeaderLayout.colWidth
                        Layout.preferredHeight: 30
                        color: "#f0f0f0"
                        border.color: "black"
                        border.width: 1
                        Text {
                            text: "Alleles"; anchors.centerIn: parent; font.bold: true
                        }
                    }
                    Rectangle {
                        Layout.preferredWidth: resultHeaderLayout.colWidth
                        Layout.preferredHeight: 30
                        color: "#f0f0f0"
                        border.color: "black"
                        border.width: 1
                        Text {
                            text: "Effect"; anchors.centerIn: parent; font.bold: true
                        }
                    }
                }

                // Results table
                ScrollView {
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    ListView {
                        id: resultListView
                        width: parent.width
                        height: parent.height
                        model: resultModel
                        clip: true
                        boundsBehavior: Flickable.StopAtBounds

                        delegate: GridLayout {
                            id: resultRowLayout
                            width: resultListView.width
                            height: 40
                            columns: 6
                            rowSpacing: 0
                            columnSpacing: 0

                            property int rowIndex: index
                            property real colWidth: width / 6

                            Rectangle {
                                Layout.preferredWidth: resultRowLayout.colWidth
                                Layout.preferredHeight: 40
                                color: rowIndex % 2 === 0 ? "#FFFFFF" : "#E3F2FD"
                                border.color: "black"
                                border.width: 1
                                Text {
                                    text: trait
                                    anchors.centerIn: parent
                                    elide: Text.ElideRight
                                    width: parent.width - 10
                                }
                            }
                            Rectangle {
                                Layout.preferredWidth: resultRowLayout.colWidth
                                Layout.preferredHeight: 40
                                color: rowIndex % 2 === 0 ? "#FFFFFF" : "#E3F2FD"
                                border.color: "black"
                                border.width: 1
                                Text {
                                    text: snp
                                    anchors.centerIn: parent
                                    elide: Text.ElideRight
                                    width: parent.width - 10
                                }
                            }
                            Rectangle {
                                Layout.preferredWidth: resultRowLayout.colWidth
                                Layout.preferredHeight: 40
                                color: rowIndex % 2 === 0 ? "#FFFFFF" : "#E3F2FD"
                                border.color: "black"
                                border.width: 1
                                Text {
                                    text: gene
                                    anchors.centerIn: parent
                                    elide: Text.ElideRight
                                    width: parent.width - 10
                                }
                            }
                            Rectangle {
                                Layout.preferredWidth: resultRowLayout.colWidth
                                Layout.preferredHeight: 40
                                color: rowIndex % 2 === 0 ? "#FFFFFF" : "#E3F2FD"
                                border.color: "black"
                                border.width: 1
                                Text {
                                    text: beta
                                    anchors.centerIn: parent
                                    elide: Text.ElideRight
                                    width: parent.width - 10
                                }
                            }
                            Rectangle {
                                Layout.preferredWidth: resultRowLayout.colWidth
                                Layout.preferredHeight: 40
                                color: rowIndex % 2 === 0 ? "#FFFFFF" : "#E3F2FD"
                                border.color: "black"
                                border.width: 1
                                Text {
                                    text: noOfAlleles
                                    anchors.centerIn: parent
                                    elide: Text.ElideRight
                                    width: parent.width - 10
                                }
                            }
                            Rectangle {
                                Layout.preferredWidth: resultRowLayout.colWidth
                                Layout.preferredHeight: 40
                                color: rowIndex % 2 === 0 ? "#FFFFFF" : "#E3F2FD"
                                border.color: "black"
                                border.width: 1
                                Text {
                                    text: effect
                                    anchors.centerIn: parent
                                    elide: Text.ElideRight
                                    width: parent.width - 10
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
