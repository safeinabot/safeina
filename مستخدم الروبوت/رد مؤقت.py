#safeina1

from asyncio import sleep


@bot.on(admin_cmd(pattern="رد (\d*) (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="رد (\d*) (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    sm= ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = sm[1]
    ttl = int(sm[0])
    try:
        await event.delete()
    except Exception as e:
        LOGS.info(str(e))
    await sleep(ttl)
    await event.respond(message)


CMD_HELP.update(
    {
        "رد مؤقت": "**اسم الاضافـه : **`رد مؤقت`\
    \n\n**╮•❐ الامـر ⦂ **`.رد + الوقـت بالثوانـي + الرسالـه`\
    \n**الشـرح •• **أرسل لك الرسالة المحددة بعد ذلك الوقت المحدد\
    "
    }
)
