#include "vcfworker.h"
#include <QDebug>
#include "vcf_to_snp.h"

VcfWorker::VcfWorker(const QString& fileUrl, QObject* parent)
    : QObject(parent), m_fileUrl(fileUrl)
{
}

void VcfWorker::process()
{
    qDebug() << "Worker: process() gestartet";
    VcfToSnp vcfToSnp;
    QStringList result = vcfToSnp.parseVCF(m_fileUrl);
    qDebug() << "Worker: Parsing beendet, Ergebnisgröße:" << result.size();
    emit finished(result);
}
