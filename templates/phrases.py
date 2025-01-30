import random
from config.config import LUSTBOT_LINK

RECOMEND_MSG_1 = """
💋 Sweeties, share this channel with your friends and acquaintances 🤗💖 so they can also improve their mood and watch new content every day 😘🔞
👇👇👇

https://t.me/+2u9IqLu6Gb43Njli
https://t.me/+2u9IqLu6Gb43Njli
https://t.me/+2u9IqLu6Gb43Njli
"""

RECOMEND_TEXT = [
    "Hey sweeties, share this channel with your friends and acquaintances 🤗💖 so they can also boost their mood and watch fresh content every day 😘🔞🔥",
    "Hello lovelies! 💋 Spread the word and share this channel with your friends and loved ones 🤗💖 Let them enjoy new content and positive vibes every day 😘🔞💋",
    "Sweeties, don’t forget to share this channel with your friends so they too can enjoy fresh content and keep their mood high every day 😘💖🔞🔥",
    "Hey everyone, share this channel with your friends and acquaintances 🤗💖 so they can get a daily dose of fun and new content 😘🔞💥",
    "Hey beautiful souls 💋 Share this channel with your friends and spread the love 💖 Let them enjoy new content and daily happiness 😘🔞🔥",
    "Hey sweethearts! 💖 Don’t keep the fun to yourself – share this channel with friends and family so they can also enjoy fresh content daily 😘🔞🔥",
    "Hey gorgeous people 💋 Share this channel with those who matter to you and help them improve their mood with fresh content every day 🤗💖🔞💥",
    "Sweeties, pass this channel along to your friends so they too can watch new content every day and feel the joy 😘💖🔞💋",
    "Hi darlings 💋 Share this channel with your friends and acquaintances 🤗💖 Let them enjoy daily content and keep their spirits up 😘🔞💥",
    "Darling, share this channel with your friends so they can have access to fresh content and positive vibes every day 😘💖🔞💋",
    "Lovely people, don’t keep this treasure to yourself! Share this channel with your friends and spread the joy every day 💖😚🔞🔥",
    "Share the love, sweeties 💋 Let your friends know about this channel and let them also enjoy new content and keep their mood lifted 😘🔞💋",
    "Hello there, beautiful! 💋 Spread the good vibes by sharing this channel with your friends and let them watch fresh content every day 😘💖🔞🔥",
    "Hey sweetie, share this channel with those who deserve to feel good and enjoy new content daily 🤗💖 Let them join the fun 😘🔞💥",
    "Friends, share this channel with your loved ones so they can enjoy new content and stay happy every day 💖😘🔞🔥",
    "Sweeties, spread the word about this channel and share it with your friends so they can join in on the fresh daily content 😘💖🔞🔥",
    "Hey beautiful people, don’t keep this awesome channel to yourself – share it with friends so they too can enjoy new content daily 💖😘🔞💋",
    "Hi lovely! 💖 Let your friends know about this channel and help them enjoy new content that will brighten their day 😘🔞💥",
    "Sweethearts, make sure your friends know about this channel so they can enjoy fresh content and positive vibes every day 💖😘🔞🔥",
    "Hey, gorgeous! 💋 Share this channel with your friends and help them get in the mood with fresh content every day 😘💖🔞🔥",
    "Share this channel with your loved ones so they too can enjoy the new content that will keep them entertained every day 💖😘🔞💥",
    "Hello beautiful people 💋 Don’t keep this channel to yourself – share it with your friends so they can enjoy daily fun and fresh content 😘🔞🔥",
    "Hey sweetie! 💖 Spread the word about this channel so your friends can enjoy the new content and stay happy every day 😘🔞💋",
    "Hey love 💋 Share this channel with your friends so they can enjoy fresh content and daily good vibes 😘💖🔞💥",
    "Sweeties, share this channel with your friends and let them enjoy a daily dose of fresh content and happiness 😘💖🔞🔥",
    "Hey darlings, share this channel with your friends so they can enjoy new content and improve their mood every day 💖😘🔞💋",
    "Hi there, sweetie 💋 Don’t keep this amazing channel to yourself! Share it with your friends so they can enjoy fresh content daily 😘💖🔞💥",
    "Spread the love, sweeties! 💖 Share this channel with your friends so they too can enjoy new content and keep their spirits up 😘🔞🔥",
    "Hi, lovely! 💋 Let your friends know about this channel and let them join in on the fun with daily fresh content 😘💖🔞💋",
    "Sweethearts, share this channel with your friends so they can enjoy fresh content and stay in a good mood every day 💖😘🔞🔥",
    "Hey gorgeous! 💖 Share this channel with your friends so they can enjoy daily content and feel the good vibes every day 😘🔞💥",
    "Don’t keep this channel to yourself, sweeties 💋 Share it with your friends so they can enjoy new content and feel happy every day 💖😘🔞💋",
    "Hey lovely, share this channel with your friends so they can improve their mood and enjoy fresh content every day 💖😘🔞💥",
    "Share the fun, sweeties! 💋 Tell your friends about this channel so they can enjoy new content and stay happy every day 😘💖🔞🔥",
    "Hey sweethearts 💖 Spread the word about this channel so your friends can enjoy fresh content and improve their mood daily 😘🔞💥",
    "Hello darlings 💋 Don’t keep this channel to yourself! Share it with your friends and let them enjoy new content daily 😘💖🔞💋",
    "Hey love 💖 Share this channel with your friends so they can join in on the daily fun and positive vibes 😘🔞💥",
    "Sweeties, pass this channel along to your friends so they can also enjoy fresh content every day and keep their mood lifted 😘💖🔞🔥",
    "Hey there, share this channel with your friends so they can also enjoy new content and stay positive every day 💖😘🔞💋",
    "Hi gorgeous, share this channel with your friends and let them enjoy new content that will keep them entertained and happy every day 😘💖🔞🔥",
]

