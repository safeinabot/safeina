#𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢


import os
from faker import Faker
import datetime
from telethon import functions, types, events
from telethon.tl.functions.messages import DeleteHistoryRequest
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest

from ..utils import admin_cmd, sudo_cmd

from . import reply_id


@bot.on(admin_cmd(pattern="كاشف ?(.*)"))
@bot.on(sudo_cmd(pattern="كاشف ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    if event.reply_to_msg_id and not event.pattern_match.group(1):
        reply_to_id = await event.get_reply_message()
        reply_to_id = str(reply_to_id.message)
    else:
        reply_to_id = str(event.pattern_match.group(1))
    if not reply_to_id:
        return await edit_or_reply(
            event, "**╮ . كـاشف الاࢪقـام الـ؏ـࢪبيـة 📲.. ارࢪسـل .م34 للتعليـمات 𓅫╰**"
        )
    chat = "@Safeina1bot"
    catevent = await edit_or_reply(event, "**╮•⎚ جـارِي الكـشف ؏ــن الـرقـم  📲⌭...**")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1194140165)
            )
            await event.client.send_message(chat, "{}".format(input_str))
            response = await response
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("**╮•⎚ تحـقق من انـك لم تقـم بحظر البوت @Safeina1bot .. ثم اعـد استخدام الامـر ...🤖♥️**")
            return
        if response.text.startswith("I can't find that"):
            await catevent.edit("**╮•⎚ عـذراً .. لـم استطـع ايجـاد المطلـوب ☹️💔**")
        else:
            await catevent.delete()
            await event.client.send_message(event.chat_id, response.message)



CMD_HELP.update(
    {
        "الكاشف": "**اسم الاضافـه : **`الكاشف`\
    \n\n**╮•❐ الامـر ⦂ **`.كاشف`  \
    \n**الشـرح •• **كـاشف الارقـام العـربيـة 📲 .. الوحيـد ع تيليجـرام .. ارسـل .كاشف"
    }
)
