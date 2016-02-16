import emoji

# Load the config files
from configobj import ConfigObj
config = ConfigObj("config.ini")
wcon = config["word2vec"]

from gensim.models.word2vec import Word2Vec
f_features = wcon["f_features"].format(**wcon)

clf = Word2Vec.load(f_features)
EM = [w for w in clf.index2word if "EMOJI_" in w][:40]

for word in EM:
    sim = clf.most_similar(word, topn = 8)
    name = ':'+word[6:]+':'
    symbol = emoji.emojize(name,use_aliases=True)
    print word + " " + symbol +' ' + ' '.join([x[0] for x in sim])

