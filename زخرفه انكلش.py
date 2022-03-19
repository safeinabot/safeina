#𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot.utils import sudo_cmd

from . import reply_id


@bot.on(admin_cmd(pattern="زغرفه ?(.*)"))
@bot.on(sudo_cmd(pattern="زغرفه ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    chat = "@Safeina1bot"
    catevent = await edit_or_reply(event, "**جـارِ الزغـرفـه💞🧸...**")
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
            await catevent.edit("sorry i can't find it")
        else:
            await catevent.delete()
            await event.client.send_message(event.chat_id, response.message)

@bot.on(admin_cmd(pattern="زغرفه$", outgoing=True))
@bot.on(sudo_cmd(pattern="زغرفه$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    if not reply_message:
        await edit_or_reply(event, "**باضافـة الكلمـة المراد زغرفتها للأمـر .. مثال : .زغرفه + كلمـه 💞🧸.**")
        return
    if not reply_message.text:
        await edit_or_reply(event, "**باضافـة الكلمـة المراد زغرفتها للأمـر .. مثال : .زغرفه + كلمـه 💞🧸.**")
        return
    chat = "@Safeina1bot"
    catevent = await edit_or_reply(event, "**باضافـة الكلمـة المراد زغرفتها للأمـر .. مثال : .زغرفه + كلمـه 💞🧸.**")
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
        "زخرفه انكلش": "`.زغرفه` + كلمه او بالـرد ع كلـمه :\
      \n**الشـرح ••** زغـارف انكـلش تمبلـر مامطروقـه ولأول مـره ع تليـثون أمر يزغرف عدة زغـارف انكـلش بوقت واحد .. الملف حقوق زدثــون#.. . "
    }
)
