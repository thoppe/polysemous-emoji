import codecs, glob, os

# Load the config files
from configobj import ConfigObj
config = ConfigObj("config.ini")

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
def tweet_iterator():
    data_dir = config["input_data_directory"]
    F = glob.glob(os.path.join(data_dir,"*"))
    for f in F:
        with codecs.open(f,'r','utf-8') as FIN:
            for line in FIN:
                yield line.strip()

def dispatcher(x):
    return reduce(lambda x, f: f(x), parser_functions, x)

###################################################################
INPUT_ITR = tweet_iterator()

if config["parse"]["multiprocessing"].as_bool("active"):
    import multiprocessing
    MP = multiprocessing.Pool()
    ITR = MP.imap(dispatcher, INPUT_ITR)
else:
    import itertools
    ITR = itertools.imap(dispatcher, INPUT_ITR)


for t in ITR:
    print t
                    
