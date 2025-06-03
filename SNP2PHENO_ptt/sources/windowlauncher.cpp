#include "../headers/windowlauncher.h"
#include <QQmlApplicationEngine>
#include <QUrl>

void WindowLauncher::openAFQEditor() {
    auto* engine = new QQmlApplicationEngine();
    engine->load(QUrl("../AFQEditor.qml"));  // später im Resource-System!
}
