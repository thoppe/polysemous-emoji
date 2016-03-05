import pyparsing as pyr
import collections, os
import numpy as np

min_n, max_n = 2, 15

def repeat_block(expr, n=2):
    letter_block = pyr.Word(pyr.alphas)
    LB = pyr.Literal('{').suppress()
    RB = pyr.Literal('}').suppress()
    repeat_block = LB + letter_block + RB
    OB = pyr.Optional(letter_block)
    block = OB + repeat_block + OB
    repeat_block.setParseAction(lambda x:x[-1]*n)
    return ''.join(block.parseString(expr))

# Load the config files
from configobj import ConfigObj
wcon = ConfigObj("config.ini")["word2vec"]

# Load the low entropy words
low_E = []
with open("low_entropy_words.txt") as FIN:
    for line in FIN:
        low_E.append(line.strip())

# Load this special raw count since clf cuts of at min_word
with open("delta_all.txt") as FIN:
    C = collections.Counter()
    for line in FIN:
        word,count = line.split()
        word = word.lower()
        if not word.isalpha():
            continue
        
        C[word] += int(count)


# Compute the repeated letter freqs
data = []
for word in low_E:
    for n in range(min_n, max_n+1):
        rword = repeat_block(word,n)
        val = C[rword] if rword in C else 0
        data.append([word,n,val])

# Create a dataframe
import pandas as pd
df = pd.DataFrame(data=data, columns=["word",'n','count'])

import seaborn as sns
plt = sns.plt    
fig = plt.figure(figsize=(14,10))

colors = sns.color_palette("hls", 5)

for word,block in df.groupby("word"):
    if True:#len(word)>=6:
        Y = block['count']
        X = block['n']
        Y /= Y.sum()

        max_idx = X[Y.argmax()]
        color_idx = max_idx-2
        plt.plot(X,Y, label=word, color=colors[color_idx])

plt.legend(ncol=4,fontsize=18)
plt.xlim(2,12)
plt.xlabel("number of repeats",fontsize=18)
plt.ylabel("probability",fontsize=18)
plt.xticks(range(min_n, max_n))

os.system('mkdir -p figures')
f_png = 'figures/repeated_letters.png'
plt.savefig(f_png, bbox_inches=None)
plt.show()
