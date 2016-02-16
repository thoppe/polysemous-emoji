import itertools
from src.emoji_handler import load_emoji
from sklearn.manifold import TSNE

# Load the config files
from configobj import ConfigObj
config = ConfigObj("config.ini")
wcon = config["word2vec"]

from gensim.models.word2vec import Word2Vec
f_features = wcon["f_features"].format(**wcon)

clf = Word2Vec.load(f_features)
EM = load_emoji(config["scrape"]["f_emoji"])

import numpy as np
import pandas as pd
df = pd.DataFrame(0.0, columns=EM.keys(), index=EM.keys())
for w1, w2 in itertools.product(EM,repeat=2):

    if w1==w2: continue
    
    word1 = "EMOJI_{}".format(w1)
    word2 = "EMOJI_{}".format(w2)
    df[w1][w2] = clf.similarity(word1,word2)
    
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

cluster_args = {"n_clusters":3}
cluster = cluster_clf(**cluster_args)

y_labels = cluster.fit_predict(A)
idx = np.argsort(y_labels)

y_labels = y_labels[idx]    
A = A[idx,:][:,idx]
labels = np.array(EM.keys())[idx]

df2 = pd.DataFrame(A, columns=labels, index=labels)


import seaborn as sns
#sns.heatmap(df,vmax=1.0,vmin=-0.5)
sns.heatmap(df2,vmax=1.0,vmin=-0.5)

sns.plt.figure()

embedding_model = TSNE(n_components=3, random_state=0)
embedding_pts = embedding_model.fit_transform(A)

colors = ['r','g','b','k','m']
for i,c in zip(np.unique(y_labels),colors):
    pts = embedding_pts[y_labels==i]
    sns.plt.scatter(pts.T[0],pts.T[1],pts.T[2],color=c)

sns.plt.show()



