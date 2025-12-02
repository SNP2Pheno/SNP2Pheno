//
// Created by Georg Seidlhuber on 25.11.25.
//

#ifndef SNP2PHENO_PTT_CONTROLLER_H
#define SNP2PHENO_PTT_CONTROLLER_H

#include <QVariantList>
#include <QProperty>

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
    [[nodiscard]] QVariantList selectedFiles() const
    {   QVariantList out;
        out.reserve(m_selectedFiles.size());
        for (const auto &s : m_selectedFiles)
            out << s;
        return out;
    }

    signals:
        void resultsChanged();
        void actionsChanged();
        void selectedFilesChanged();

private:
    QVariantList m_results = QVariantList();
    QSet<QString> m_selectedFiles = QSet<QString>();

public slots:
    void invokeAction(const QString& actionName);
    void addSelectedFiles(const QVariantList &files);
    void clearSelectedFiles();

private slots:
    void onPlaceholderData();
};


#endif //SNP2PHENO_PTT_CONTROLLER_H