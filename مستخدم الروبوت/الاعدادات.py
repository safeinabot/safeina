#safeina1

import asyncio
import io
import os
from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE

if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)


@bot.on(admin_cmd(outgoing=True, pattern="pips (.*)"))
@bot.on(sudo_cmd(pattern="pips (.*)", allow_sudo=True))
async def pipcheck(pip):
    pipmodule = pip.pattern_match.group(1)
    reply_to_id = pip.message.id
    if pip.reply_to_msg_id:
        reply_to_id = pip.reply_to_msg_id
    if pipmodule:
        pip = await edit_or_reply(pip, "`Searching . . .`")
        pipc = await asyncrunapp(
            "pip3",
            "search",
            pipmodule,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await pipc.communicate()
        pipout = str(stdout.decode().strip()) + str(stderr.decode().strip())
        if pipout:
            if len(pipout) > 4096:
                await pip.edit("`Output too large, sending as file`")
                with open("pips.txt", "w+") as file:
                    file.write(pipout)
                await pip.client.send_file(
                    pip.chat_id,
                    "pips.txt",
                    reply_to=reply_to_id,
                    caption=pipmodule,
                )
                os.remove("output.txt")
                return
            await pip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`"
                f"{pipout}"
                "`"
            )
        else:
            await pip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`No Result Returned/False`"
            )


@bot.on(admin_cmd(pattern="فرمته$"))
@bot.on(sudo_cmd(pattern="فرمته$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    cmd = "rm -rf *"
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    stdout.decode()
    OUTPUT = f"**اعـادة تهيئــة البـوت:**\n\n**تـم حذف جميـع المجـلدات والملفـات بنجـاح✅**"
    event = await edit_or_reply(event, OUTPUT)


@bot.on(admin_cmd(pattern="الاضافات$"))
@bot.on(sudo_cmd(pattern="الاضافات$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    cmd = "ls userbot/plugins"
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        eply_to_id = event.reply_to_msg_id
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"**⌔∮ [𝗦𝗢𝗨𝗥𝗖𝗘 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢](tg://need_update_for_some_feature/) الالاضافات:**\n{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id,
            )
            await event.delete()
    else:
        event = await edit_or_reply(event, OUTPUT)


@bot.on(admin_cmd(pattern="تاريخ$"))
@bot.on(sudo_cmd(pattern="تاريخ$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    #    dirname = event.pattern_match.group(1)
    #    tempdir = "localdir"
    cmd = "date"
    #    if dirname == tempdir:
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        eply_to_id = event.reply_to_msg_id
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id,
            )
            await event.delete()
    else:
        event = await edit_or_reply(event, OUTPUT)


@bot.on(admin_cmd(pattern="الفارات$"))
async def _(event):
    if event.fwd_from:
        return
    cmd = "env"
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        eply_to_id = event.reply_to_msg_id

    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = (
        f"**[𝗦𝗢𝗨𝗥𝗖𝗘 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢](tg://need_update_for_some_feature/) Environment Module:**\n\n\n{o}"
    )
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id,
            )
            await event.delete()
    else:
        event = await edit_or_reply(event, OUTPUT)


@bot.on(admin_cmd(pattern="السرعه$"))
@bot.on(sudo_cmd(pattern="السرعه$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("جارِ حساب السرعة...")
    if event.fwd_from:
        return
    #    dirname = event.pattern_match.group(1)
    #    tempdir = "localdir"
    cmd = "speedtest-cli"
    #    if dirname == tempdir:
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        eply_to_id = event.reply_to_msg_id
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    OUTPUT = f"**[𝗦𝗢𝗨𝗥𝗖𝗘 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢](tg://need_update_for_some_feature/) , تم حساب سرعة السيرفر:**\n{o}"
    if len(OUTPUT) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "env.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=eply_to_id,
            )
            await event.delete()
    else:
        event = await edit_or_reply(event, OUTPUT)


CMD_HELP.update(
    {
        "الاعدادات": "**اسم الاضافـه : **`الاعدادات`\
    \n\n**╮•❐ الامـر ⦂** `.pips query`\
    \n**الشـرح •• **Searches your pip modules\
    \n\n**╮•❐ الامـر ⦂ **`.فرمته`\
    \n**الشـرح •• **لــ حذف كل ملفات ومجلدات بوتـك\
    \n\n**╮•❐ الامـر ⦂ **`.الاضافات`\
    \n**الشـرح •• **يعرض لك قائمة الالاضافات الموجودة في البوت\
    \n\n**╮•❐ الامـر ⦂ **`.تاريخ`\
    \n**الشـرح •• **يعرض لك التاريخ باليوم\
    \n\n**╮•❐ الامـر ⦂ **`.الفارات`\
    \n**الشـرح •• **لعـرض قائمـه بكل الفارات في حسـابك على هيروكـو\
    \n\n**╮•❐ الامـر ⦂ **`.السرعه`\
    \n**الشـرح •• **لــ حساب السرعــه\
    "
    }
)
