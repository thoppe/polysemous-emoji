from ksvd import KSVD
import h5py, os
import emoji

# Load the config files
from configobj import ConfigObj
config = ConfigObj("config.ini")
wcon = config["word2vec"]
kcon = config["kSVD"]

# Load kSVF
f_model = kcon["f_kSVD"].format(**kcon)
h5 = h5py.File(f_model,'r')
D = h5["D"]
gamma = h5["gamma"]
k = D.shape[0]

# Load word2vec wordmap
from gensim.models.word2vec import Word2Vec
f_features = wcon["f_features"].format(**wcon)
clf = Word2Vec.load(f_features)

# Build a lookup for row->word
import numpy as np
words_index = np.array(clf.index2word)
words = dict(zip(words_index,range(len(words_index))))

EM = [w for w in clf.index2word if "EMOJI_" in w][:40]
del clf


# "define" the dense vectors
describe_n = 6

sparse_importance = gamma[:].sum(axis=0)
sparse_idx = np.argsort(sparse_importance)[::-1]
sparse_desc = {}
print "Showing examples of the spare vectors"

for n,i in enumerate(sparse_idx):
    #print gamma[:,i].sum()
    idx = np.argsort( gamma[:,i] )[-describe_n:]
    weights = gamma[:,i][idx]

    sparse_desc[i] = words_index[idx]
    if n < 15:
        print sparse_importance[i], sparse_desc[i]


print

for key in EM:
    name = ':'+w[6:]+':'
    symbol = emoji.emojize(name,use_aliases=True)
    idx = words[key]
    g   = gamma[idx]

    non_zero_items = np.where(g!=0)[0]
    
    print key, g[g!=0]
    for i in non_zero_items:

        if sparse_importance[i]>0 and g[i]>0:
            print "{:0.4f} {:0.4f} {}".format(g[i], sparse_importance[i], sparse_desc[i])
    print

    


