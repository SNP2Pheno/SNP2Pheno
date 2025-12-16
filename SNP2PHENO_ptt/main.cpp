#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <qqml.h>
#include "headers/vcf_to_snp.h"
#include "headers/windowlauncher.h"
#include <iostream>
#include "headers/vcfparsercontroller.h"
#include <QQmlContext>
#include "headers/snpdatabase.h"
#include <QIcon>

#include <QMessageLogContext>
#include <QString>

void myMessageHandler(QtMsgType type, const QMessageLogContext& context, const QString& msg)
{
	// Only forward messages from "vcf_to_snp.cpp" to the QML debug console.
	QString fileName = QString(context.file);
	if (!fileName.contains("vcf_to_snp.cpp"))
	{
		// Output messages from other files to standard output.
		std::cout << msg.toStdString() << std::endl;
		return;
	}
}



int main(int argc, char* argv[])
{
#if defined(Q_OS_WIN) && QT_VERSION_CHECK(6, 9, 0) <= QT_VERSION && QT_VERSION < QT_VERSION_CHECK(6, 9, 0)
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
#endif

    qputenv("QML_XHR_ALLOW_FILE_READ", QByteArray("1"));
    QGuiApplication app(argc, argv);

  app.setWindowIcon(QIcon(":/images/ICONV6.ico"));

    // Register VcfToSnp with QML under the module "MyApp"
    qmlRegisterType<VcfToSnp>("MyApp", 1, 0, "VcfToSnp");

    qmlRegisterType<SnpDatabase>("QueryApp", 1, 0, "SnpDatabase");

    // Installiere den eigenen Message Handler
    qInstallMessageHandler(myMessageHandler);


    QQmlApplicationEngine engine;

    VcfParserController* parserController = new VcfParserController();
    engine.rootContext()->setContextProperty("vcfParser", parserController);

    WindowLauncher windowLauncher;
    engine.rootContext()->setContextProperty("windowLauncher", &windowLauncher);

    engine.load(QUrl("qrc:/QML/main.qml"));
    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}

