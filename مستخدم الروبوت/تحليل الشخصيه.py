#safeina1

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError


@bot.on(admin_cmd(pattern="التحليل(.*)"))
@bot.on(sudo_cmd(pattern="التحليل(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_or_reply(event, "Reply to any user's media message.")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_or_reply(event, "**بالرد على صوره او ميديا**")
        return
    chat = "@Rekognition_Bot"
    if reply_message.sender.bot:
        await event.edit("Reply to actual users message.")
        return
    cat = await edit_or_reply(event, "**بالرد على صوره او ميديا**")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=461083923)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await cat.edit("unblock @Rekognition_Bot and try again")
            return
        if response.text.startswith("See next message."):
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=461083923)
            )
            response = await response
            msg = response.message.message
            await cat.edit(msg)
        else:
            await cat.edit("sorry, I couldnt find it")

        await event.client.send_read_acknowledge(conv.chat_id)


CMD_HELP.update(
    {
        "تحليل الشخصيه": "**اسم الاضافـه : **`تحليل الشخصيه`\
        \n\n**╮•❐ الامـر ⦂ **`.التحليل بالرد على الصورة او الميديا`\
        \n**الشـرح •• **__احصل على معلومات تحليل شخصية حول صورة باستخدام AWS Rekognition. \
    \ n اكتشف المعلومات بما في ذلك التسميات المكتشفة والوجوه والعمر والجنس. علامات النص والاعتدال__"
    }
)
