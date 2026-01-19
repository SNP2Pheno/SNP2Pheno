# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering
from collections import Counter
import plotly.figure_factory as ff

import seaborn as sns
import matplotlib.pyplot as plt

# These rs_ids are associated with eye color => selection of SNPs for clustering
# for every SNP there is a relevant Allele (?, if unknown)

rs_ids = {"rs507666" : "A", "rs8176746" : "T", "rs687289" : "G", "rs8176704": "A", "rs657152": "A"}    # currently used ones for clustering => see dendrogram

# load genotype data
df = pd.read_csv("clustering_data/genotype_bloodtype.csv", sep=";", index_col="Unnamed: 0")


print(df)

# represent Alleles numerically
d = {}

for rs in rs_ids:
    # for every rsID of interest, create a list of values for every user
    if rs in list(df.index):
        d[rs] = []
        if rs_ids[rs] != "?":   # if a specific allele is known for this rsID
            for user, allele in zip(df.columns, df.loc[rs].values):
                # if the allele is not a string or length < 2, append -1 (missing data)
                if type(allele) != str or len(allele) < 2:
                    d[rs].append(-1)
                elif allele.find(rs_ids[rs]) >= 0:      # if the known allele is found in the genotype, append 1
                    d[rs].append(1)
                else:
                    d[rs].append(0)     # known allele not found in genotype
        # every user has now a value for this rsID [1, 0, 1]
        else:
            # if no specific allele is known for this rsID (==?), find the three most common alleles and encode them as 0, 1, 2
            # count all unique genotypes
            uniques = Counter(["".join(sorted(list(x))) for x in df.loc[rs].values if type(x) == str and len(x) == 2])
            uniques_3 = sorted(uniques, key=uniques.get, reverse=True)[:3] # get the three most common genotypes
            
            print(uniques_3)
            # assign values based on the index in uniques_3
            for user, allele in zip(df.columns, df.loc[rs].values):
                if type(allele) != str or len(allele) < 2 or allele not in uniques_3:
                    d[rs] = -1
                else:
                    d[rs] = uniques_3.index(allele)

            # break
            
# print(d)
df2 = pd.DataFrame.from_dict(d)
df2.index = list(df.columns)

cols = df2.columns

#%% add person data: jve
    # rs12913832: GG -> 1 if A, 0 if other
    # rs12896399: GG -> 1 if G, 0 if other
    # rs1408799: CC  -> 1 if C, 0 if other

#df2.loc["jve"] = [0, 1, 1]
#print(df2)

#%%

# add blood type data
df3 = pd.read_csv('clustering_data/phenotype_bloodtype.csv', sep='\t')

df3["Blood type"] = df3["Blood type"].astype(str).str.strip().str.upper()

# Remove Rhesus symbols (+ / -) and any whitespace
df3["Blood type"] = df3["Blood type"].str.replace("+", "", regex=False)
df3["Blood type"] = df3["Blood type"].str.replace("-", "", regex=False)
df3["Blood type"] = df3["Blood type"].str.replace(" ", "", regex=False)

# Filter only valid main groups (A, B, AB, 0)
valid_groups = ["A", "B", "AB", "0"]
df3 = df3[df3["Blood type"].isin(valid_groups)]

# Reset index (optional)
df3 = df3.reset_index(drop=True)

print(df3["Blood type"].value_counts())
print(df3.head())

l = []
# map blood type to each user => look for userID and get the blood type
for u in df2.index:
    userID = u[4:u.find("_")]
    if int(userID) in list(df3["User IDs"]):
        # print(userID)
        l.append(list(df3[df3['User IDs'] == int(userID)]["Blood type"])[0])
    else:
        l.append(np.nan)
    

df2["Blood type"] = l

#%%
X = df2.dropna(subset="Blood type")

# select only specific blood types for better visualization
# change colors here (also change in lut)
X = X[X["Blood type"].isin(["A", "B", "AB", "O"])]
X = X.replace(-1, np.nan)
X = X.dropna() # thresh=2)
X = X.fillna(-1)
   

print(X)


fig = plt.figure(figsize=(25, 25), dpi=400)
color_palette = {
    "A": "tab:red",
    "B": "tab:blue",
    "AB": "tab:purple",
    "0": "tab:green"
}

# Make sure the blood type labels are clean and uppercase
X["Blood type"] = X["Blood type"].astype(str).str.strip().str.upper()

row_colors = X["Blood type"].map(color_palette)

# Use a valid continuous color map for the heatmap (not "AB")
g = sns.clustermap(
    X[cols],
    row_colors=row_colors,
    cmap="Greens",       # valid colormap
    method="average",    # optional: can adjust to "complete" etc.
    figsize=(25, 25),
)

plt.suptitle("Clustermap: Blood Type", y=1.05, fontsize=25)

g.ax_heatmap.set_yticklabels([])
g.ax_heatmap.set_yticks([])
g.ax_heatmap.set_ylabel("")

plt.show()

#%%
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# reduce 3D to 2D with PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X[cols])

# every person is now a point in the plot

df_pca = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])
df_pca['Blood type'] = list(X["Blood type"])

# Plot PCA scatter with points colored by blood type
plt.figure(figsize=(10, 7), dpi=400)
# =============================================================================
# fig = sns.scatterplot(
#     data=df_pca,
#     x='PC1',
#     y='PC2',
#     hue="Blood type", alpha=1
# )
# =============================================================================

palette = [color_palette[k] for k in ["A", "B", "AB", "0"]]

sns.kdeplot(
    data=df_pca,
    x='PC1', y='PC2',
    hue="Blood type",
    palette=palette,
    fill=True, alpha=0.5
)


plt.title("PCA: Blood Type\n")

plt.show()
# fig.show()


X_tsne = TSNE(n_components=2, random_state=4242, perplexity=10).fit_transform(X[cols])

# Create DataFrame for plotting
df_tsne = pd.DataFrame(X_tsne, columns=['TSNE1', 'TSNE2'])
df_tsne['Blood type'] = list(X["Blood type"])


# Plot t-SNE scatter with points colored by blood type => better separation than PCA
plt.figure(figsize=(10, 7), dpi=400)
# sns.scatterplot(data=df_tsne, x='TSNE1', y='TSNE2', hue='Blood type', palette='Set2', s=80)
sns.kdeplot(
    data=df_tsne,
    x='TSNE1', y='TSNE2',
    hue="Blood type",
    palette=palette,
    fill=True, alpha=0.5
)

plt.title("t-SNE: Blood Type\n")

# plt.legend(title='Blood type')
# plt.tight_layout()
plt.show()
