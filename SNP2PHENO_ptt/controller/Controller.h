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

public:
    explicit Controller(QObject* parent = nullptr);

    [[nodiscard]] QVariantList results() const { return m_results; }
    [[nodiscard]] QStringList availableActions() const;

    signals:
        void resultsChanged();
        void actionsChanged();

private:
    QVariantList m_results;

public slots:
    void invokeAction(const QString& actionName);

private slots:
    void onPlaceholderData();
};


#endif //SNP2PHENO_PTT_CONTROLLER_H