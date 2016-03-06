from collections import Counter, defaultdict
import os, tqdm
import numpy as np
from scipy.ndimage.measurements import label
import itertools, multiprocessing
# rm -f all_unique_tweets.txt && cat all_parsed_tweets.txt | unique all_unique_tweets.txt


ngrams = defaultdict(Counter)
total_tweets = 10984240

f_tweets = "all_unique_tweets.txt"

def solve_mask(line):

    tokens = np.array(line.split())
    emoji_mask = [1 if "EMOJI_" in x else 0 for x in tokens]

    if sum(emoji_mask) < 2:
        return None

    feature_mask, n_features = label(emoji_mask, structure=[1,1,1])

    return (tokens, feature_mask, n_features)
    

with open(f_tweets) as FIN:
    pbar = tqdm.tqdm(total=total_tweets)

    #ITR = itertools.imap(solve_mask, FIN)
    MP = multiprocessing.Pool()
    ITR = MP.imap(solve_mask, FIN,chunksize=100)
    
    for k,result in enumerate(ITR):

        pbar.update()

        if result is None: continue
        tokens, feature_mask, n_features = result

        for n in range(1,n_features+1):
            idx = feature_mask == n
            size = sum(idx)
            if size>=2:
                block = tuple(tokens[idx])
                ngrams[size].update((block,))

    pbar.close()

os.system('mkdir -p collated')

for n in range(2, 50):
    if not ngrams[n]: continue

    f_save = "collated/ngram_emoji_{}.txt".format(n)

    with open(f_save,'w') as FOUT:
        print "Saving", f_save
    
        for item,count in ngrams[n].most_common():

            s = ' '.join([x.replace("EMOJI_","") for x in item])
            FOUT.write("{} {}\n".format(count,s))
            
