import random
import json

from config.config import LUSTBOT_LINK

with open("templates/static_text.json", "r", encoding="utf-8") as file:
    data = json.load(file)

agit_text = data['agitation_text']
water_mark = data['watermark']
watermark_proposal = data['watermark_proposal']

RECOMEND_MSG = [
    f"__**{random.choice(data["recommendation"]).upper()}**__\n\n__**FORWARD THIS POST OR COPY THE LINK FROM THE BIO**__"
]
if isinstance(RECOMEND_MSG, list):
    RECOMEND_MSG = random.choice(RECOMEND_MSG)

SPAM_MESSAGE = random.choice(data["spam"])

def get_spam_message():
    return f"{random.choice(data["spam"])} @sqrhub"

watermark_proposal = watermark_proposal.replace("{LUSTBOT_LINK}", LUSTBOT_LINK).replace("{water_mark}", water_mark)

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

agitation_text = agit_text.format(LUSTBOT_LINK=LUSTBOT_LINK)