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
## 1. Data collection

Gathered all tweets that contained the [top 200 emoji](http://emojitracker.com/).
Approximately 80,000 per hour, 13,000,000 total.

## 2. Data QC (spam tweets)

Removed exactly identical tweets.
Removed tweets that only differ by index:
  
"Hello baby @justinbieber Can u follow me? <span class="emoji">♥</span> x37"
"Hello baby @justinbieber Can u follow me? <span class="emoji">♥</span> x38"
"Hello baby @justinbieber Can u follow me? <span class="emoji">♥</span> x39"
  
====*

## 3. Data Wrangling

Built a pipeline for repeatable processing:

`remove_mentions, remove_urls, HTML_symbols, remove_apostrophe, space_symbols, special_lowercase, replace_emoji, limit_character_subset, remove_repeated_tokens, remove_twitter_mentions_hashtags, remove_emoji_modifier`

Special care: Emoji have [skin tone](http://emojipedia.org/emoji-modifier-fitzpatrick-type-1-2/) which count as an extra character. 
TIL: Fitzpatrick is the name of the skin tone scale.

====*

## 4. Machine Learning
Train `word2vec` over tweets and consider emojis as a qualified "word"

## 5. _What can we learn?_
Habits of highly emotive people...

====
## Emoji have synonyms and antonyms
!(figures/similarity_map.png) <<height:700px>>
====
### There is an optimal length to _omggggggg_
!(figures/repeated_letters.png) <<height:700px>>
====
### `word2vec` spreads vectors across the hypersphere
!(figures/hypersphere_dist.png) <<height:700px>>
====
## Polysemous emoji!
!(figures/EMOJI_key.png) <<height:500px>>
!(figures/EMOJI_skull.png) <<height:500px>>
!(figures/EMOJI_smiling_face_with_open_mouth_and_smiling_eyes.png) <<height:500px>>

Sample tweets containing target emoji, compute mean w2vec of each tweet, run low order affinity propagation, cluster and interpret vectors near clusters.
====*
## What is a <span class="emoji">🔑</span> ?
!(figures/EMOJI_key.png) <<height:500px>>
  
#### major success is key consistency communication knowledge growth life
  or
## ❤ 💜 @ 😘 ❣ 💛 💖 💞 💝

====*
## What is a <span class="emoji">💀</span> ?
!(figures/EMOJI_skull.png) <<height:500px>>

### 🙃 after 😐 before I literally 😑 😕 just
  or
### WOAH LMAO LMFAO lmfao LMFAOOOO 😂 lmao
  
====

## Can we automate this?

## <span class="emoji">😂 😍 😭 😊  ❤ 😩 😘 💕  😒 😁 💯 😉  😏 😌   😔  💖 👀 😎 ♥  😢 😴 💙 😑  👌 💘 😕 🎶 💜 👍 ☺ 😳 ✨ 😄 😋 😪 😜 🙈  😞 😐 🙏 🙌 💔 👏 ▶ ✌ 👇 🔥 💁  💩 💀 💋 💗 🎉 💞  👉 👊 🌹 💓 👑 ‼  💪 💛 💚 🙊 😇 😈 😻 ➡ 😚 😛 😱 ✔ 😆 🌸 😝 </span> ...

====
  
# Thanks, you!
[@metasemantic](https://twitter.com/metasemantic)