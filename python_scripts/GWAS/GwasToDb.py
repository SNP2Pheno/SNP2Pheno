from parse_GWAS import parseSNP
from Association import Association, TYPE
from Database.database_operations import Database

class GwasToDb:
    db: Database = None

    def __init__(self, filename):
        if filename is None:
            return
        self.db = Database(filename)

    def insert_association(self, association, alleleID):
        if association is None:
            return

        if association.type == TYPE.DISEASE:
            self.db.insert_disease(association, alleleID)

        if association.type == TYPE.APPEARANCE:
            self.db.insert_appearance(association, alleleID)

    def run(self):
        rsIDs = self.db.get_rsIDs()
        for ID in rsIDs:
            alleleID = self.db.insert_allele(ID)
            for association in parseSNP("rs" + str(ID)):
                self.insert_association(association, alleleID)
                self.db.commit()

if __name__ == "__main__":
    gwas = GwasToDb("../Database/SNP2Pheno.db")
    gwas.run()