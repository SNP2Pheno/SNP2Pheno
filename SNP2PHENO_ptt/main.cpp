#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QIcon>

int main(int argc, char* argv[])
{
	QGuiApplication app(argc, argv);

	app.setWindowIcon(QIcon("../images/ICONV6.ico"));

	QQmlApplicationEngine engine;

	engine.load(QUrl::fromLocalFile("../main.qml"));
	if (engine.rootObjects().isEmpty())
		return -1;

	return app.exec();
}
