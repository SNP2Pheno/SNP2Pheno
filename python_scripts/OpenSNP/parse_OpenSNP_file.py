
def parse_OpenSNP_file(file_path):
    snp_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue

            parts = line.strip().split('\t')
            snp_id = parts[0]
            if not snp_id.startswith('rs'):
                continue
            snp_genotype = parts[-1]
            snp_dict[snp_id] = snp_genotype
    return snp_dict

def write_to_file(snp_dict, output_file):
    with open(output_file, 'w') as file:
        for snp_id, snp_genotype in snp_dict.items():
            file.write(f"{snp_id}\t{snp_genotype}\n")