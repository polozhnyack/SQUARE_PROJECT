import random
import json

from config.config import LUSTBOT_LINK

link = "https://t.me/+2u9IqLu6Gb43Njli"

with open("templates/static_text.json", "r", encoding="utf-8") as file:
    data = json.load(file)

RECOMEND_MSG = [
    f"__**{random.choice(data['recommendation']).upper()}**__\n\n__**FORWARD THIS POST OR COPY THE LINK FROM THE BIO**__"
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

agitation_text = f"🌟 **HI SWEETIES!** 🌟\n\n__**IF YOU LIKE OUR CHANNEL,**__ [SUPPORT US](https://t.me/boost?c=1528886598) 🎉\n\n✔️ __NO ADS – ONLY USEFUL CONTENT FOR YOU!__\n__✔️THE ATMOSPHERE HERE IS ALWAYS FRIENDLY AND WE APPRECIATE EACH AND EVERY ONE OF YOU!__ 🤗\n✔️ __WE ARE ACTIVELY DEVELOPING AND ALWAYS WELCOME NEW IDEAS!__ 💡\n\n**ALSO, DON'T FORGET TO UPDATE OUR CHANNEL WITH YOUR CONTENT VIA** [LUSTBOT]({LUSTBOT_LINK})"




SPAM_MESSAGE = [
    '🔥 EŔOTIC HÛB FOR Ť₲ 🔞\n\n🤩__ϜΙΝD МORE__✨ 👉 ',
    '🔥 SÉX CLÚB IN Ť₲ 🔞\n\n🤩__ϜΙΝD ΜΑGİС__✨ 👉 ',
    '🔥 PLEÀSÛRE ZØNE HUB IN Ť₲ 🔞\n\n🤩__ϜΙΝD ƳÕÛŘ SPOT__✨ 👉 ',
    '🔥 EΧCŁUSIVE PØRN IN TG 🔞\n\n🤩__ϜΙΝD MØRE__✨ 👉 ',
    '🔥 TOP SƏX HÛB IN TG 🔞\n\n🤩__ϜΙΝD THE BƏST__✨ 👉 ',
    '🔥 HØT PØRNØ HUB IN TG 🔞\n\n🤩__ϜΙΝD YÕÛŘ CLÍÇK__✨ 👉 ',
    '🔥 ADULT LÛST HUB IN Ť₲ 🔞\n\n🤩__ϜΙΝD YÕÛR ŤASŤE__✨ 👉 ',
    '🔥 BEST 18+ HÛB FOR Ť₲ 🔞\n\n🤩__ϜΙΝD HØŤ SŤÛFF__✨ 👉 ',
    '🔥 ADULT SCÈNËS HUB IN TG 🔞\n\n🤩__ϜΙΝD MØRE THRİLL__✨ 👉 ',
    '🔥 PØRN VİP ZONE IN Ť₲ 🔞\n\n🤩__ϜΙΝD YØUR BLISS__✨ 👉 ',
    '🔥 BΞST ADULT HÛB IN Ť₲ 🔞\n\n🤩__ϜΙΝD SÉXÎNESS__✨ 👉 ',
    '🔥 TØP 18+ HÛB FOR TG 🔞\n\n🤩__ϜΙΝD WILD VİBES__✨ 👉 ',
    '🔥 PRÉMÎUM PØRN HUB IN TG 🔞\n\n🤩__ϜΙΝD YØUR FAV__✨ 👉 ',
    '🔥 RÀW PØRN HUB IN TG 🔞\n\n🤩__ϜΙΝD NØ.1 CHØICE__✨ 👉 ',
    '🔥 SÛPERIOR 18+ HUB IN Ť₲ 🔞\n\n🤩__ϜΙΝD EXCÎTEMNT__✨ 👉 ',
    '🔥 NØ.1 PØRN ZØNË IN TG 🔞\n\n🤩__ϜΙΝD THË TOP__✨ 👉 ',
    '🔥 BEST ADÛLŤ HÛB IN TG 🔞\n\n🤩__ϜΙΝD YOUR FÙN__✨ 👉 ',
    '🔥 18+ EXCŁÛSİVÉ HUB IN TG 🔞\n\n🤩__ϜΙΝD ADÛLŤ FUN__✨ 👉 ',
    '🔥 PRØ PØRN SCENES HUB IN TG 🔞\n\n🤩__ϜΙΝD YOUR VÎBES__✨ 👉 ',
    '🔥 HØTTËST ADULT HUB IN TG 🔞\n\n🤩__ϜΙΝD SPÎCÝ CLÎCK__✨ 👉 ',
    '🔥 TØP EROTIC ZØNË IN Ť₲ 🔞\n\n🤩__ϜΙΝD YØUR PASSIØN__✨ 👉 ',
    '🔥 NŞFW PØRN HUB IN TG 🔞\n\n🤩__ϜΙΝD THË FÎRE__✨ 👉 ',
    '🔥 HØTTÈST CLÎPS IN Ť₲ 🔞\n\n🤩__ϜΙΝD THRÎLL__✨ 👉 ',
    '🔥 18+ ŤØP HUB IN Ť₲ 🔞\n\n🤩__ϜΙΝD LÛŚT__✨ 👉 ',
    '🔥 SÊXIEST PØRN HUB IN TG 🔞\n\n🤩__ϜΙΝD ÊXCITEMENT__✨ 👉 ',
    '🔥 NO.1 PØRN ËXPËRIENCE IN TG 🔞\n\n🤩__ϜΙΝD THË HØTTEST__✨ 👉 ',
    '🔥 NÕ.1 HÛB FOR SEX CLIPS IN TG 🔞\n\n🤩__ϜΙΝD WÎLD VIBES__✨ 👉 ',
    '🔥 EXCLÛSİVË 18+ CONTENT IN Ť₲ 🔞\n\n🤩__ϜΙΝD FUN__✨ 👉 ',
    '🔥 BEST NSFW HÛB IN Ť₲ 🔞\n\n🤩__ϜΙΝD THE MØST__✨ 👉 ',
    '🔥 TØP ADULT CLIPS IN TG 🔞\n\n🤩__ϜΙΝD YØUR PLEASURE__✨ 👉 ',
    '🔥 SÎZZLING PØRN HUB IN TG 🔞\n\n🤩__ϜΙΝD THË BÉST__✨ 👉 ',
    '🔥 A-CLASS PØRN CHANNEL IN TG 🔞\n\n🤩__ϜΙΝD YOUR FAVS__✨ 👉 ',
    '🔥 RÊAL ADULT HUB IN TG 🔞\n\n🤩__ϜΙΝD THE PLEASURE__✨ 👉 ',
    '🔥 BÎG PØRN CLÎPS IN Ť₲ 🔞\n\n🤩__ϜΙΝD THE SÎZZLE__✨ 👉 ',
    '🔥 NO.1 EXCLUSIVE PØRN IN TG 🔞\n\n🤩__ϜΙΝD LÛXÛRY__✨ 👉 ',
    '🔥 ELÎTE ADULT HUB IN TG 🔞\n\n🤩__ϜΙΝD HØTTEST CLÎCK__✨ 👉 ',
    '🔥 WÎLD PØRN HUB IN TG 🔞\n\n🤩__ϜΙΝD FÛLL FUN__✨ 👉 ',
    '🔥 PLEASÛRABLE PØRN HUB IN TG 🔞\n\n🤩__ϜΙΝD THE FANTASY__✨ 👉 ',
    '🔥 N°1 ADULT ZØNË IN TG 🔞\n\n🤩__ϜΙΝD FÎRE INSIDE__✨ 👉 ',
    '🔥 FÙLL ADÛLŤ HUB IN TG 🔞\n\n🤩__ϜΙΝD YØUR JOY__✨ 👉 '
]
