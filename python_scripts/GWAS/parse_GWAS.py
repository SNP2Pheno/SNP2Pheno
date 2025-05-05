import sqlite3

import requests

def parseSNP(snpID):
    con = sqlite3.connect("SNP2Pheno.db")

    link = "https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/" + snpID + "/associations"
    response = requests.get(link)
    if response.status_code == 200:

        # check if SNP already exists in the database
        cursor = con.execute('''
            SELECT 1 FROM SNP_TABLE WHERE rs_ID = ?
        ''', (int(snpID.replace("rs", "")),))
        # if it exists, update it
        if cursor.fetchone() is None:
            # if not, insert it
            con.execute('''
                INSERT INTO SNP_TABLE (rs_ID, Ref) VALUES (?, ?)
            ''', (int(snpID.replace("rs", "")), "Unknown"))
            con.commit()

        data = response.json()
        for association in data['_embedded']['associations']:
            pValueExponent = 0
            pValueMantisse = 0
            orValue = 0.0
            CIMax = 0.0
            CIMin = 0.0
            expression = "Unknown"

            if association.get('pvalueMantissa') is not None and association.get('pvalueExponent') is not None:
                pValueMantisse = association.get('pvalueMantissa')
                pValueExponent = association.get('pvalueExponent')
            if association.get('orPerCopyNum') is not None:
                orValue = association.get('orPerCopyNum')
            if association.get('range') is not None and association.get('range') != '[NR]':
                CIMin = association.get('range')[1:].split('-')[0]
                CIMax = association.get('range')[:-1].split('-')[1]
            if association.get('pvalueDescription') is not None:
                expression = association.get('pvalueDescription')
            trait = association.get('_links').get('efoTraits')

            response_trait = requests.get(trait.get('href'))
            if response_trait.status_code == 200:
                data_trait = response_trait.json()
                trait_name = data_trait['_embedded']['efoTraits'][0].get('trait')
            else:
                trait_name = "Unknown Trait"

            # Insert data into the database
            # check if phenotype already exists
            cursor = con.execute('''
                SELECT 1 FROM PHENO_TABLE WHERE Phenotype = ? AND Expression = ?
            ''', (trait_name, expression))

            if cursor.fetchone() is None:
                con.execute('''
                    INSERT INTO PHENO_TABLE (Phenotype, Expression) VALUES (?, ?)
                ''', (trait_name, expression))

            con.commit()
        con.close()

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")



parseSNP("rs7329174")