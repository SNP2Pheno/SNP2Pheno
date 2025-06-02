import sqlite3

class Database:
    db = None
    cur = None

    def __init__(self, file):
        self.db = sqlite3.connect(file)
        self.cur = self.db.cursor()

    def get_rsIDs(self):
        self.cur.execute("SELECT rs_ID FROM SNP_TABLE")
        data = list()
        for row in self.cur.fetchall():
            data.append(row[0])
        return data

    def insert_disease(self, association, alleleID):
        # insert into GWAS table
        GWAS_ID = self.__insert_GWAS(association)

        # insert into disease table
        self.cur.execute("INSERT INTO DISEASE_TABLE \
            (Allele_ID, GWAS_ID, Disease, Effect) \
            Values(?,?,?,?)",
            [alleleID,
            GWAS_ID,
            association.traitName,
            association.expression])

    def insert_appearance(self, association, alleleID):
        GWAS_ID = self.__insert_GWAS(association)
        self.cur.execute("INSERT INTO APPEARANCE_TABLE \
            (Allele_ID, GWAS_ID, Phenotype, Expression) \
            VALUES (?,?,?,?)",
            [alleleID,
            GWAS_ID,
            association.traitName,
            association.expression])

    def __insert_GWAS(self, association):
        self.cur.execute("INSERT INTO GWAS_TABLE \
            (PValueMantissa,\
            PValueExponent,\
            OR_value,\
            betaNum,\
            betaUnit,\
            betaDirection,\
            CI_min,\
            CI_max) \
            VALUES (?,?,?,?,?,?,?,?)",
            [association.pValueMantissa,
            association.pValueExponent,
            association.orValue,
            association.betaNum,
            association.betaUnit,
            association.betaDirection,
            association.CIMin,
            association.CIMax])
        self.db.commit()

        return self.cur.lastrowid

    def insert_allele(self, rsID):
        self.cur.execute("INSERT INTO ALLELE_TABLE \
            (rs_ID, Allele_1, Allele_2) \
            VALUES (?,?,?)",
            [rsID, "NA", "NA"])
        return self.cur.lastrowid

    def commit(self):
        self.db.commit()