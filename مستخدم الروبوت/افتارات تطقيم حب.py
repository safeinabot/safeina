#𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢


from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot.utils import sudo_cmd

from . import reply_id


@bot.on(admin_cmd(pattern="ح$", outgoing=True))
@bot.on(sudo_cmd(pattern="ح$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    if not reply_message:
        await edit_or_reply(event, "**╮ .قـم بالـرد علـى الـرقمـٓہ من 57 - 1 مثـال .ح بالـرد ع رقـم ...𓅫╰**")
        return
    if not reply_message.text:
        await edit_or_reply(event, "**╮ .قـم بالـرد علـى الـرقمـٓہ من 57 - 1 مثـال .ح بالـرد ع رقـم ...𓅫╰**")
        return
    chat = "@Safeina1bot"
    catevent = await edit_or_reply(event, "**╮•⎚ جـارِ التحميل ... 🧸🎈**")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=5249229463)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit(
                "**╮•⎚ تحـقق من انـك لم تقـم بحظر البوت @Safeina1bot .. ثم اعـد استخدام الامـر ...🤖♥️**"
            )
            return
        if response.text.startswith(""):
            await catevent.edit("**🤨💔...؟**")
        else:
            await catevent.delete()
            await event.client.send_message(event.chat_id, response.message)


CMD_HELP.update(
    {
        "افتارات تطقيم حب": "**اسم الاضافـه : **`افتارات تطقيم حب`\
    \n\n**╮•❐ الامـر ⦂ **`.ح` بالـرد علـى رقـم من 1 الى 57 \
    \n**الشـرح •• **تحميل افتـارات تطقيـم حـب تمبلـر ممطـروقـه"
    }
)
