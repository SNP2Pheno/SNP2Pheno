import sqlite3
from sqlite3 import OperationalError

con = sqlite3.connect("../python_scripts/GWAS/SNP2Pheno.db")

try:
    con.execute('DROP TABLE SNP_TABLE')
except OperationalError as OE:
    if OE.sqlite_errorcode == 1:
        pass
    else:
        raise OE

con.execute("CREATE TABLE if not exists SNP_TABLE (                  \
            rs_ID integer primary key,                               \
            Ref text,                                                \
            Genesymbol text                                          \
            )")

try:
    con.execute('DROP TABLE CUSTOMSET_TABLE')
except OperationalError as OE:
    if OE.sqlite_errorcode == 1:
        pass
    else:
        raise OE

con.execute("CREATE TABLE if not exists CUSTOMSET_TABLE (           \
            ID integer primary key,                                 \
            name text NOT NULL,                                     \
            username text,                                          \
            createdAt DATETIME DEFAULT CURRENT_TIMESTAMP            \
            )")

try:
    con.execute('DROP TABLE CUSTOMSETALLELE_TABLE')
except OperationalError as OE:
    if OE.sqlite_errorcode == 1:
        pass
    else:
        raise OE

con.execute("CREATE TABLE if not exists CUSTOMSETALLELE_TABLE (                   \
            CustomSet_ID integer primary key,                               \
            Allele_ID integer,                                              \
            FOREIGN KEY (CustomSet_ID) REFERENCES CUSTOMSET_TABLE (ID),     \
            FOREIGN KEY (Allele_ID) REFERENCES ALLELE_TABLE (ID)            \
            )")

try:
    con.execute('DROP TABLE ALLELE_TABLE')
except OperationalError as OE:
    if OE.sqlite_errorcode == 1:
        pass
    else:
        raise OE
con.execute("CREATE TABLE if not exists ALLELE_TABLE (              \
            ID integer primary key autoincrement,                   \
            rs_ID integer,                                          \
            Allele_1 text NOT NULL,                                 \
            Allele_2 text NOT NULL,                                 \
            FOREIGN KEY (rs_ID) REFERENCES SNP_TABLE (rs_ID)        \
            )")

try:
    con.execute('DROP TABLE PHENO_TABLE')
except OperationalError as OE:
    if OE.sqlite_errorcode == 1:
        pass
    else:
        raise OE

con.execute("CREATE TABLE if not exists PHENO_TABLE (               \
            ID integer primary key autoincrement,                   \
            Phenotype text NOT NULL,                                \
            Expression text NOT NULL                                \
            )")

try:
    con.execute('DROP TABLE GWAS_TABLE')
except OperationalError as OE:
    if OE.sqlite_errorcode == 1:
        pass
    else:
        raise OE
con.execute("CREATE TABLE if not exists GWAS_TABLE (                \
            ID integer primary key autoincrement,                   \
            PValueMantissa integer,                                 \
            PValueExponent integer,                                 \
            OR_value real,                                          \
            betaNum real,                                          \
            betaUnit text,                                         \
            betaDirection text,                                   \
            CI_min real,                                            \
            CI_max real                                             \
            )")


try:
    con.execute('DROP TABLE APPEARANCE_TABLE')
except OperationalError as OE:
    if OE.sqlite_errorcode == 1:
        pass
    else:
        raise OE
con.execute("CREATE TABLE if not exists APPEARANCE_TABLE (          \
            Allele_ID integer,                                      \
            Pheno_ID integer,                                       \
            GWAS_ID integer,                                        \
            FOREIGN KEY (Allele_ID) REFERENCES ALLELE_TABLE(ID),    \
            FOREIGN KEY (Pheno_ID) REFERENCES PHENO_TABLE(ID),      \
            FOREIGN KEY (GWAS_ID) REFERENCES GWAS_TABLE(ID)         \
            )")


try:
    con.execute('DROP TABLE DISEASE_TABLE')
except OperationalError as OE:
    if OE.sqlite_errorcode == 1:
        pass
    else:
        raise OE
con.execute("CREATE TABLE if not exists DISEASE_TABLE (             \
            Allele_ID integer,                                      \
            Pheno_ID integer,                                       \
            Uniprot_Note text,                                      \
            GWAS_ID integer,                                        \
            FOREIGN KEY (Allele_ID) REFERENCES ALLELE_TABLE(ID),    \
            FOREIGN KEY (Pheno_ID) REFERENCES PHENO_TABLE(ID),      \
            FOREIGN KEY (GWAS_ID) REFERENCES GWAS_TABLE(ID)         \
            )")

