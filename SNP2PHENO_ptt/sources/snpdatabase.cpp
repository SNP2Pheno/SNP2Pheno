// snpdatabase.cpp
#include "../headers/snpdatabase.h"
#include <QDebug>


SnpDatabase::SnpDatabase(QObject *parent) : QObject(parent)
{
    db = QSqlDatabase::addDatabase("QSQLITE");
    //db.setDatabaseName("gwas_data.db");  // adjust path if needed
    db.setDatabaseName("../gwas_data.db");

    if (!db.open()) {
        qWarning() << "Failed to open database:" << db.lastError().text();
    }
}

QVariantList SnpDatabase::querySnp(const QString &snpId)
{
    QVariantList results;

    if (!db.isOpen()) {
        qWarning() << "Database not open!";
        return results;
    }

    QSqlQuery query;
    query.prepare("SELECT \"STRONGEST SNP-RISK ALLELE\", \"MAPPED_GENE\" FROM gwas_snps WHERE \"SNPS\" = :snpid");

    query.bindValue(":snpid", snpId);

    if (!query.exec()) {
        qWarning() << "Query failed:" << query.lastError().text();
        return results;
    } else {
        qDebug() << "Query OK";
    }

    while (query.next()) {
        QString allele = query.value(0).toString();
        QString gene = query.value(1).toString();
        results.append(QVariantMap{{"snp", snpId}, {"allele", allele}, {"gene", gene}});
    }

    return results;
}

QVariantMap SnpDatabase::queryEffect(const QString &snpId_R_allele) {
    QVariantMap result;
    QSqlQuery query;
    query.prepare(R"(
        SELECT "DISEASE/TRAIT", "MAPPED_GENE", "OR or BETA"
        FROM gwas_snps
        WHERE "STRONGEST SNP-RISK ALLELE" = :snpId_R_allele
        COLLATE NOCASE
    )");
    query.bindValue(":snpId_R_allele", snpId_R_allele.trimmed());

    if (!query.exec()) {
        qDebug() << "Query failed:" << query.lastError().text();
        return result;
    }

    while (query.next()) {
        QString trait = query.value(0).toString();
        QString gene = query.value(1).toString();
        QString val = query.value(2).toString();

        bool ok = false;
        double beta = val.toDouble(&ok);

        qDebug() << "beta value:" << beta;

        if (ok) {
            if (beta > 0.0 && beta < 10.0) {
                beta = std::log(beta);
            }
            result["trait"] = trait;
            result["gene"] = gene;
            result["beta"] = beta;
            return result;
        }
    }

    return result;
}
