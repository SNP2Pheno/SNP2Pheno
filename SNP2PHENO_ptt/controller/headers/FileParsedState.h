//
// Created by Georg Seidlhuber on 15.12.25.
//

#ifndef SNP2PHENO_PTT_FILEPARSEDSTATE_H
#define SNP2PHENO_PTT_FILEPARSEDSTATE_H

enum fileParsedState {
    idle,
    parsing,
    parsedSuccessfully,
    parsedError
};

#endif //SNP2PHENO_PTT_FILEPARSEDSTATE_H