link = "https://t.me/+2u9IqLu6Gb43Njli"

texts_with_link = [text + f"\n\n👇👇👇\n\n{link}\n{link}\n{link}" for text in RECOMEND_TEXT]

RECOMEND_MSG = random.choice(texts_with_link)


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


SPAM_MESSAGE = [
    '🔥 EŔOTIC HÛB FOR Ť₲ 🔞\n\n🤩__ϜΙΝD МORE__✨ 👉 @lustsqr',
    '🔥 SÉX CLÚB IN Ť₲ 🔞\n\n🤩__ϜΙΝD ΜΑGİС__✨ 👉 @lustsqr',
    '🔥 PLEÀSÛRE ZØNE HUB IN Ť₲ 🔞\n\n🤩__ϜΙΝD ƳÕÛŘ SPOT__✨ 👉 @lustsqr',
    '🔥 EΧCŁUSIVE PØRN IN TG 🔞\n\n🤩__ϜΙΝD MØRE__✨ 👉 @lustsqr',
    '🔥 TOP SƏX HÛB IN TG 🔞\n\n🤩__ϜΙΝD THE BƏST__✨ 👉 @lustsqr',
    '🔥 HØT PØRNØ HUB IN TG 🔞\n\n🤩__ϜΙΝD YÕÛŘ CLÍÇK__✨ 👉 @lustsqr',
    '🔥 ADULT LÛST HUB IN Ť₲ 🔞\n\n🤩__ϜΙΝD YÕÛR ŤASŤE__✨ 👉 @lustsqr',
    '🔥 BEST 18+ HÛB FOR Ť₲ 🔞\n\n🤩__ϜΙΝD HØŤ SŤÛFF__✨ 👉 @lustsqr',
    '🔥 ADULT SCÈNËS HUB IN TG 🔞\n\n🤩__ϜΙΝD MØRE THRİLL__✨ 👉 @lustsqr',
    '🔥 PØRN VİP ZONE IN Ť₲ 🔞\n\n🤩__ϜΙΝD YØUR BLISS__✨ 👉 @lustsqr',
    '🔥 BΞST ADULT HÛB IN Ť₲ 🔞\n\n🤩__ϜΙΝD SÉXÎNESS__✨ 👉 @lustsqr',
    '🔥 TØP 18+ HÛB FOR TG 🔞\n\n🤩__ϜΙΝD WILD VİBES__✨ 👉 @lustsqr',
    '🔥 PRÉMÎUM PØRN HUB IN TG 🔞\n\n🤩__ϜΙΝD YØUR FAV__✨ 👉 @lustsqr',
    '🔥 RÀW PØRN HUB IN TG 🔞\n\n🤩__ϜΙΝD NØ.1 CHØICE__✨ 👉 @lustsqr',
    '🔥 SÛPERIOR 18+ HUB IN Ť₲ 🔞\n\n🤩__ϜΙΝD EXCÎTEMNT__✨ 👉 @lustsqr',
    '🔥 NØ.1 PØRN ZØNË IN TG 🔞\n\n🤩__ϜΙΝD THË TOP__✨ 👉 @lustsqr',
    '🔥 BEST ADÛLŤ HÛB IN TG 🔞\n\n🤩__ϜΙΝD YOUR FÙN__✨ 👉 @lustsqr',
    '🔥 18+ EXCŁÛSİVÉ HUB IN TG 🔞\n\n🤩__ϜΙΝD ADÛLŤ FUN__✨ 👉 @lustsqr',
    '🔥 PRØ PØRN SCENES HUB IN TG 🔞\n\n🤩__ϜΙΝD YOUR VÎBES__✨ 👉 @lustsqr',
    '🔥 HØTTËST ADULT HUB IN TG 🔞\n\n🤩__ϜΙΝD SPÎCÝ CLÎCK__✨ 👉 @lustsqr',
    '🔥 TØP EROTIC ZØNË IN Ť₲ 🔞\n\n🤩__ϜΙΝD YØUR PASSIØN__✨ 👉 @lustsqr',
    '🔥 NŞFW PØRN HUB IN TG 🔞\n\n🤩__ϜΙΝD THË FÎRE__✨ 👉 @lustsqr',
    '🔥 HØTTÈST CLÎPS IN Ť₲ 🔞\n\n🤩__ϜΙΝD THRÎLL__✨ 👉 @lustsqr',
    '🔥 18+ ŤØP HUB IN Ť₲ 🔞\n\n🤩__ϜΙΝD LÛŚT__✨ 👉 @lustsqr',
    '🔥 SÊXIEST PØRN HUB IN TG 🔞\n\n🤩__ϜΙΝD ÊXCITEMENT__✨ 👉 @lustsqr',
    '🔥 NO.1 PØRN ËXPËRIENCE IN TG 🔞\n\n🤩__ϜΙΝD THË HØTTEST__✨ 👉 @lustsqr',
    '🔥 NÕ.1 HÛB FOR SEX CLIPS IN TG 🔞\n\n🤩__ϜΙΝD WÎLD VIBES__✨ 👉 @lustsqr',
    '🔥 EXCLÛSİVË 18+ CONTENT IN Ť₲ 🔞\n\n🤩__ϜΙΝD FUN__✨ 👉 @lustsqr',
    '🔥 BEST NSFW HÛB IN Ť₲ 🔞\n\n🤩__ϜΙΝD THE MØST__✨ 👉 @lustsqr',
    '🔥 TØP ADULT CLIPS IN TG 🔞\n\n🤩__ϜΙΝD YØUR PLEASURE__✨ 👉 @lustsqr',
    '🔥 SÎZZLING PØRN HUB IN TG 🔞\n\n🤩__ϜΙΝD THË BÉST__✨ 👉 @lustsqr',
    '🔥 A-CLASS PØRN CHANNEL IN TG 🔞\n\n🤩__ϜΙΝD YOUR FAVS__✨ 👉 @lustsqr',
    '🔥 RÊAL ADULT HUB IN TG 🔞\n\n🤩__ϜΙΝD THE PLEASURE__✨ 👉 @lustsqr',
    '🔥 BÎG PØRN CLÎPS IN Ť₲ 🔞\n\n🤩__ϜΙΝD THE SÎZZLE__✨ 👉 @lustsqr',
    '🔥 NO.1 EXCLUSIVE PØRN IN TG 🔞\n\n🤩__ϜΙΝD LÛXÛRY__✨ 👉 @lustsqr',
    '🔥 ELÎTE ADULT HUB IN TG 🔞\n\n🤩__ϜΙΝD HØTTEST CLÎCK__✨ 👉 @lustsqr',
    '🔥 WÎLD PØRN HUB IN TG 🔞\n\n🤩__ϜΙΝD FÛLL FUN__✨ 👉 @lustsqr',
    '🔥 PLEASÛRABLE PØRN HUB IN TG 🔞\n\n🤩__ϜΙΝD THE FANTASY__✨ 👉 @lustsqr',
    '🔥 N°1 ADULT ZØNË IN TG 🔞\n\n🤩__ϜΙΝD FÎRE INSIDE__✨ 👉 @lustsqr',
    '🔥 FÙLL ADÛLŤ HUB IN TG 🔞\n\n🤩__ϜΙΝD YØUR JOY__✨ 👉 @lustsqr'
]
