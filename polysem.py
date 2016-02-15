from ksvd import KSVD
import h5py, os
from gensim.models.word2vec import Word2Vec

# Load the config files
from configobj import ConfigObj
wcon = ConfigObj("config.ini")["word2vec"]
kcon = ConfigObj("config.ini")["kSVD"]

from gensim.models.word2vec import Word2Vec
f_features = wcon["f_features"].format(**wcon)
clf = Word2Vec.load(f_features)
X = clf.syn0

print clf
print X.shape

result = KSVD(X,
              dict_size=kcon.as_int("basis_size"),
              target_sparsity=kcon.as_int("sparsity"),
              max_iterations=kcon.as_int("iterations"),
              enable_printing=True,
              enable_threading = True,
              print_interval=1)

D,gamma = result

f_model = kcon["f_kSVD"].format(**kcon)

h5 = h5py.File(f_model,'w')
h5.create_dataset("D",data=D, compression="gzip")
h5.create_dataset("gamma",data=gamma, compression="gzip")

# Save the arguments (maybe later?)
#for key in args:
#    g.attrs[key] = cargs[key]

h5.close()
