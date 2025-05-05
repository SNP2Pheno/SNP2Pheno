import requests

def parseSNP(snpID):

    link = "https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/" + snpID + "/associations"
    response = requests.get(link)
    if response.status_code == 200:
        data = response.json()
        for association in data['_embedded']['associations']:

            if association.get('pvalueMantissa') is not None and association.get('pvalueExponent') is not None:
                pValueMantisse = association.get('pvalueMantissa')
                pValueExponent = association.get('pvalueExponent')
            if association.get('orPerCopyNum') is not None:
                orValue = association.get('orPerCopyNum')
            if association.get('range') is not None and association.get('range') != '[NR]':
                CIMin = association.get('range')[1:].split('-')[0]
                CIMax = association.get('range')[:-1].split('-')[1]
            expression = association.get('pvalueDescription')
            trait = association.get('_links').get('efoTraits')

            response_trait = requests.get(trait.get('href'))
            if response_trait.status_code == 200:
                data_trait = response_trait.json()
                trait_name = data_trait['_embedded']['efoTraits'][0].get('trait')
            else:
                trait_name = "Unknown Trait"

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")



parseSNP("rs7329174")