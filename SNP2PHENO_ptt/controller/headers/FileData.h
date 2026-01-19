//
// Created by Georg Seidlhuber on 15.12.25.
//

#ifndef SNP2PHENO_PTT_FILEDATA_H
#define SNP2PHENO_PTT_FILEDATA_H

#include "FileParsedState.h"

struct fileData {
    fileParsedState state = idle;
    std::map<std::string, std::string> rsIDs {};
    QVariantList results{
        QVariantMap{
            {"No data available", QVariant()}
        }
    };
};

#endif //SNP2PHENO_PTT_FILEDATA_H