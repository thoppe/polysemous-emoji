import codecs, glob, os, itertools
from src.emoji_handler import load_emoji

# Load the config files
from configobj import ConfigObj
config = ConfigObj("config.ini")

# Load the emojis as a config
EM = load_emoji(config["scrape"]["f_emoji"])
# Reverse the table
EM_rev = {v: k for k, v in EM.items()}
config["parse"]["replace_emoji"]["table"] = EM_rev

# Import the preprocessing data
import src.preprocessing as pre

# Fill the pipeline with function objects
parser_functions = []
for name in config["parse"]["pipeline"]:
    obj  = getattr(pre,name)

    # Load any kwargs in the config file
    kwargs = {}
    if name in config["parse"]:
        kwargs = config["parse"][name]

    parser_functions.append( obj(**kwargs) )


###################################################################

# Iterates through all the tweets downloaded
def tweet_iterator(limit):
    data_dir = config["input_data_directory"]
    F = glob.glob(os.path.join(data_dir,"*"))
    counter = itertools.count()
    
    for f in F:
        with codecs.open(f,'r','utf-8') as FIN:
            for line in FIN:
                yield line.strip()

                c = counter.next()
                print c
                
                if limit and limit < c:
                    raise StopIteration

def dispatcher(x):
    return reduce(lambda x, f: f(x), parser_functions, x)

###################################################################

def parsed_tweet_iterator():

    limit = config["parse"].as_int("limit")
    INPUT_ITR = tweet_iterator(limit=limit)
    
    if config["parse"].as_bool("multiprocessing"):
        cs = config["parse"].as_int("multiprocessing_chunksize")
        import multiprocessing
        MP = multiprocessing.Pool()
        ITR = MP.imap(dispatcher, INPUT_ITR,chunksize=cs)
    else:
        ITR = itertools.imap(dispatcher, INPUT_ITR)

    return ITR


if __name__ == "__main__":
       
    for t in parsed_tweet_iterator():
        print t
                    
