import numpy as np
from sklearn.cluster import AffinityPropagation as cluster_clf
from scipy.spatial.distance import cdist
from scipy.cluster.hierarchy import dendrogram, linkage

max_t = 250

target = "Skull"
#target = "Smiling Face With Open Mouth and Smiling Eyes"
target = "EMOJI_"+target.lower().replace(" ","_")
                 
# Load the config files
from configobj import ConfigObj
config = ConfigObj("config.ini")
wcon = config["word2vec"]   

from gensim.models.word2vec import Word2Vec
f_features = wcon["f_features"].format(**wcon)
clf = Word2Vec.load(f_features)


def tweet_iterator(limit=None):
    counter = 0
    with open("all_unique_tweets.txt") as FIN:
        for line in FIN:
            if target in line:
                yield line.split()
                counter += 1
                if counter == limit: break


V = []
for tokens in tweet_iterator(max_t):
    v = np.array([clf[t] for t in tokens if t in clf])
    V.append( v.mean(axis=0) )

V = np.array(V)
DV = cdist(V,V,metric='cosine')
print DV

import seaborn as sns
plt = sns.plt

# Values are sometimes "slightly" less than zero due to rounding
DV[DV<0] = 0

cluster_args = {"damping":0.9}
cluster = cluster_clf(**cluster_args)

y_labels = cluster.fit_predict(DV)
idx = np.argsort(y_labels)

affinity_DV = DV[idx,:][:,idx]
y_labels = y_labels[idx]
    
#sns.heatmap(DV,xticklabels=False,yticklabels=False,linewidths=0)
#plt.figure()
sns.heatmap(affinity_DV,xticklabels=False,yticklabels=False,linewidths=0)
plt.show()



