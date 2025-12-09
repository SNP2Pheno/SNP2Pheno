import pandas as pd

# Read the file (works for both .csv and .xlsx)
df = pd.read_csv("parsed_results_blood_typeGene.csv", sep=None, engine="python")

# Drop duplicate rsIDs, keeping the first occurrence
df_unique = df.drop_duplicates(subset=["rsID"], keep="first")

# Save the result
df_unique.to_csv("unique_BloodTypeGene_rsIDs.csv", index=False)
# or for CSV:
# df_unique.to_csv("unique_rsIDs.csv", index=False)

print(f"Reduced from {len(df)} rows to {len(df_unique)} unique rsIDs.")
