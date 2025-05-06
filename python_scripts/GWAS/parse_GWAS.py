import sqlite3

import requests

from python_scripts.GWAS.Association import Association

def is_better(ass_new, ass_old):
    """Return True if the new association is more significant and has all necessary data."""
    if ass_old.pValueExponent > ass_new.pValueExponent:
        return True
    if ass_old.pValueExponent == ass_new.pValueExponent and ass_old.pValueMantissa > ass_new.pValueMantissa:
        return True
    return False


def parseSNP(snpID):
    output_data = []
    link = "https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/" + snpID + "/associations"
    response = requests.get(link)
    if response.status_code == 200:
        data = response.json()
        for association in data['_embedded']['associations']:
            ass_obj = Association()

            if association.get('pvalueMantissa') is not None and association.get('pvalueExponent') is not None:
                ass_obj.pValueMantissa = association.get('pvalueMantissa')
                ass_obj.pValueExponent = association.get('pvalueExponent')
            if association.get('orPerCopyNum') is not None:
                ass_obj.orValue = association.get('orPerCopyNum')
            if association.get('range') is not None and association.get('range') != '[NR]':
                ass_obj.CIMin = association.get('range')[1:].split('-')[0]
                ass_obj.CIMax = association.get('range')[:-1].split('-')[1]
            if association.get('pvalueDescription') is not None:
                ass_obj.expression = association.get('pvalueDescription')
            trait = association.get('_links').get('efoTraits')

            response_trait = requests.get(trait.get('href'))
            if response_trait.status_code == 200:
                data_trait = response_trait.json()
                ass_obj.trait_name = data_trait['_embedded']['efoTraits'][0].get('trait')

            # check if there is a same pheno-expression pair => then look at p-Value
            for d in output_data:
                if d.trait_name == ass_obj.trait_name and d.expression == ass_obj.expression:
                    if is_better(d, ass_obj):
                        output_data.remove(d)
                        output_data.append(ass_obj)
                    break
            else:
                output_data.append(ass_obj)


    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

    return output_data



output_data = parseSNP("rs7329174")
parseSNP("rs75161997")