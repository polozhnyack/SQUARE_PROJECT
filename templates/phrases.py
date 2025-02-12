import random
import json

from config.config import LUSTBOT_LINK

link = "https://t.me/+2u9IqLu6Gb43Njli"

with open("templates/static_text.json", "r", encoding="utf-8") as file:
    data = json.load(file)

RECOMEND_MSG = [
    f"__**{random.choice(data["recommendation"]).upper()}**__\n\n__**FORWARD THIS POST OR COPY THE LINK FROM THE BIO**__"
]
if isinstance(RECOMEND_MSG, list):
    RECOMEND_MSG = random.choice(RECOMEND_MSG)
# texts_with_link = [f"__**{text.upper()}**__" + f"\n\n__**Forward this post or copy the link from the bio**__".upper() for text in RECOMEND_TEXT]

# RECOMEND_MSG = random.choice(texts_with_link)


water_mark = "[**SUBSCRIBE 👉 🔥LUSTSQUARE🔥**](https://t.me/+omFU55gPbi0xYzYy)"

watermark_proposal = f"\n\n👤 *Submitted via [LUSTBOT]({LUSTBOT_LINK})📢👀*\n\n{water_mark}"

start_proposal_text = r"""
*Hello\! 👋 Welcome to LUSTBOT 🔥\!*

Here, you can:
\- 💡 *Share your ideas or suggestions* for our project\.
\- 📩 *Send us your content* to be featured\.
\- 🤝 *Get in touch with the admins* for any inquiries or issues\.
\- ❗ *The bot will not send you any advertisements*\.

Your suggestions are *anonymous*\.
However, please note that sending *prohibited or inappropriate content*:
\- 🚫 Will *not be reviewed*\.
\- 🛑 May result in a *ban from the bot*\.

Simply type your message or attach media, and we’ll forward it as a suggestion\.
Thank you for contributing\! 🙏
"""

agitation_text = f"🌟 **HI SWEETIES!** 🌟\n\n__**IF YOU LIKE OUR CHANNEL,**__ [SUPPORT US](https://t.me/boost?c=1528886598) 🎉\n\n✔️ __NO ADS – ONLY USEFUL CONTENT FOR YOU!__\n__✔️THE ATMOSPHERE HERE IS ALWAYS FRIENDLY AND WE APPRECIATE EACH AND EVERY ONE OF YOU!__ 🤗\n✔️ __WE ARE ACTIVELY DEVELOPING AND ALWAYS WELCOME NEW IDEAS!__ 💡\n\n**ALSO, DON"T FORGET TO UPDATE OUR CHANNEL WITH YOUR CONTENT VIA** [LUSTBOT]({LUSTBOT_LINK})"
