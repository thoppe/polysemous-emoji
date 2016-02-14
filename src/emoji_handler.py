import emoji


def load_emoji(f_emoji_list):
    
    emoji_chars = {}

    with open(f_emoji_list) as FIN:

        for line in FIN:
            text = line.strip()
            if not text: continue
            key = ":{}:".format(text)
            val = emoji.emojize(key,use_aliases=True)
            assert key != val, "{} not an emoji".format(key)
            emoji_chars[text] = val

    print "Loaded {} emoji.".format(len(emoji_chars))

    return emoji_chars
