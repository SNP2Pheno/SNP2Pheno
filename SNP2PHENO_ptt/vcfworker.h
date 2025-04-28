#ifndef VCFWORKER_H
#define VCFWORKER_H

#include <QObject>
#include <QString>
#include <QStringList>

class VcfWorker : public QObject
{
    Q_OBJECT
public:
    explicit VcfWorker(const QString& fileUrl, QObject* parent = nullptr);

    public slots:
        void process();

    signals:
        void finished(const QStringList& result);

private:
    QString m_fileUrl;
};

#endif // VCFWORKER_H
