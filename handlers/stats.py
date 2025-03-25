from config.config import CHANNEL_ID, bot
from aiogram.types import Message
from telethon import TelegramClient, functions

from config.config import TGSTAT, CHANNEL_ID


async def channel_stats(message: Message):

    from tgstat_api_client.client import TGStat

    stat = TGStat(token=TGSTAT)
    channel_stat = await stat.get_stat(chat=CHANNEL_ID)

    channel_stat_dict = {
        "id": channel_stat.id,
        "title": channel_stat.title,
        "username": channel_stat.username,
        "participants_count": channel_stat.participants_count,
        "avg_post_reach": channel_stat.avg_post_reach,
        "adv_post_reach_12h": channel_stat.adv_post_reach_12h,
        "adv_post_reach_24h": channel_stat.adv_post_reach_24h,
        "adv_post_reach_48h": channel_stat.adv_post_reach_48h,
        "err_percent": channel_stat.err_percent,
        "err24_percent": channel_stat.err24_percent,
        "er_percent": channel_stat.er_percent,
        "daily_reach": channel_stat.daily_reach,
        "ci_index": channel_stat.ci_index,
        "mentions_count": channel_stat.mentions_count,
        "forwards_count": channel_stat.forwards_count,
        "mentioning_channels_count": channel_stat.mentioning_channels_count,
        "posts_count": channel_stat.posts_count
    }

    stats_text = (
        f"<b>🔸 Название канала:</b> {channel_stat_dict['title']}\n\n"
        f"<b>🔸 Username:</b> {channel_stat_dict['username'] or 'Не указан'}\n"
        f"<b>📊 Количество подписчиков:</b> {channel_stat_dict['participants_count']}\n"
        f"<b>📈 Средний охват поста:</b> {channel_stat_dict['avg_post_reach']}\n"
        f"<b>📊 Рекламный охват (12 ч.):</b> {channel_stat_dict['adv_post_reach_12h']}\n"
        f"<b>📊 Рекламный охват (24 ч.):</b> {channel_stat_dict['adv_post_reach_24h']}\n"
        f"<b>📊 Рекламный охват (48 ч.):</b> {channel_stat_dict['adv_post_reach_48h']}\n"
        f"<b>📉 Процент вовлеченности:</b> {channel_stat_dict['err_percent']}%\n"
        f"<b>📉 Процент вовлеченности (24 ч.):</b> {channel_stat_dict['err24_percent']}%\n"
        f"<b>📊 Коэффициент вовлеченности:</b> {channel_stat_dict['er_percent']}%\n"
        f"<b>🌐 Дневной охват:</b> {channel_stat_dict['daily_reach']}\n"
        f"<b>📰 Индекс цитирования:</b> {channel_stat_dict['ci_index']}\n"
        f"<b>🔄 Количество упоминаний:</b> {channel_stat_dict['mentions_count']}\n"
        f"<b>🔄 Количество репостов:</b> {channel_stat_dict['forwards_count']}\n"
        f"<b>🔁 Канал упоминается в:</b> {channel_stat_dict['mentioning_channels_count']} других каналах\n"
        f"<b>📅 Количество публикаций:</b> {channel_stat_dict['posts_count']}\n"
    )

    await message.answer(stats_text, parse_mode="HTML")