from gensim.models.word2vec import Word2Vec

# Load the config files
from configobj import ConfigObj
wcon = ConfigObj("config.ini")["word2vec"]

# Measure the number of CPU cores
import psutil
workers = psutil.cpu_count()
print "Using {} cores to train the model".format(workers)

# Build the model
features = Word2Vec(workers  =workers,
                    window   =100,
                    sample   =wcon.as_float("window"),
                    negative =wcon.as_int("negative"),
                    size     =wcon.as_int("model_size"),
                    min_count=wcon.as_int("min_count"))

from parse import parsed_tweet_iterator


INPUT_ITR = parsed_tweet_iterator()

print "Learning the vocabulary"
features.build_vocab(INPUT_ITR)

print features
