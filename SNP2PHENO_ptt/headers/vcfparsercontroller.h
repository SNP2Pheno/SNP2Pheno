#ifndef VCFPARSERCONTROLLER_H
#define VCFPARSERCONTROLLER_H

#include <QObject>
#include <QStringList>

class VcfParserController : public QObject
{
    Q_OBJECT
        Q_PROPERTY(QStringList snpList READ snpList NOTIFY snpListChanged)
public:
    explicit VcfParserController(QObject* parent = nullptr);

    QStringList snpList() const { return m_snpList; }

public slots:
    void startParsing(const QString& fileUrl);

signals:
    void snpListChanged();

private:
    QStringList m_snpList;
};

#endif // VCFPARSERCONTROLLER_H
