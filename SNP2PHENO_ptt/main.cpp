#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QIcon>
#include <QQmlContext>
#include "controller/Controller.h"

int main(int argc, char* argv[])
{
	QGuiApplication app(argc, argv);

	QGuiApplication::setWindowIcon(QIcon("../images/ICONV6.ico"));

	QQmlApplicationEngine engine;

	Controller controller;
	engine.rootContext()->setContextProperty("controller", &controller);

	engine.load(QUrl::fromLocalFile("../main.qml"));

	return QGuiApplication::exec();
}
