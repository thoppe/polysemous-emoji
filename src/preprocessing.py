import glob, codecs, re, string
import HTMLParser


def pipeline_function(func):
    
    class joint(object):
        def __init__(self,*args,**kwargs):
            # Set any function arguments for calling
            self.kwargs = kwargs
            
        def __call__(self, x):
            return func(x, **self.kwargs)
        
    return joint

@pipeline_function
def remove_mentions(t):
    '''
    Replaces @ mentions with just the @ symbol.
    '''   
    out = []
    for t in t.split():
        if t[0] == "@":
            t = "@"
        out.append(t)
    return ' '.join(out)

@pipeline_function
def remove_urls(t, replace_string):
    '''
    Simple regex removal of http and https matching urls.
    '''
    t = re.sub(r"(?:\@|https?\://)\S+", replace_string, t)
    t = re.sub(r"(?:\@|http?\://)\S+", replace_string, t)
    return t
    
@pipeline_function
def remove_apostrophe(t):
    '''
    Completely remove any apostrophe.
    '''
    return t.replace("'","")

saved_space_chars = string.letters + string.digits + string.whitespace + '#'

@pipeline_function
def space_symbols(t):
    '''
    If a character isn't a digit or string, make it a new token.
    '''
    tokens = [x if x in saved_space_chars else ' '+x+' ' for x in t]
    tokens = ' '.join(''.join(tokens).split())
    return tokens

HP = HTMLParser.HTMLParser()
@pipeline_function
def HTML_symbols(t):
    '''
    Unescape any weird HTML codes like &amp;
    '''
    return HP.unescape(t)



@pipeline_function
def special_lowercase(t):
    '''
    Map tokens to lowercase if there isn't a caps after the first
    character.
    '''
    out = []
    for token in t.split():

        if len(token) > 1 and token[1:].lower() == token[1:]:
            token = token.lower()
            
        out.append(token)
        
    return ' '.join(out)


@pipeline_function
def replace_emoji(t, prefix, table):
    '''
    Replace the emoji dict with a word token
    '''
    t = [prefix+table[token] if token in table.keys()
         else token for token in t.split()]
    return ' '.join(t)


saved_limit_characters = set(saved_space_chars + '@')

@pipeline_function
def limit_character_subset(t):
    '''
    Removes single character tokens not matching a specific set,
    useful if `space_symbols` has been run already.
    '''
    out = []
    for token in t.split():

        if len(token) > 1 or token in saved_limit_characters:
            out.append(token)
        
    return ' '.join(out)
