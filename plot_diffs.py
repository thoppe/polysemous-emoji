import itertools
from sklearn.manifold import TSNE

CLUSTER_N = 4
cutoff = 120

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
df = pd.DataFrame(0.0, columns=EM, index=EM)
for w1, w2 in itertools.product(EM,repeat=2):
    if w1==w2: continue    
    df[w1][w2] = clf.similarity("EMOJI_"+w1,"EMOJI_"+w2)

V = np.array([clf["EMOJI_"+w] for w in EM])
    
A = df.values
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.cluster import SpectralClustering as cluster_clf
#from sklearn.cluster import KMeans as cluster_clf

'''
for n in range(2,20):

    cluster_args = {"n_clusters":n}

    cluster = cluster_clf(**cluster_args)
    y_labels = cluster.fit_predict(A)
    idx = np.argsort(y_labels)

    silhouette_avg = silhouette_score(A, y_labels)
    print n, silhouette_avg
'''

cluster_args = {"n_clusters":CLUSTER_N}
cluster = cluster_clf(**cluster_args)

y_labels = cluster.fit_predict(A)
idx = np.argsort(y_labels)

y_labels = y_labels[idx]    
A = A[idx,:][:,idx]
labels = np.array(EM)[idx]

df2 = pd.DataFrame(A, columns=labels, index=labels)


import seaborn as sns
#sns.heatmap(df,vmax=1.0,vmin=-0.5)
sns.heatmap(df2,vmax=1.0,vmin=-0.5)

sns.plt.figure()

embedding_model = TSNE(n_components=2, metric='cosine')
embedding_pts = embedding_model.fit_transform(V)

#embedding_model = TSNE(n_components=2, metric="precomputed")
#embedding_pts = embedding_model.fit_transform(1/(2*(A+1)))

colors = ['r','g','b','k','m']
for i,c in zip(np.unique(y_labels),colors):
    pts = embedding_pts[y_labels==i]
    sns.plt.scatter(pts.T[0],pts.T[1],color=c)

sns.plt.show()



