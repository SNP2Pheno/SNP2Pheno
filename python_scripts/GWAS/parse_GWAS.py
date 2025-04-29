import requests

link = "https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/rs7329174/associations"
response = requests.get(link)
if response.status_code == 200:
    data = response.json()

    firstAssociation = data['_embedded']['associations'][0]
    pValueMantisse = firstAssociation.get('pvalueMantissa')
    pValueExponent = firstAssociation.get('pvalueExponent')
    orValue = firstAssociation.get('orPerCopyNum')
    CIRange = firstAssociation.get('range')
    expression = firstAssociation.get('pvalueDescription')
    trait = firstAssociation.get('_links').get('efoTraits')

    response_trait = requests.get(trait.get('href'))
    if response_trait.status_code == 200:
        data_trait = response_trait.json()
        trait_name = data_trait['_embedded']['efoTraits'][0].get('trait')
    else:
        trait_name = "Unknown Trait"

    print(f"pValueMantisse: {pValueMantisse}")
    print(f"pValueExponent: {pValueExponent}")
    print(f"orValue: {orValue}")
    print(f"CIRange: {CIRange}")
    print(f"expression: {expression}")
    print(f"trait: {trait_name}")

else:
    print(f"Failed to fetch data. Status code: {response.status_code}")