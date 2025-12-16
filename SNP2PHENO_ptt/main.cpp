#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QIcon>
#include <QQmlContext>
#include "controller/Controller.h"

int main(int argc, char* argv[])
{
	QGuiApplication app(argc, argv);

	QGuiApplication::setWindowIcon(QIcon(ICON_PATH_CPP));

	QQmlApplicationEngine engine;

	Controller controller;
	engine.rootContext()->setContextProperty("controller", &controller);

	engine.load(QUrl::fromLocalFile(MAIN_QML_PATH));

	return QGuiApplication::exec();
}
