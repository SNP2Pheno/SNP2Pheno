//
// Created by Georg Seidlhuber on 25.11.25.
//

#include "Controller.h"
#include <qmetaobject.h>

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

void Controller::invokeAction(const QString& actionName) {
    QMetaObject::invokeMethod(this, actionName.toLatin1().constData());
}

void Controller::setSelectedFiles (const QVariantList &files) {
    m_selectedFiles = files;
    emit selectedFilesChanged();
}

void Controller::onPlaceholderData() {
    QVariantList placeholderData;

    QVariantMap row1;
    row1["id"] = 1;
    row1["name"] = "Alice";
    row1["age"] = 29;
    row1["department"] = "Engineering";
    row1["salary"] = 75000;
    row1["country"] = "USA";
    row1["email"] = "alice@example.com";
    placeholderData.append(row1);

    QVariantMap row2;
    row2["id"] = 2;
    row2["name"] = "Bob";
    row2["age"] = 36;
    row2["department"] = "Marketing";
    row2["salary"] = 65000;
    row2["country"] = "UK";
    row2["email"] = "bob@example.com";
    placeholderData.append(row2);

    QVariantMap row3;
    row3["id"] = 3;
    row3["name"] = "Charlie";
    row3["age"] = 41;
    row3["department"] = "Sales";
    row3["salary"] = 82000;
    row3["country"] = "Canada";
    row3["email"] = "charlie@example.com";
    placeholderData.append(row3);

    QVariantMap row4;
    row4["id"] = 4;
    row4["name"] = "Diana";
    row4["age"] = 33;
    row4["department"] = "Engineering";
    row4["salary"] = 78000;
    row4["country"] = "Germany";
    row4["email"] = "diana@example.com";
    placeholderData.append(row4);

    QVariantMap row5;
    row5["id"] = 5;
    row5["name"] = "Eve";
    row5["age"] = 27;
    row5["department"] = "Design";
    row5["salary"] = 68000;
    row5["country"] = "France";
    row5["email"] = "eve@example.com";
    placeholderData.append(row5);

    QVariantMap row6;
    row6["id"] = 6;
    row6["name"] = "Frank";
    row6["age"] = 45;
    row6["department"] = "Management";
    row6["salary"] = 95000;
    row6["country"] = "USA";
    row6["email"] = "frank@example.com";
    placeholderData.append(row6);

    QVariantMap row7;
    row7["id"] = 7;
    row7["name"] = "Grace";
    row7["age"] = 31;
    row7["department"] = "Engineering";
    row7["salary"] = 80000;
    row7["country"] = "Australia";
    row7["email"] = "grace@example.com";
    placeholderData.append(row7);

    QVariantMap row8;
    row8["id"] = 8;
    row8["name"] = "Henry";
    row8["age"] = 38;
    row8["department"] = "Sales";
    row8["salary"] = 71000;
    row8["country"] = "UK";
    row8["email"] = "henry@example.com";
    placeholderData.append(row8);

    QVariantMap row9;
    row9["id"] = 9;
    row9["name"] = "Iris";
    row9["age"] = 26;
    row9["department"] = "Marketing";
    row9["salary"] = 62000;
    row9["country"] = "Spain";
    row9["email"] = "iris@example.com";
    placeholderData.append(row9);

    QVariantMap row10;
    row10["id"] = 10;
    row10["name"] = "Jack";
    row10["age"] = 42;
    row10["department"] = "Engineering";
    row10["salary"] = 88000;
    row10["country"] = "USA";
    row10["email"] = "jack@example.com";
    placeholderData.append(row10);

    QVariantMap row11;
    row11["id"] = 11;
    row11["name"] = "Karen";
    row11["age"] = 35;
    row11["department"] = "HR";
    row11["salary"] = 67000;
    row11["country"] = "Canada";
    row11["email"] = "karen@example.com";
    placeholderData.append(row11);

    QVariantMap row12;
    row12["id"] = 12;
    row12["name"] = "Leo";
    row12["age"] = 29;
    row12["department"] = "Design";
    row12["salary"] = 70000;
    row12["country"] = "Italy";
    row12["email"] = "leo@example.com";
    placeholderData.append(row12);

    m_results = placeholderData;
    emit resultsChanged();
}

//TODO: implementation of each query