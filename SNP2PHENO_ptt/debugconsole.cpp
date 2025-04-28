#include "debugconsole.h"
#include <QMetaObject>

DebugConsole* DebugConsole::instance()
{
    static DebugConsole* s_instance = new DebugConsole();
    return s_instance;
}

DebugConsole::DebugConsole(QObject* parent)
    : QObject(parent)
{
}

QString DebugConsole::log() const
{
    return m_log;
}

void DebugConsole::setLog(const QString& newLog)
{
    if (m_log != newLog) {
        m_log = newLog;
        emit logChanged();
    }
}

void DebugConsole::appendLog(const QString& message)
{
    // Split current log text into lines (ignoring empty lines)
    QStringList lines = m_log.split("\n", Qt::SkipEmptyParts);
    // Append the new message
    lines.append(message);
    // Remove the oldest lines if there are more than 100
    while (lines.size() > 100) {
        lines.removeFirst();
    }
    m_log = lines.join("\n");
    emit logChanged();
}
