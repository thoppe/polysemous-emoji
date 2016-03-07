import glob, emoji

n = 2

#F_NP = sorted(glob.glob("collated/ngram_emoji_?.txt"))
F_NP = sorted(glob.glob("collated/ngram_emoji_{}.txt".format(n)))


for f in F_NP:
    with open(f) as FIN:
        for k,line in enumerate(FIN):
            tokens = line.split()
            count = tokens[0]
            tokens= tokens[1:]
            em = [emoji.emojize(":{}:".format(s)) for s in tokens]
            s = ' '.join(em)
            if len(set(em))==n:
                print s, count
            if k>20:break
    exit()
        
