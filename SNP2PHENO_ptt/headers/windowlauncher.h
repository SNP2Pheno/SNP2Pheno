#ifndef WINDOWLAUNCHER_H
#define WINDOWLAUNCHER_H

#include <QObject>

class WindowLauncher : public QObject {
    Q_OBJECT
public:
    Q_INVOKABLE void openAFQEditor();
};

#endif // WINDOWLAUNCHER_H
