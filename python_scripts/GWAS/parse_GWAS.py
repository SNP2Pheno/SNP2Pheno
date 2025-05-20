from collections import defaultdict

import requests

from python_scripts.GWAS.Association import Association, TYPE


def is_better(associationNew, associationOld):
    if associationOld.pValueExponent > associationNew.pValueExponent:
        return True
    if associationOld.pValueExponent == associationNew.pValueExponent and associationOld.pValueMantissa > associationNew.pValueMantissa:
        return True
    return False


def parseSNP(snpID):
    allAssociations = []
    link = "https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/" + snpID + "/associations"
    response = requests.get(link)
    if response.status_code == 200:
        data = response.json()
        for association in data['_embedded']['associations']:
            assicationObj = Association()

            if association.get('pvalueMantissa') is not None and association.get('pvalueExponent') is not None:
                assicationObj.pValueMantissa = association.get('pvalueMantissa')
                assicationObj.pValueExponent = association.get('pvalueExponent')
            if association.get('orPerCopyNum') is not None:
                assicationObj.orValue = association.get('orPerCopyNum')
            if association.get('range') is not None and association.get('range') != '[NR]':
                association_normalized = association.get('range').replace("–", "-")
                assicationObj.CIMin = association_normalized.split('-')[0]
                assicationObj.CIMax = association_normalized.split('-')[1]
            if association.get('pvalueDescription') is not None:
                assicationObj.expression = association.get('pvalueDescription')
            if association.get('betaNum') is not None:
                assicationObj.betaNum = association.get('betaNum')
            if association.get('betaUnit') is not None:
                assicationObj.betaUnit = association.get('betaUnit')
            if association.get('betaDirection') is not None:
                assicationObj.betaDirection = association.get('betaDirection')
            trait = association.get('_links').get('efoTraits')
            numOfInd = association.get('_links').get('study')

            responseTrait = requests.get(trait.get('href'))
            if responseTrait.status_code == 200:
                data_trait = responseTrait.json()
                assicationObj.traitName = data_trait['_embedded']['efoTraits'][0].get('trait')

                response_ols = requests.get('https://www.ebi.ac.uk/ols4/api/ontologies/efo/terms?short_form=' + data_trait['_embedded']['efoTraits'][0].get('shortForm'))
                if response_ols.status_code == 200:
                    data_ols = response_ols.json()
                    description = data_ols['_embedded']['terms'][0]['description'][0]
                    if str(description).__contains__('disease') or str(description).__contains__('disorder'):
                        assicationObj.type = TYPE.DISEASE
                    else:
                        assicationObj.type = TYPE.APPEARANCE

            responseNumOfIndividuals = requests.get(numOfInd.get('href'))
            if responseNumOfIndividuals.status_code == 200:
                dataNumOfInd = responseNumOfIndividuals.json()
                ancestries = dataNumOfInd['ancestries']
                if ancestries is not None:
                    for a in ancestries:
                        if a['type'] == 'initial':
                            assicationObj.NumOfIndividualsInStudy = a['numberOfIndividuals']

            allAssociations.append(assicationObj)

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

    outputData = []

    grouped = defaultdict(list)
    for ass in allAssociations:
        key = (ass.traitName, ass.expression)
        grouped[key].append(ass)

    for key, group in grouped.items():
        sortedGroup = sorted(group, key=lambda x: x.NumOfIndividualsInStudy)

        topAssociations = sortedGroup[:3]

        bestAssociation = min(topAssociations, key=lambda x: (x.pValueExponent, x.pValueMantissa))
        outputData.append(bestAssociation)

    return outputData
