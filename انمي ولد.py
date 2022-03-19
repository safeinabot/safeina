#𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot.utils import sudo_cmd

from . import reply_id


@bot.on(admin_cmd(pattern="ولد ?(.*)"))
@bot.on(sudo_cmd(pattern="ولد ?(.*)", allow_sudo=True))
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
            event, "**╮ . اكثـر مـن 1000 افتـارات انمـي شبـاب ممطـروقـه.. ارسـل .ولد انمي 𓅫╰**"
        )
    chat = "@Safeina1bot"
    catevent = await edit_or_reply(event, "**╮•⎚ جـارِ تحميـل الافتـار ...**")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=5249229463)
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



import os
from faker import Faker
import datetime
from telethon import functions, types, events
from telethon.tl.functions.messages import DeleteHistoryRequest
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest

from ..utils import admin_cmd, sudo_cmd


@bot.on(admin_cmd("فيزا$"))
@bot.on(sudo_cmd("فيزا$", allow_sudo=True))
async def _(safeinaDevent):
    if safeinaDevent.fwd_from:
        return
    safeinaDcc = Faker()
    safeinaDname = safeinaDcc.name()
    safeinaDadre = safeinaDcc.address()
    safeinaDcard = safeinaDcc.credit_card_full()
    
    await edit_or_reply(safeinaDevent, f"𓆰 𝙎𝙊𝙐𝙍𝘾𝞝 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢- 𝙑𝙄𝙎𝘼_𝘾𝘼𝙍𝘿  💳𓆪\n\n\n__**👤 الاسـم :- **__\n ٴ──┄──┄──┄──┄──\n`{safeina Dname}`\n\n__**🏡 العنـوان :- **__\n ٴ──┄──┄──┄──┄──\n`{Safeina Dadre}`\n\n__**💸 الفيـزا :- **__\n ٴ──┄──┄──┄──┄──\n`{safeina Dcard}`\n\n◟𝙎𝙤𝙪𝙧𝙘𝙚 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢➧ @safeina1◞ ")
    


CMD_HELP.update(
    {
        "انمي شباب": "**اسم الاضافـه : **`انمي شباب`\
    \n\n**╮•❐ الامـر ⦂ **`.ولد انمي`  \
    \n**الشـرح •• **اكثـر مـن 1000 افتـارات انمـي شبـاب ممطـروقـه .. ارسـل .ولد انمي"
    }
)
