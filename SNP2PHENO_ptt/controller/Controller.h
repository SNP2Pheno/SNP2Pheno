//
// Created by Georg Seidlhuber on 25.11.25.
//

#ifndef SNP2PHENO_PTT_CONTROLLER_H
#define SNP2PHENO_PTT_CONTROLLER_H

#include <QVariantList>
#include <QProperty>
#include <VCFRecord.h>
#include "headers/FileData.h"

class Controller : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QVariantList results READ results NOTIFY resultsChanged)
    Q_PROPERTY(QStringList availableActions READ availableActions NOTIFY actionsChanged)
    Q_PROPERTY(QVariantList selectedFiles READ selectedFiles NOTIFY selectedFilesChanged)

public:
    explicit Controller(QObject* parent = nullptr);

    [[nodiscard]] QVariantList results() const { return m_results; }
    [[nodiscard]] QStringList availableActions() const;
    [[nodiscard]] QVariantList selectedFiles() const;

    Q_INVOKABLE fileParsedState requestFileStatus(const QString& fileName);

    signals:
        void resultsChanged();
        void actionsChanged();
        void selectedFilesChanged();
        void fileStatusChanged(const QString& fileName);

private:
    QVariantList m_results = QVariantList();
    QMap<QString, fileData> m_selectedFiles = QMap<QString, fileData>();
    static std::vector<vcf::VCFRecord> parseVCF(const QString &fileName);
    static std::vector<vcf::VCFRecord> parseTXT(const QString &fileName);

public slots:
    void invokeAction(const QString& actionName);
    void addSelectedFiles(const QVariantList &files);
    void clearSelectedFiles();
    void startParsing(QString const& fileName);

private slots:
    void onPlaceholderData();
};


#endif //SNP2PHENO_PTT_CONTROLLER_H