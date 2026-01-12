//
// Created by Georg Seidlhuber on 25.11.25.
//

#include "Controller.h"
#include <VCFParser.h>
#include <qmetaobject.h>
#include <QtConcurrent/QtConcurrentRun>
#include <QFuture>
#include <QFutureWatcher>
#include <iostream>
#include <qurl.h>
#include <ranges>
#include <regex>
#include "sources/subprocess.hpp"

using std::cout;

Controller::Controller(QObject* parent) : QObject(parent) {}

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

QVariantList Controller::selectedFiles() const {
    QVariantList out;
    for (const QString& filePath : m_selectedFiles.keys()) {
        out.append(filePath);
    }
    return out;
}

fileParsedState Controller::requestFileStatus(const QString &fileName) {
    if (m_selectedFiles.contains(fileName)) {
        return m_selectedFiles[fileName].state;
    }
    return parsedError;
}

void Controller::invokeAction(const QString& actionName) {
    QMetaObject::invokeMethod(this, actionName.toLatin1().constData());
}

void Controller::addSelectedFiles(const QVariantList &files) {
    for (const QVariant &v : files) {
        QString filePath = v.toString();
        if (!m_selectedFiles.contains(filePath)) {
            m_selectedFiles[filePath] = fileData();
        }
    }
    emit selectedFilesChanged();
}

void Controller::clearSelectedFiles() {
    m_selectedFiles.clear();
    emit selectedFilesChanged();
}

void Controller::startParsing(const QString &fileName) {
    if (!m_selectedFiles.contains(fileName)) {
        m_selectedFiles[fileName] = fileData();
    }
    if (!m_selectedFiles[fileName].rsIDs.empty()) {
        return;
    }

    const QString localPath = QUrl(fileName).toLocalFile();

    QString ext;
    if (fileName.endsWith(".vcf")) {
        ext = "vcf";
    } else if (fileName.endsWith(".txt")) {
        ext = "txt";
    } else {
        m_selectedFiles[fileName].state = parsedError;
        emit fileStatusChanged(fileName);
        return;
    }

    m_selectedFiles[fileName].state = parsing;
    emit fileStatusChanged(fileName);

    auto future = QtConcurrent::run([this, localPath, ext]() -> std::map<std::string, std::string> {
        if (ext == "vcf") {
            return parseVCF(localPath);
        }
        if (ext == "txt") {
            return parseTXT(localPath);
        }
        return {};
    });

    auto *watcher = new QFutureWatcher<std::map<std::string, std::string>>(this);

    connect(watcher, &QFutureWatcher<std::map<std::string, std::string>>::finished,
            this, [this, watcher, fileName]() {
        auto future = watcher->future();
        std::map<std::string, std::string> records = future.result();
        watcher->deleteLater();

        if (records.empty()) {
            m_selectedFiles[fileName].state = parsedError;
            emit fileStatusChanged(fileName);
            return;
        }

        m_selectedFiles[fileName].rsIDs = records;
        m_selectedFiles[fileName].state = parsedSuccessfully;

        emit fileStatusChanged(fileName);
        emit resultsChanged();
    });

    watcher->setFuture(future);
}

void Controller::showResult(QString const &fileName) {
    m_results.clear();
    m_results = m_selectedFiles[fileName].results;
    emit resultsChanged();
}

std::map<std::string, std::string> Controller::parseVCF(const QString &fileName) {
    try {
        vcf::VCFParser parser{fileName.toStdString()};
        std::map<std::string, std::string> rsIDs = {};
        for (const vcf::VCFRecord &record : parser.parseAll()) {
            auto [id, allele] = record.decodeAlleles();
            if (id.length() >= 3) {
                rsIDs[id] = allele;
            }
        }
        return rsIDs;
    } catch (...) {
        return {};
    }
}

std::map<std::string, std::string> Controller::parseTXT(const QString &fileName) {
    try {
        auto p = subprocess::Popen(
            {"python3", "-u", "../controller/sources/23andme_parse.py",
             fileName.toStdString()},
            subprocess::output{subprocess::PIPE}
        );
        auto res = p.communicate();
        std::string output(res.first.buf.data(), res.first.length);

        std::regex pattern(R"(\['(rs\d+)',\s*'([ACGT])'\])");
        std::smatch match;

        std::string::const_iterator search_start(output.cbegin());
        std::map<std::string, std::string> rsIDs = {};

        while (std::regex_search(search_start, output.cend(), match, pattern)) {
            std::string id = match[1].str();
            std::string allele    = match[2].str();

            rsIDs[id] = allele;

            search_start = match.suffix().first;
        }

        return rsIDs;
    } catch (...) {
        return {};
    }
}