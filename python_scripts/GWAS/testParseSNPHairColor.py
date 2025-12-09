import re

from python_scripts.GWAS.parse_GWAS import parseSNP

# explanation for these values:
# p-value < 5e-8 (widely accepted threshold for genome-wide significance)
# OR > 1.2 or OR < 0.8 (20% increase or decrease in odds per allele)
# beta threshold of 0.2 (in GWAS as "middle effect size")

def getSignificant(current_associations, threshold=5e-8, or_min=1.2, or_max=0.8, beta_threshold=0.2):
    res = []
    current_traits = ["hair color", "hair colour"]

    for a in current_associations:
        if a.traitName and a.traitName in current_traits:
            if a.pValueExponent is not None and a.pValueMantissa is not None:
                p = a.pValueMantissa * (10 ** a.pValueExponent)
                if p < threshold:
                    if a.orValue is not None or a.betaNum is not None:
                        if a.orValue > or_min or a.orValue < or_max:
                         if abs(a.betaNum) >= beta_threshold:
                            res.append(a)
    return res


current_trait = "hair color"
output_file = "parsed_results_" + current_trait +".csv"
header = [
        "rsID", "pValueExponent", "pValueMantissa", "orValue", "betaNum", "betaUnit",
        "betaDirection", "CIMax", "CIMin", "expression", "traitName",
        "type", "NumOfIndividualsInStudy", "strongestAllele"
    ]

with open(output_file, "w") as f:
   f.write(";".join(header) + "\n")

for rs in open('snp_ids_listHairColor.txt').read().splitlines():

    print(f"Processing {rs}...")

    if rs.startswith('chr'): continue


    current_associations = parseSNP(rs)
    significant_associations = getSignificant(current_associations)
    if significant_associations:
        print(f"Significant association found for {rs}, count: {len(significant_associations)}")
        with open(output_file, "a") as f:
            for a in significant_associations:
                f.write(rs + ";" + ";".join(map(str, vars(a).values())) + "\n")