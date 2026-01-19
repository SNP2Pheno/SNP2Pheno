//
// Created by Georg Seidlhuber on 25.11.25.
//

#include "Controller.h"
#include "../database/DatabaseManager.h"
#include <qmetaobject.h>
#include <QDebug>

Controller::Controller(QObject* parent)
    : QObject(parent), m_dbManager(new DatabaseManager(this))
{
    initializeDatabase();
}

Controller::~Controller()
{
    delete m_dbManager;
}

void Controller::initializeDatabase()
{
    if (m_dbManager->openDb("SNP2Pheno.db")) {
        if (m_dbManager->createTables()) {
            if (m_dbManager->insertSampleData()) {
                m_results = m_dbManager->getInitialData();
                emit resultsChanged();
            } else {
                qDebug() << "Failed to insert sample data.";
            }
        } else {
            qDebug() << "Failed to create tables.";
        }
    } else {
        qDebug() << "Failed to open database.";
    }
}

QStringList Controller::availableActions() const {
    QStringList actions;
    const QMetaObject* meta = metaObject();

    for (int i = 0; i < meta->methodCount(); ++i) {
        QMetaMethod method = meta->method(i);
        QString name = method.name();

        if (name.startsWith("on") && method.methodType() == QMetaMethod::Slot) {
            actions.append(name);
        }
    }

    return actions;
}

QVariantList Controller::selectedFiles() const
{
    QStringList list = QStringList(m_selectedFiles.cbegin(), m_selectedFiles.cend());
    list.sort();

    QVariantList out;
    out.reserve(list.size());
    for (const auto &s : list)
        out << s;

    return out;
}

void Controller::invokeAction(const QString& actionName) {
    if (actionName == "onPlaceholderData") {
        // This is now handled by the database initialization
        return;
    }
    QMetaObject::invokeMethod(this, actionName.toLatin1().constData());
}

void Controller::addSelectedFiles (const QVariantList &files) {
    for (const QVariant &v : files) {
        m_selectedFiles.insert(v.toString());
    }
    emit selectedFilesChanged();
}

void Controller::clearSelectedFiles() {
    m_selectedFiles.clear();
    emit resultsChanged();
}

void Controller::onPlaceholderData() {
    // This function is no longer used, database is the source of truth.
    // Kept to avoid breaking existing QML if it's referenced by name,
}

//TODO: implementation of each query