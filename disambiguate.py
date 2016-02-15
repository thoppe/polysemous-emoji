from ksvd import KSVD
import h5py, os

# Load the config files
from configobj import ConfigObj
wcon = ConfigObj("config.ini")["word2vec"]
kcon = ConfigObj("config.ini")["kSVD"]

#from gensim.models.word2vec import Word2Vec
#f_features = wcon["f_features"].format(**wcon)
#clf = Word2Vec.load(f_features)

f_model = kcon["f_kSVD"].format(**kcon)
h5 = h5py.File(f_model,'r')
D = h5["D"]
gamma = h5["gamma"]

print gamma[:][0]
