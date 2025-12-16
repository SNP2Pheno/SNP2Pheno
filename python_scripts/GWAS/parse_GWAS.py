from collections import defaultdict
import requests
from Association import Association, TYPE

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
            association_obj = Association()

            if association.get('loci')[0].get('strongestRiskAlleles') is not None:
                wholeRiskAlleleName = association.get('loci')[0].get('strongestRiskAlleles')[0].get('riskAlleleName')
                association_obj.riskAllele = wholeRiskAlleleName.split('-')[1]
            if association.get('pvalueMantissa') is not None and association.get('pvalueExponent') is not None:
                association_obj.pValueMantissa = association.get('pvalueMantissa')
                association_obj.pValueExponent = association.get('pvalueExponent')
            if association.get('orPerCopyNum') is not None:
                association_obj.orValue = association.get('orPerCopyNum')
            if association.get('range') is not None and not str(association.get('range')).__contains__('NR'):
                association_normalized = association.get('range').replace("–", "-").replace(", ", "-")
                if len(association_normalized.split('-')) == 2:
                    association_obj.CIMin = association_normalized.split('-')[0]
                    association_obj.CIMax = association_normalized.split('-')[1]
            if association.get('pvalueDescription') is not None:
                association_obj.expression = association.get('pvalueDescription')
            if association.get('betaNum') is not None:
                association_obj.betaNum = association.get('betaNum')
            if association.get('betaUnit') is not None:
                association_obj.betaUnit = association.get('betaUnit')
            if association.get('betaDirection') is not None:
                association_obj.betaDirection = association.get('betaDirection')
            trait = association.get('_links').get('efoTraits')
            numOfInd = association.get('_links').get('study')

            responseTrait = requests.get(trait.get('href'))
            if responseTrait.status_code == 200:
                data_trait = responseTrait.json()
                association_obj.traitName = data_trait['_embedded']['efoTraits'][0].get('trait')
                if data_trait['_embedded']['efoTraits'][0].get('shortForm') is not None:
                    response_ols = requests.get('https://www.ebi.ac.uk/ols4/api/ontologies/efo/terms?short_form=' + data_trait['_embedded']['efoTraits'][0].get('shortForm'))
                    if response_ols.status_code == 200:
                        data_ols = response_ols.json()
                        if len(data_ols['_embedded']['terms'][0].get('description')) != 0:
                            description = data_ols['_embedded']['terms'][0]['description'][0]
                            if str(description).__contains__('disease') or str(description).__contains__('disorder'):
                                association_obj.type = TYPE.DISEASE
                            else:
                                association_obj.type = TYPE.APPEARANCE

            responseNumOfIndividuals = requests.get(numOfInd.get('href'))
            if responseNumOfIndividuals.status_code == 200:
                dataNumOfInd = responseNumOfIndividuals.json()
                ancestries = dataNumOfInd['ancestries']
                if ancestries is not None:
                    for a in ancestries:
                        if a['type'] == 'initial':
                            association_obj.NumOfIndividualsInStudy = a['numberOfIndividuals']
                            if association_obj.NumOfIndividualsInStudy is None:
                                association_obj.NumOfIndividualsInStudy = 0

            allAssociations.append(association_obj)
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
