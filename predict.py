from src.emoji_handler import load_emoji

# Load the config files
from configobj import ConfigObj
config = ConfigObj("config.ini")
wcon = config["word2vec"]

from gensim.models.word2vec import Word2Vec
f_features = wcon["f_features"].format(**wcon)

clf = Word2Vec.load(f_features)
EM = load_emoji(config["scrape"]["f_emoji"])

for word in EM:
    sim = clf.most_similar("EMOJI_{}".format(word), topn = 8)
    print word, EM[word] + u' ' + u' '.join([x[0] for x in sim])


