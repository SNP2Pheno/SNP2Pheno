import sqlite3
from collections import defaultdict

import requests

from python_scripts.GWAS.Association import Association, TYPE


def is_better(ass_new, ass_old):
    if ass_old.pValueExponent > ass_new.pValueExponent:
        return True
    if ass_old.pValueExponent == ass_new.pValueExponent and ass_old.pValueMantissa > ass_new.pValueMantissa:
        return True
    return False


def parseSNP(snpID):
    all_associations = []
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
            if association.get('betaNum') is not None:
                ass_obj.betaNum = association.get('betaNum')
            if association.get('betaUnit') is not None:
                ass_obj.betaUnit = association.get('betaUnit')
            if association.get('betaDirection') is not None:
                ass_obj.betaDirection = association.get('betaDirection')
            trait = association.get('_links').get('efoTraits')
            numOfInd = association.get('_links').get('study')

            response_trait = requests.get(trait.get('href'))
            if response_trait.status_code == 200:
                data_trait = response_trait.json()
                ass_obj.trait_name = data_trait['_embedded']['efoTraits'][0].get('trait')

                response_ols = requests.get('https://www.ebi.ac.uk/ols4/api/ontologies/efo/terms?short_form=' + data_trait['_embedded']['efoTraits'][0].get('shortForm'))
                if response_ols.status_code == 200:
                    data_ols = response_ols.json()
                    description = data_ols['_embedded']['terms'][0]['description'][0]
                    if str(description).__contains__('disease') or str(description).__contains__('disorder'):
                        ass_obj.type = TYPE.DISEASE
                    else:
                        ass_obj.type = TYPE.APPEARANCE

            response_NumOfInd = requests.get(numOfInd.get('href'))
            if response_NumOfInd.status_code == 200:
                data_NumOfInd = response_NumOfInd.json()
                ancestries = data_NumOfInd['ancestries']
                if ancestries is not None:
                    for a in ancestries:
                        if a['type'] == 'initial':
                            ass_obj.NumOfIndividualsInStudy = a['numberOfIndividuals']

            all_associations.append(ass_obj)

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

    output_data = []

    grouped = defaultdict(list)
    for ass in all_associations:
        key = (ass.trait_name, ass.expression)
        grouped[key].append(ass)

    for key, group in grouped.items():
        sorted_group = sorted(group, key=lambda x: x.NumOfIndividualsInStudy)

        top_associations = sorted_group[:3]

        best_ass = min(top_associations, key=lambda x: (x.pValueExponent, x.pValueMantissa))
        output_data.append(best_ass)

    return output_data



output_data = parseSNP("rs7329174")
for i, output_datum in enumerate(output_data):
    print(output_datum.__str__())
#parseSNP("rs75161997")