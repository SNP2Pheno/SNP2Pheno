# Future Tasks
## 1000 Genome files
- research 1000 genome + connection to current dataset
- arrange meeting with Lirk for further information
- filter out rsIDs for a specific phenotype
- look for rsIDs (source openSNP) and compare results (alleles)
- DoD: similar results like openSNP (chart, table, analysis)

## Check Indexed VCF-parsing
- test indexed VCF parsing
- integrate into VCF parser
- DoD: Answer question if it's useful to integrate this into SNP2Pheno

## AI revision
- check if the AI gives similar rs-IDs to those we have in our database (Note: We tried to integrate [FutureHouse](https://www.futurehouse.org/), unfinished)
- develop prompts to...
- ... get rs-IDs for specific phenotypic expressions
- ... distinguish between appearance and disease
- DoD: list of prompts

## Automize DB filling
- use significant SNPs for specific traits (e.g., eye color, hair color, etc.) from GWAS and add them to DB
- DoD: DB is filled with rsIDs, alleles, and other important features (p-values, etc.)

## Lirk'sche Liste
- allow user to add list of rsIDs to database
- DoD: button/option to add own list of rsIDs with potential traits
- DoD: add information from GWAS Catalog
- DoD: should be presented as table in separate UI tab

## Simple TXT parser
- With structure rsID, allele
