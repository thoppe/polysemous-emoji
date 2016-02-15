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
                    sample   =wcon.as_float("sample"),
                    negative =wcon.as_int("negative"),
                    size     =wcon.as_int("model_size"),
                    min_count=wcon.as_int("min_count"))

model_size = 200
min_count = 30
features = Word2Vec(workers=8,
                    window=5,
                    negative=5,
                    sample=1e-5,
                    size=model_size,
                    min_count=min_count)


from parse import parsed_tweet_iterator
def split_token_iter():
    for t in parsed_tweet_iterator():
        yield t.split()


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
