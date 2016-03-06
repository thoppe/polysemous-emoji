from collections import Counter

URL = {True : Counter(), False : Counter()}
MENTION = {True : Counter(), False : Counter()}

C = Counter()

with open("all_unique_tweets.txt") as FIN:
    for k,line in enumerate(FIN):
        tokens = line.split()

        em = [x.replace("EMOJI_","") for x in tokens if "EMOJI_" in x]
        em = set(em)

        C.update(tokens)

        if "URL" in tokens:
            URL[True].update(em)
        else:
            URL[False].update(em)

        if "@" in tokens:
            MENTION[True].update(em)
        else:
            MENTION[False].update(em)

        if k%10000==0:
            print k
                

        #if k>50000:
        #    break


import pandas as pd

keys = URL[True].keys()+URL[False].keys()+MENTION[True].keys()+MENTION[False].keys()
keys = set(keys) 

df = pd.DataFrame(index=keys)

df["URL1"] = 0.0
df["URL0"] = 0.0
df["MENTION1"] = 0.0
df["MENTION0"] = 0.0

for key,val in URL[True].items(): df["URL1"][key] = val
for key,val in URL[False].items(): df["URL0"][key] = val

for key,val in MENTION[True].items(): df["MENTION1"][key] = val
for key,val in MENTION[False].items(): df["MENTION0"][key] = val

for key in df:
    df[key] /= df[key].sum()

s = (df["URL1"]-df["URL0"])

s.sort()
with open("delta_url.txt",'w') as FOUT:
    for key in s.keys():
        st = "{:45s} {:0.4f}".format(key,s[key])
        FOUT.write(st+'\n')
        print st


s = (df["MENTION1"]-df["MENTION0"])
s.sort()
with open("delta_mention.txt",'w') as FOUT:
    for key in s.keys():
        st = "{:45s} {:0.4f}".format(key,s[key])
        FOUT.write(st+'\n')
        print st


s = pd.Series(C)
s.sort()

with open("delta_all.txt",'w') as FOUT:
    for key in s.keys():
        st = "{:45s} {:d}".format(key,s[key])
        FOUT.write(st+'\n')
        print st
        

    
