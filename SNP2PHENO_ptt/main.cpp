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

	engine.load(QUrl::fromLocalFile("../main.qml"));
	if (engine.rootObjects().isEmpty())
		return -1;

	Controller controller;
	engine.rootContext()->setContextProperty("controller", &controller);

	return QGuiApplication::exec();
}
