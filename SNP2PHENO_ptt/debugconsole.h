#ifndef DEBUGCONSOLE_H
#define DEBUGCONSOLE_H

#include <QObject>
#include <QString>

class DebugConsole : public QObject
{
    Q_OBJECT
        Q_PROPERTY(QString log READ log WRITE setLog NOTIFY logChanged)
public:
    static DebugConsole* instance();
    explicit DebugConsole(QObject* parent = nullptr);

    QString log() const;
    void setLog(const QString& newLog);

public slots:
    void appendLog(const QString& message);

signals:
    void logChanged();

private:
    QString m_log;
};

#endif // DEBUGCONSOLE_H
