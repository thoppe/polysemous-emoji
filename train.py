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
                    sample   =wcon.as_float("sample"),
                    window   =wcon.as_int("window"),
                    negative =wcon.as_int("negative"),
                    size     =wcon.as_int("model_size"),
                    min_count=wcon.as_int("min_count"))

from parse import parsed_tweet_iterator
def split_token_iter():
    with open("all_parsed_tweets.txt") as FIN:
        for line in FIN:
            yield line.split()

print "Learning the vocabulary"
ITR = split_token_iter()
features.build_vocab(ITR)
print features

print "Training the features"
for n in range(wcon.as_int("epoch_n")):
    print " - Epoch {}".format(n)
    ITR = split_token_iter()
    features.train(ITR)

print "Reducing the features"
features.init_sims(replace=True)

print features

print "Saving the features"
import os
os.system('mkdir -p clf')
f_features = wcon["f_features"].format(**wcon)
features.save(f_features)
