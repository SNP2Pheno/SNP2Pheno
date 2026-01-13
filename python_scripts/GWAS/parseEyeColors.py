import pandas as pd

#eye color EFO_0003949
file_path = "gwas-association-downloaded_2025-12-16-EFO_0003949.tsv"
#hair color EFO_0003924
#file_path = "gwas-association-downloaded_2025-10-07-EFO_0003924.tsv"
#handedness
#file_path = "gwas-association-downloaded_2025-10-13-EFO_0009902.tsv"
#biological sex
#file_path = "gwas-association-downloaded_2025-10-13-PATO_0000047.tsv"
#blood types
#file_path = "gwas-association-downloaded_2025-10-13-EFO_0600060.tsv"
#file_path = "gwas-association-downloaded_2025-10-13-EFO_0600061.tsv"
#file_path = "gwas-association-downloaded_2025-10-13-EFO_0600062.tsv"
#file_path = "gwas-association-downloaded_2025-10-13-EFO_0600063.tsv"
#file_path = "../../../../gwas-association-downloaded_2025-10-13-ensemblMappedGenes_ABO.tsv"

df = pd.read_csv(file_path, sep="\t")

snp_ids = df["SNPS"].drop_duplicates()

print(snp_ids.tolist())

output_file = "snp_ids_listEyeColor.txt"

with open(output_file, "w") as f:
    for snp_id in snp_ids:
        f.write(f"{snp_id}\n")