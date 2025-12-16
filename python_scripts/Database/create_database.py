import sqlite3
from sqlite3 import OperationalError

con = sqlite3.connect("SNP2Pheno.db")

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
    con.execute('DROP TABLE GWAS_TABLE')
except OperationalError as OE:
    if OE.sqlite_errorcode == 1:
        pass
    else:
        raise OE
con.execute("CREATE TABLE if not exists GWAS_TABLE (                \
            ID integer primary key autoincrement,                   \
            RiskAllele text,                                        \
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
            ID integer primary key autoincrement,                   \
            Allele_ID integer,                                      \
            GWAS_ID integer,                                        \
            Phenotype text,                                         \
            Expression text,                                        \
            FOREIGN KEY (Allele_ID) REFERENCES ALLELE_TABLE(ID),    \
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
            GWAS_ID integer,                                        \
            Disease text,                                           \
            Effect text,                                            \
            FOREIGN KEY (Allele_ID) REFERENCES ALLELE_TABLE(ID),    \
            FOREIGN KEY (GWAS_ID) REFERENCES GWAS_TABLE(ID)         \
            )")


try:
    con.execute('DROP TABLE MODEL_TABLE')
except OperationalError as OE:
    if OE.sqlite_errorcode == 1:
        pass
    else:
        raise OE
con.execute("CREATE TABLE if not exists MODEL_TABLE (                       \
            ID integer primary key autoincrement,                           \
            Path_To_Model text NOT NULL,                                    \
            Appearance_ID integer,                                          \
            FOREIGN KEY (Appearance_ID) REFERENCES APPEARANCE_TABLE(ID)      \
            )")

try:
    con.execute('DROP TABLE RELEVANT_SNPS_CLUST_CLASS_TABLE')
except OperationalError as OE:
    if OE.sqlite_errorcode == 1:
        pass
    else:
        raise OE
con.execute("CREATE TABLE if not exists RELEVANT_SNPS_CLUST_CLASS_TABLE (         \
            MODEL_ID integer,                                               \
            SNP_ID integer,                                                 \
            PRIMARY KEY (MODEL_ID, SNP_ID),                                 \
            FOREIGN KEY (MODEL_ID) REFERENCES MODEL_TABLE(ID),              \
            FOREIGN KEY (SNP_ID) REFERENCES SNP_TABLE(rs_ID)                \
            )")

try:
    con.execute('DROP TABLE PHANTOM_PIC_IDENTIFIERS_TABLE')
except OperationalError as OE:
    if OE.sqlite_errorcode == 1:
        pass
    else:
        raise OE
con.execute("CREATE TABLE if not exists PHANTOM_PIC_IDENTIFIERS_TABLE (          \
            ID integer primary key autoincrement,                           \
            Path_Identifier TEXT NOT NULL,                                        \
            Identifier_Value TEXT NOT NULL,                                   \
            Model_ID integer,                                               \
            FOREIGN KEY (Model_ID) REFERENCES MODEL_TABLE(ID)               \
            )")

con.close()