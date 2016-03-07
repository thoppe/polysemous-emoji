<style>.emoji {color:#EF597B;} </style>
  
# polysemous emoji <span class="emoji">🌹</span>
----------
### [Travis Hoppe](http://thoppe.github.io/) / [@metasemantic](https://twitter.com/metasemantic)

====

## *Polysemy*: One word, many senses

### I put money in the _bank_.
### The ball when in with a _bank_ shot.
### Drive carefully around the snow _bank_.
### I went fishing in the river _bank_.
====+
<br>
## What about emoji? <span class="emoji">😍 😘 😂 ❤ 😭  💯 </span>
   
====
## Data collection

Gathered all tweets that contained the [top 200 emoji](http://emojitracker.com/).
Approximately 80,000 per hour, 13,000,000 total.

## Data QC (spam tweets)

Removed exactly identical tweets.
Removed tweets that only differ by index:

"Hello baby @justinbieber Can u follow me? ♥ x37"
"Hello baby @justinbieber Can u follow me? ♥ x38"
"Hello baby @justinbieber Can u follow me? ♥ x39"
  
====*

## Data Wrangling

Built a pipeline for repeatable processing:

`remove_mentions, remove_urls, HTML_symbols, remove_apostrophe, space_symbols, special_lowercase, replace_emoji, limit_character_subset, remove_repeated_tokens, remove_twitter_mentions_hashtags, remove_emoji_modifier`

Special care: Emoji's have [skin tone](http://emojipedia.org/emoji-modifier-fitzpatrick-type-1-2/) which count as an extra character. 
TIL: Fitzpatrick is the name of the skin tone scale.

====*

## Machine Learning
Train `word2vec` over tweets and consider emojis as a qualified "word"
!(figures/similarity_map.png) <<height:700px>>

====


# Thanks, you!
[@metasemantic](https://twitter.com/metasemantic)