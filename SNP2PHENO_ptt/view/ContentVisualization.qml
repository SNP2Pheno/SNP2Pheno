import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtWebEngine 1.15

Rectangle {
    Layout.fillWidth: true
    Layout.fillHeight: true

    color: "transparent"

    WebEngineView {
        id: webview
        anchors.fill: parent
        settings.localContentCanAccessRemoteUrls: true
        url: Qt.resolvedUrl("../Visualization/index.html")
    }
}