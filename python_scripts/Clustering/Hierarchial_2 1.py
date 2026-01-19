# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 17:41:03 2025

@author: julia
"""

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering
from collections import Counter
import plotly.figure_factory as ff

import seaborn as sns
import matplotlib.pyplot as plt


rs_ids = {"rs12913832" : "A", "rs12913832" : "G", "rs1667394" : "?", "rs11855019" : "?", "rs12203592" : "?", "rs12896399" : "G", "rs3002288" : "A", "rs7173419" : "T", "rs1408799" : "C"}

rs_ids = {"rs12913832" : "A", "rs12913832" : "G", "rs1667394" : "?", "rs11855019" : "?", "rs12913832" : "A", "rs12896399" : "G", "rs1847134" : "A", "rs12203592" : "?", "rs12896399" : "G", "rs3002288" : "A", "rs7173419" : "T", "rs1408799" : "C"}

rs_ids = {"rs12913832" : "A", "rs12896399" : "G", "rs1408799" : "C"}

df = pd.read_csv("clustering_data/genotype_eyecolor.csv", sep=";", index_col="Unnamed: 0")


print(df)

d = {}

for rs in rs_ids:
    
    if rs in list(df.index):
        d[rs] = []
        if rs_ids[rs] != "?":
            for user, allele in zip(df.columns, df.loc[rs].values):
                if type(allele) != str or len(allele) < 2:
                    d[rs].append(-1)
                elif allele.find(rs_ids[rs]) >= 0:
                    d[rs].append(1)
                else:
                    d[rs].append(0)
        else:
            uniques = Counter(["".join(sorted(list(x))) for x in df.loc[rs].values if type(x) == str and len(x) == 2])
            uniques_3 = sorted(uniques, key=uniques.get, reverse=True)[:3]
            
            print(uniques_3)
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

df2.loc["jve"] = [0, 1, 1]
print(df2)

#%%

df3 = pd.read_csv('clustering_data/phenotype_eyecolor.csv', sep=';')

l = []
for u in df2.index:
    if u == "jve":
        l.append("Blue")
        continue
    userID = u[4:u.find("_")]
    if int(userID) in list(df3["User IDs"]):
        # print(userID)
        l.append(list(df3[df3['User IDs'] == int(userID)]["Eye color"])[0])
    else:
        l.append(np.nan)
    

df2["EyeColor"] = l

#%%
X = df2.dropna(subset="EyeColor")

# change colors here (also change in lut)
X = X[X["EyeColor"].isin(["Blue", "Brown"])]
# X = X[X["EyeColor"].isin(["Blue", "Brown", "Green"])]
X = X.replace(-1, np.nan)
X = X.dropna() # thresh=2)
X = X.fillna(-1)
   

print(X)


fig = plt.figure(figsize=(25, 25), dpi=400)


lut = dict(zip([str(x) for x in np.unique(X["EyeColor"])], ["tab:blue", "brown"])) #  ["tab:blue", "brown"])) # ["tab:blue", "grey", "brown", "tab:green"])) # ["tab:blue", "brown"])) # ["tab:blue", "grey", "brown", "tab:green"]))
row_colors = X["EyeColor"].map(lut)
g = sns.clustermap(X[cols], row_colors=list(row_colors), cmap="Greens") # col_cluster=False) # , standard_scale=1)#, method="average")
               #method='complete', metric='hamming', row_cluster=False) #, z_score=0, cmap="vlag", center=0)


plt.suptitle("Clustermap: Eye Color\n(# Blue: 161, # Brown: 269)",  y=1.05, fontsize=25) #", # Green: 74)",
# plt.yticks([])
# plt.axis('off')

g.ax_heatmap.set_yticklabels([])
g.ax_heatmap.set_yticks([])
g.ax_heatmap.set_ylabel("")

print(Counter(X["EyeColor"]))

plt.show()

#%%

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt

import pickle


def random_forest_classification(df, features, target, test_size=0.3, n_estimators=100, random_state=42):
    
    # Split data
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Train RandomForest
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    print(y_pred)
    
    # save model as pickle
    with open('RF_eyecolor.pkl', 'wb') as file:
        pickle.dump(model, file)

    
    # Metrics
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Feature importance plot
    importances = model.feature_importances_
    plt.figure(figsize=(8, 6))
    plt.barh(features, importances, color='teal')
    plt.title('Feature Importance (RandomForest)')
    plt.xlabel('Importance')
    plt.ylabel('Features')
    plt.show()
    
    return pd.DataFrame([list(y_test), list(y_pred)]).T
# Example usage:
# df = pd.read_csv('your_data.csv')
# random_forest_classification(df, features=['feature1', 'feature2', 'feature3'], target='target_column')


df_result = random_forest_classification(X, features=cols, target='EyeColor')

#%%
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X[cols])


df_pca = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])
df_pca['EyeColor'] = list(X["EyeColor"])

# Plot PCA scatter with points colored by eye color
plt.figure(figsize=(10, 7), dpi=400)
# =============================================================================
# fig = sns.scatterplot(
#     data=df_pca,
#     x='PC1',
#     y='PC2',
#     hue="EyeColor", alpha=1
# )
# =============================================================================

sns.kdeplot(data=df_pca,
                x='PC1',
                y='PC2',
                hue="EyeColor", palette=sns.color_palette(["tab:blue", "green", "brown"]), fill=True, alpha=0.5)#  "tab:green", 

plt.plot(float(df_pca.iloc[-1]["PC1"]), float(df_pca.iloc[-1]["PC2"]), c="k", marker="*")

plt.title("PCA: Eye Color\n(# Blue: 161, # Brown: 269)") # ", # Green: 74)")

plt.show()
# fig.show()


X_tsne = TSNE(n_components=2, random_state=4242, perplexity=10).fit_transform(X[cols])

# Create DataFrame for plotting
df_tsne = pd.DataFrame(X_tsne, columns=['TSNE1', 'TSNE2'])
df_tsne['EyeColor'] = list(X["EyeColor"])


# Plot t-SNE scatter with points colored by eye color
plt.figure(figsize=(10, 7), dpi=400)
# sns.scatterplot(data=df_tsne, x='TSNE1', y='TSNE2', hue='EyeColor', palette='Set2', s=80)
sns.kdeplot(data=df_tsne,
                x='TSNE1',
                y='TSNE2',
                hue="EyeColor", palette=sns.color_palette(["tab:blue", "green", "brown"]), fill=True, alpha=0.5) #, "tab:green"

plt.plot(float(df_tsne.iloc[-1]["TSNE1"]), float(df_tsne.iloc[-1]["TSNE2"]), c="k", marker="*")

plt.title("t-SNE: Eye Color\n(# Blue: 161, # Brown: 269)") # ", # Green: 74)")

# plt.legend(title='Eye Color')
# plt.tight_layout()
plt.show()
