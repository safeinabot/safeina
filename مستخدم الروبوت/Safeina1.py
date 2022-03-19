#𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢

import re
import random
from userbot import bot
import asyncio
import os
import json
from pathlib import Path
from ..helpers.functions import yt_search
from telethon.errors.rpcerrorlist import YouBlockedUserError


IF_EMOJI = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats 
    "]+")

def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(IF_EMOJI, '', inputString)


@bot.on(admin_cmd(pattern="اغنيه ?(.*)"))

async def nope(doit):
    ok = doit.pattern_match.group(1)
    if not ok:
        if doit.is_reply:
            what = (await doit.get_reply_message()).message
        else:
            await doit.edit("`Sir please give some query to search and download it for you..!`")
            return
    sticcers = await bot.inline_query(
        "LyBot", f"{(deEmojify(ok))}")
    await sticcers[0].click(doit.chat_id,
                            reply_to=doit.reply_to_msg_id,
                            silent=True if doit.is_reply else False,
                            hide_via=True)
    await doit.delete()



SEARCH_STRING = "**╮ جـارِ البحث ؏ـن الفيديـو 🎬♥️╰**"
NOT_FOUND_STRING = "<code>Sorry !I am unable to find any results to your query</code>"
SENDING_STRING = "**╮ ❐ جـارِ تحميـل الفيديـو انتظـر قليلاً  ▬▭... 𓅫╰**"
BOT_BLOCKED_STRING = "**❈╎تحـقق من انـك لم تقـم بحظـر البوت @utubebot .. ثم اعـد استخدام الامـر ...🤖♥️**"

@bot.on(admin_cmd(pattern="تحميل ف ?(.*)"))
async def fetcher(event):
    if event.fwd_from:
        return
    song = event.pattern_match.group(1)
    chat = "@utubebot"
    event = await edit_or_reply(event, SEARCH_STRING, parse_mode="html")
    async with event.client.conversation(chat) as conv:
        try:
            purgeflag = await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(song)
            ok = await conv.get_response()
            while ok.edit_hide != True:
                await asyncio.sleep(0.1)
                ok = await event.client.get_messages(chat, ids=ok.id)
            baka = await event.client.get_messages(chat)
            if baka[0].message.startswith(
                ("**عـذراً .. لـم اجـد شـيئ**")
            ):
                await delete_messages(event, chat, purgeflag)
                return await edit_delete(
                    event, NOT_FOUND_STRING, parse_mode="html", time=5
                )
            await event.edit(SENDING_STRING, parse_mode="html")
            await baka[0].click(0)
            music = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.edit(BOT_BLOCKED_STRING, parse_mode="html")
            return
        await event.client.send_file(
            event.chat_id,
            music,
            caption=f"<b>==> <code>{song}</code></b>",
            parse_mode="html",
        )
        await event.delete()
        await delete_messages(event, chat, purgeflag)


from . import *


