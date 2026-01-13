
from Database.database_operations import Database


def snps_to_database(snpList, db: Database):
    for snp in snpList:
        if db.get_rsIDs().__contains__(snp):
            continue
        db.insert_rsID(snp)

if __name__ == '__main__':
    snp_ids = []
    with open('../GWAS/parsed_results_hair color.csv') as f:
    #with open('../GWAS/parsed_results_eye-color.csv') as f:
        lines = f.readlines()
        for line in lines[1:]:
            snp_ids.append(int(line.strip().split(';')[0].removeprefix('rs')))

    snp_ids = set(snp_ids)
    db = Database("SNP2Pheno.db")
    snps_to_database(snp_ids, db)