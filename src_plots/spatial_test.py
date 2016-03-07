from __future__ import division

import h5py, os
import numpy as np
from scipy.spatial.distance import pdist
from scipy.misc import factorial

dim = 200
def random_hypersphere_point(dim):
    pts = np.random.normal(size=dim)
    return pts / np.linalg.norm(pts)

# Load the config files
from configobj import ConfigObj
wcon = ConfigObj("config.ini")["word2vec"]
kcon = ConfigObj("config.ini")["kSVD"]

from gensim.models.word2vec import Word2Vec
f_features = wcon["f_features"].format(**wcon)
clf = Word2Vec.load(f_features)
X = clf.syn0


X = X[0:1000]
dist1 = pdist(X,metric='cosine')
n,dim = X.shape

print X.shape

rand_pts = [random_hypersphere_point(dim) for _ in xrange(n)]
dist2 = pdist(rand_pts,metric='cosine')


import seaborn as sns
sns.distplot(dist1, label="w2vec")
sns.distplot(dist2, label="random points")
sns.plt.legend(fontsize=18, loc="best")
sns.plt.title("All pairwise distances of w2vec over {}-d hypersphere".format(dim))
sns.plt.xlim(0,2)
os.system('mkdir -p figures')
f_png = 'figures/hypersphere_dist.png'
sns.plt.savefig(f_png, bbox_inches=None)
sns.plt.show()
