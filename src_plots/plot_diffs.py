import itertools, os
import emoji
from sklearn.cluster import SpectralClustering as cluster_clf
# sudo apt-get install ttf-ancient-fonts

CLUSTER_N = 4
cutoff = 40

# Load the config files
from configobj import ConfigObj
config = ConfigObj("config.ini")
wcon = config["word2vec"]

from gensim.models.word2vec import Word2Vec
f_features = wcon["f_features"].format(**wcon)

clf = Word2Vec.load(f_features)
EM = [w.lstrip("EMOJI_") for w in clf.index2word if "EMOJI_" in w][:cutoff]

import numpy as np
import pandas as pd

def label_maker(s):
    return emoji.emojize(":"+s+":")

names = map(label_maker,EM)

df = pd.DataFrame(0.0, columns=names, index=names)
for w1, w2 in itertools.product(EM,repeat=2):
    if w1==w2: continue

    name1 = label_maker(w1)
    name2 = label_maker(w2)
    
    df[name1][name2] = clf.similarity("EMOJI_"+w1,"EMOJI_"+w2)

A = df.values

cluster_args = {"n_clusters":CLUSTER_N}
cluster = cluster_clf(**cluster_args)

y_labels = cluster.fit_predict(A)
idx = np.argsort(y_labels)

y_labels = y_labels[idx]    
A = A[idx,:][:,idx]

labels = np.array(names)[idx]
df2 = pd.DataFrame(A, columns=labels, index=labels)

import seaborn as sns

import matplotlib
import matplotlib.pyplot as plt


plt.figure(figsize=(10,10))
fs = 20
rc={
    'font.family':"Symbola",
    'xtick.labelsize': fs, 'ytick.labelsize': fs
}

sns.set(rc=rc)
sns.heatmap(df2,vmax=1.0,cbar=False)
plt.tight_layout()

os.system('mkdir -p figures')
f_png = 'figures/similarity_map.png'
plt.savefig(f_png, bbox_inches=None)

plt.show()


'''
# Attempt at a TSNE plot
sns.plt.figure()
from sklearn.manifold import TSNE

V = np.array([clf["EMOJI_"+w] for w in EM])
   

embedding_model = TSNE(n_components=2, metric='cosine')
embedding_pts = embedding_model.fit_transform(V)

#embedding_model = TSNE(n_components=2, metric="precomputed")
#embedding_pts = embedding_model.fit_transform(1/(2*(A+1)))

colors = ['r','g','b','k','m']
for i,c in zip(np.unique(y_labels),colors):
    pts = embedding_pts[y_labels==i]
    sns.plt.scatter(pts.T[0],pts.T[1],color=c)


'''


