//
// Created by Georg Seidlhuber on 25.11.25.
//

#ifndef SNP2PHENO_PTT_CONTROLLER_H
#define SNP2PHENO_PTT_CONTROLLER_H
#include <QObject>
#include <QVariantList>
#include <QProperty>


class Controller : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QVariantList results READ results NOTIFY resultsChanged)

public:
    explicit Controller(QObject* parent = nullptr);

    //TODO: INVOKABLE for each query needed
    Q_INVOKABLE void startQuery(const QString& queryString);

    [[nodiscard]] QVariantList results() const { return m_results; }

    signals:
        void resultsChanged();

private:
    QVariantList m_results;
};


#endif //SNP2PHENO_PTT_CONTROLLER_H