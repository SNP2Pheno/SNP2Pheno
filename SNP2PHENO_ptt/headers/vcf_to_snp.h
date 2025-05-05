#ifndef VCF_TO_SNP_H
#define VCF_TO_SNP_H

#include <QObject>
#include <QString>
#include <QStringList>

class VcfToSnp : public QObject {
    Q_OBJECT
public:

    explicit VcfToSnp(QObject* parent = nullptr);

    // Expose the function so QML can call it.
    Q_INVOKABLE QStringList parseVCF(const QString& filePath);
};

#endif // VCF_TO_SNP_H
