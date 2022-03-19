from asyncio import sleep

from ..utils import errors_handler
from . import BOTLOG, BOTLOG_CHATID, M


@bot.on(admin_cmd(outgoing=True, pattern="تنظيف$"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="تنظيف$"))
@errors_handler
async def fastpurger(purg):
    # For .purge command, purge all messages starting from the reply.
    chat = await purg.get_input_chat()
    msgs = []
    itermsg = purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id)
    count = 0

    if purg.reply_to_msg_id is not None:
        async for msg in itermsg:
            msgs.append(msg)
            count += 1
            msgs.append(purg.reply_to_msg_id)
            if len(msgs) == 100:
                await purg.client.delete_messages(chat, msgs)
                msgs = []
    else:
        await edit_or_reply(
            purg,
            "**⪼ قم برد على اي رساله وسيتم حذف جميع الرسائل التي تليـها ༗ .**",
        )
        return

    if msgs:
        await purg.client.delete_messages(chat, msgs)
    done = await purg.client.send_message(
        purg.chat_id,
        "**⪼ اكتمل الحذف السريع ❕**\n⪼ حذف " + str(count) + " رساله 𓆰",
    )

    if BOTLOG:
        await purg.client.send_message(
            BOTLOG_CHATID,
            "#التنظيف \n⪼ تم تنظيف " + str(count) + " رساله بنجاح 𓆰",
        )
    await sleep(2)
    await done.delete()

@bot.on(admin_cmd(pattern="حذف رسائلي"))
async def purgeme(event):
    "To purge your latest messages."
    message = event.text
    count = int(message[12:])
    i = 1
    async for message in event.client.iter_messages(event.chat_id, from_user="me"):
        if i > count + 1:
            break
        i += 1
        await message.delete()

    smsg = await event.client.send_message(
        event.chat_id,
        f"**⌔∮ اهلا {M} تم حذف** " + str(count) + " رساله.",
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#حذف_الرسائل \n`تم حذف" + str(count) + " رساله بنجاح.`",
        )
    await sleep(5)
    await smsg.delete()

CMD_HELP.update(
    {
        "التنظيف": "**اسم الاضافـه : **`التنظيف`\
        \n\n**╮•❐ الامـر ⦂ **`.تنظيف` بالـرد على رسالـة البدء المراد المسح من عندها\
        \n**الشـرح •• **__يقـوم بحذف كل الرسائل بدءًا من رسالة الـرد.__\
        \n\n**╮•❐ الامـر ⦂ **`.حذف رسائلي` + عدد\
        \n**الشـرح •• **__حذف عـدد محدد من كميـة رسائلك الاخيـره.__"
    }
)
