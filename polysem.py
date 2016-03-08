import numpy as np
from scipy.spatial.distance import cdist
import scipy.cluster.hierarchy as sch
import collections
import emoji

from sklearn.cluster import AffinityPropagation as cluster_clf
cluster_args = {"damping":0.999}

#from sklearn.cluster import KMeans as cluster_clf
#from sklearn.cluster import MeanShift as cluster_clf
#cluster_args = {}

max_t  = 20000
skip_t = 6

target = "skull"
target = "Smiling Face With Open Mouth and Smiling Eyes"
target = "key"
target = target.lower().replace(" ","_")
emoji_name = emoji.emojize(":"+target+":", use_aliases=True)
target = "EMOJI_"+target.lower().replace(" ","_")
print emoji_name

                 
# Load the config files
from configobj import ConfigObj
config = ConfigObj("config.ini")
wcon = config["word2vec"]   

from gensim.models.word2vec import Word2Vec
f_features = wcon["f_features"].format(**wcon)
clf = Word2Vec.load(f_features)

z = clf[target]

#dist = clf.syn0.dot(z)
#min_dist_idx = np.argsort(dist)[::-1]
#print [clf.index2word[j] for j in min_dist_idx[:10]]
#print clf.most_similar(target)
#exit()

def tweet_iterator(limit=None,skip=None):
    counter = 0
    with open("all_unique_tweets.txt") as FIN:
        for line in FIN:
            if target in line:

                counter += 1                
                if counter == limit: break

                if skip and counter%skip==0:
                    yield line.split()


V = []
for tokens in tweet_iterator(max_t,skip=skip_t):
    v = np.array([clf[t] for t in tokens if t in clf])
    V.append( v.mean(axis=0) )

V = np.array(V)

print "Size of V {}".format(V.shape)

cluster = cluster_clf(**cluster_args)
y_labels = cluster.fit_predict(V)

print "Number of clusters {}".format(y_labels.max())
print "Cluster sizes", collections.Counter(y_labels).most_common()

Z = []
WORDS = []
for i in range(y_labels.max()):
    idx = y_labels==i
    z = V[idx].mean(axis=0)
    z /= np.linalg.norm(z)
    Z.append(z)
    
    dispersion = V[idx].dot(z).mean()

    dist = clf.syn0.dot(z)
    min_dist_idx = np.argsort(dist)[::-1]
    words = [clf.index2word[j] for j in min_dist_idx[:10]]
    WORDS.append(words)


Z = np.array(Z)
WORDS = np.array(WORDS)

import seaborn as sns
plt = sns.plt
rc={'font.family':"Symbola",}
sns.set(rc=rc)

#fig = plt.figure()
#sns.heatmap(DZ,vmax=1)#,xticklabels=False,yticklabels=False,linewidths=0)

from scipy.cluster.hierarchy import dendrogram, linkage
#plt.figure()
#Y = linkage(Z,method='complete',metric='cosine')
#sch.dendrogram(Y)

fig = plt.figure(figsize=(8,8))
# Compute and plot first dendrogram.

# Compute and plot second dendrogram.
ax2 = fig.add_axes([0.3,0.71,0.6,0.2])
Y = linkage(Z,method='complete',metric='cosine')
Z2 = sch.dendrogram(Y)
ax2.set_xticks([])
ax2.set_yticks([])

#ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
#Z1 = sch.dendrogram(Y, orientation='right')
#ax1.set_xticks([])
#ax1.set_yticks([])

# Plot distance matrix.
axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
idx1 = Z2['leaves']
idx2 = Z2['leaves']

DZ = cdist(Z, Z, metric='cosine')
DZ = DZ[idx1,:][:,idx2]

im = axmatrix.matshow(DZ, aspect='auto', origin='upper', cmap=plt.cm.YlGnBu)
axmatrix.set_xticks([])
axmatrix.set_yticks([])

WORDS = WORDS[idx1]

for k,words in enumerate(WORDS):

    words = [w if "EMOJI_" not in w else
             emoji.emojize(":"+w.replace("EMOJI_","")+":", use_aliases=True)
             for w in words]
    print "idx", k
    print ' '.join(words)
    print

fs = 20
    
plt.xlabel(emoji_name,fontsize=30)
f_png = "figures/{}.png".format(target)
plt.savefig(f_png,bbox_inches=0)
sns.plt.show()
exit()


'''
cluster_V = V[ np.argsort(y_labels) ] 
affinity_DV = cdist(cluster_V, cluster_V, metric='cosine')
# Fix rounding errors, make strictly >= 0
affinity_DV[affinity_DV<0] = 0

y_labels = y_labels[idx]

import seaborn as sns
plt = sns.plt

fig = plt.figure()
sns.heatmap(affinity_DV,xticklabels=False,yticklabels=False,linewidths=0)
sns.plt.show()
exit()

'''
# generate the linkage matrix

#sns.heatmap(DV,xticklabels=False,yticklabels=False,linewidths=0)
#plt.figure()




plt.show()



