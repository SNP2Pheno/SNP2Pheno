#include "vcfparsercontroller.h"
#include "vcfworker.h"
#include <QThread>
#include <QDebug>

VcfParserController::VcfParserController(QObject* parent)
    : QObject(parent)
{
}

void VcfParserController::startParsing(const QString& fileUrl)
{
    QThread* thread = new QThread;
    VcfWorker* worker = new VcfWorker(fileUrl);
    worker->moveToThread(thread);

    connect(thread, &QThread::started, worker, &VcfWorker::process);

    // Speichere das Ergebnis, wenn der Worker fertig ist.
    connect(worker, &VcfWorker::finished, this, [=](const QStringList& result) {
        m_snpList = result;
        emit snpListChanged();  // Signal, damit QML die Änderung mitbekommt
        qDebug() << "VCF parsing finished. Total SNP tokens:" << result.size();
        });

    connect(worker, &VcfWorker::finished, thread, &QThread::quit);
    connect(worker, &VcfWorker::finished, worker, &QObject::deleteLater);
    connect(thread, &QThread::finished, thread, &QObject::deleteLater);

    thread->start();
}
