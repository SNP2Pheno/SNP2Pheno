#include "../headers/vcfworker.h"
#include <QDebug>
#include "../headers/vcf_to_snp.h"

VcfWorker::VcfWorker(const QString& fileUrl, QObject* parent)
    : QObject(parent), m_fileUrl(fileUrl)
{
}

void VcfWorker::process()
{
    VcfToSnp vcfToSnp;
    QStringList result = vcfToSnp.parseVCF(m_fileUrl);
    emit finished(result);
}
