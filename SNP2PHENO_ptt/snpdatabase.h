// snpdatabase.h
#ifndef SNPDATABASE_H
#define SNPDATABASE_H

#include <QObject>
#include <QStringList>
#include <QSqlDatabase>
#include <QSqlQuery>
#include <QSqlError>
#include <QVariantList>

class SnpDatabase : public QObject
{
    Q_OBJECT
public:
    explicit SnpDatabase(QObject *parent = nullptr);

    Q_INVOKABLE QVariantList querySnp(const QString &snpId);

    Q_INVOKABLE QVariantMap queryEffect(const QString &snpId_R_allele);

private:
    QSqlDatabase db;
};

#endif // SNPDATABASE_H
