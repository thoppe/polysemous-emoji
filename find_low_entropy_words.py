from __future__ import division
import collections, os

# Load the config files
from configobj import ConfigObj
wcon = ConfigObj("config.ini")["word2vec"]

from gensim.models.word2vec import Word2Vec
f_features = wcon["f_features"].format(**wcon)
clf = Word2Vec.load(f_features)

words = clf.index2word[:]

# Remove emoji and non-alphawords and drop to lowercase
words = [w.lower() for w in words if w.isalpha()]

# Only keep words larger than 6 letters
words = [w for w in words if len(w)>4]

os.system('mkdir -p collated')

# Compute n-gram freq
for n in [1,2,3,4]:
    gram = collections.Counter()
    for w in words:
        if len(w) < n: continue
        
        tokens = [w[k:k+n] for k in range(len(w)-n+1)]
        gram[w] = -len(set(tokens)) / len(tokens)

    small = [w for w,v in gram.most_common(10000) if v>-0.45]
    small = sorted(small)
    print small

    f_save = os.path.join("collated","low_entropy_{}.txt".format(n))
    with open(f_save,'w') as FOUT:
        for w in small:
            FOUT.write(w+'\n')
