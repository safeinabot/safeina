# for -<*>~ SOURCE 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢~<*>-
# edit By: @S_F_M_L

import asyncio
import os

from . import *


@bot.on(admin_cmd(pattern="تسبام"))
async def safeina(zel):
    tspam = str(zel.text[7:])
    message = tspam.replace(" ", "")
    for letter in message:
        await zel.respond(letter)
    await zel.delete()


@bot.on(admin_cmd(pattern="سبام"))
async def Safeina(zel):
    if not zel.text[0].isalpha() and zel.text[0] not in ("/", "#", "@", "!"):
        message = zel.text
        counter = int(message[6:8])
        spam_message = str(zel.text[8:])
        await asyncio.wait([zel.respond(spam_message) for i in range(counter)])
        await zel.delete()


@bot.on(admin_cmd(pattern="بسبام"))
async def Safeina(zel):
    if not zel.text[0].isalpha() and zel.text[0] not in ("/", "#", "@", "!"):
        message = zel.text
        counter = int(message[9:13])
        spam_message = str(zel.text[13:])
        for i in range(zel, counter):
            await zel.respond(spam_message)
        await zel.delete()


@bot.on(admin_cmd(pattern="بكسبام"))
async def tiny_pic_spam(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        reply = await e.get_reply_message()
        message = e.text
        text = message.split()
        counter = int(text[1])
        media = await e.client.download_media(reply)
        for i in range(1, counter):
            await e.client.send_file(e.chat_id, media)
        os.remove(media)
        await e.delete()


@bot.on(admin_cmd(pattern="تكرار ?(.*)"))
async def delayspammer(e):
    args = e.pattern_match.group(1)
    print(args)

    try:
        args = args.split(" ", 2)
        delay = float(args[0])
        count = int(args[1])
        msg = str(args[2])
    except BaseException:
        return await e.edit(
            f"**- الاستخدام :** {HNDLR}delayspam <delay time> <count> <msg>"
        )

    if not msg[0].isalpha() and msg[0] in ("/", "#", "@", "!"):
        return

    await e.delete()
    try:
        for i in range(count):
            await e.respond(msg)
            await asyncio.sleep(delay)
    except Exception as u:
        await e.respond(f"**Error :** `{u}`")
