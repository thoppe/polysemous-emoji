import os, time, json, codecs
import tweepy
from src.emoji_handler import load_emoji

# Load the config files
from configobj import ConfigObj
config = ConfigObj("config.ini")

f_auth = config["scrape"]["auth_token_file"]
cred   = ConfigObj(f_auth)

# Create the data directory
cmd = "mkdir -p {input_data_directory}"
os.system(cmd.format(**config))

EM = load_emoji(config["scrape"]["f_emoji"])

# Basic stream listener

class StdOutListener(tweepy.streaming.StreamListener):

    def on_data(self, data):
        js = json.loads(data)

        # Skip malformed tweets (empty)
        if "text" not in js:
            return True

        # Remove extra padding
        text = ' '.join(js["text"].split())

        # Skip obvious retweets
        if "RT @" == text[:4]:
            return True

        # Save to a new file every hour
        ts = time.time()
        ts = int(round(ts/3600))

        f_out = "tweets_{}.txt".format(ts)
        f_out = os.path.join(config["input_data_directory"], f_out)
                
        with codecs.open(f_out,'a','utf-8') as FOUT:
            FOUT.write(text+'\n')

        # If verbose, print tweets as them come
        if config["scrape"]["verbose"]:
            print text
        
        return True

    def on_error(self, status):
        print "Error", status


# Handles Twitter authetification & connection to Streaming API
L = StdOutListener()
auth = tweepy.OAuthHandler(cred["consumer_key"],
                           cred["consumer_secret"])

auth.set_access_token(cred["access_token"],
                      cred["access_token_secret"])
stream = tweepy.Stream(auth, L)

keywords = EM.values()

while True:
    try:
        stream.filter(languages=['en'],track=keywords)
    except:
        print "Stream error"
        time.sleep(10)
