#safeina

import asyncio
import os
import re
import time
from datetime import datetime
from pathlib import Path

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

from . import hmention, progress, ytsearch


@bot.on(admin_cmd(pattern="تحميل (ص|ف)(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="تحميل (ص|ف)(?: |$)(.*)", allow_sudo=True))
async def download_video(v_url):
    url = v_url.pattern_match.group(2)
    if not url:
        rmsg = await v_url.get_reply_message()
        myString = rmsg.text
        url = re.search("(?P<url>https?://[^\s]+)", myString).group("url")
    if not url:
        await edit_or_reply(v_url, "**عـليك ادراج رابـط مع الامر اولا ليتـم التحميـل**")
        return
    ytype = v_url.pattern_match.group(1).lower()
    v_url = await edit_or_reply(v_url, "**⌔╎جـارِ التحميل انتظر قليلا ▬▭ ...**")
    reply_to_id = await reply_id(v_url)
    if ytype == "ص":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        video = False
        song = True
    elif ytype == "ف":
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
        song = False
        video = True
    try:
        await v_url.edit("**╮ ❐ يتـم جلـب البيانـات انتظـر قليلاً ...𓅫╰▬▭ **")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await v_url.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await v_url.edit("**- عذرا هذا المحتوى قصير جدا لتنزيله ⚠️**")
        return
    except GeoRestrictedError:
        await v_url.edit(
            "**- الفيديو غير متاح من موقعك الجغرافي بسبب القيود الجغرافية التي يفرضها موقع الويب ❕**"
        )
        return
    except MaxDownloadsReached:
        await v_url.edit("**- تم الوصول إلى الحد الأقصى لعدد التنزيلات ❕**")
        return
    except PostProcessingError:
        await v_url.edit("**كان هناك خطأ أثناء المعالجة**")
        return
    except UnavailableVideoError:
        await v_url.edit("**⌔∮عـذراً .. الوسائط غير متوفـره بالتنسيق المطلـوب**")
        return
    except XAttrMetadataError as XAME:
        await v_url.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await v_url.edit("**حدث خطأ أثناء استخراج المعلومات يرجى وضعها بشكل صحيح ⚠️**")
        return
    except Exception as e:
        await v_url.edit(f"{str(type(e)): {str(e)}}")
        return
    itime = time.time()
    icstb = Path(f"{ytdl_data['id']}.jpg")
    if not os.path.exists(icstb):
        icstb = Path(f"{ytdl_data['id']}.webp")
    if not os.path.exists(icstb):
        icstb = None
    if song:
        await v_url.edit(
            f"**╮ ❐ جـارِ التحضيـر للـرفع انتظـر ...𓅫╰**:\
            \n**{ytdl_data['title']}**\
            \nبـواسطة *{ytdl_data['uploader']}*"
        )
        await v_url.client.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp3",
            supports_streaming=True,
            thumb=icatb,
            reply_to=reply_to_id,
            attributes=[
                DocumentAttributeAudio(
                    duration=int(ytdl_data["duration"]),
                    title=str(ytdl_data["title"]),
                    performer=str(ytdl_data["uploader"]),
                )
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, v_url, itime, "** ⌔╎جاري التحميل ▬▭ ...**", f"{ytdl_data['title']}.mp3")
            ),
        )
        os.remove(f"{ytdl_data['id']}.mp3")
    elif video:
        await v_url.edit(
            f"`Preparing to upload video:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*"
        )
        await v_url.client.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp4",
            reply_to=reply_to_id,
            supports_streaming=True,
            caption=ytdl_data["title"],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, v_url, itime, "** ⌔╎جاري التحميل ▬▭ ...**", f"{ytdl_data['title']}.mp4")
            ),
        )
        os.remove(f"{ytdl_data['id']}.mp4")
    if icstb:
        os.remove(icstb)
    await v_url.delete()


@bot.on(admin_cmd(pattern="يوتيوب(?: |$)(\d*)? ?(.*)", command="يوتيوب"))
@bot.on(sudo_cmd(pattern="يوتيوب(?: |$)(\d*)? ?(.*)", command="يوتيوب", allow_sudo=True))
async def yt_search(event):
    if event.fwd_from:
        return
    if event.is_reply and not event.pattern_match.group(2):
        query = await event.get_reply_message()
        query = str(query.message)
    else:
        query = str(event.pattern_match.group(2))
    if not query:
        return await edit_delete(
            event, "**╮ بالـرد ﮼؏ كلمـٓھہ للبحث أو ضعها مـع الأمـر ... 𓅫╰**"
        )
    video_q = await edit_or_reply(event, "**╮ جـارِ البحث ▬▭... ╰**")
    if event.pattern_match.group(1) != "":
        lim = int(event.pattern_match.group(1))
        if lim <= 0:
            lim = int(10)
    else:
        lim = int(10)
    try:
        full_response = await ytsearch(query, limit=lim)
    except Exception as e:
        return await edit_delete(video_q, str(e), time=10, parse_mode=parse_pre)
    reply_text = f"**•  اليك عزيزي قائمة بروابط الكلمة اللتي بحثت عنها:**\n`{query}`\n\n**•  النتائج:**\n{full_response}"
    await edit_or_reply(video_q, reply_text)



CMD_HELP.update(
    {
        "يوتيوب": "**اسم الاضـافه :** `يوتيوب`\
    \n\n  •  **╮•❐ الامـر ⦂** `.تحميل ص + الرابط`\
    \n  •  **الشـرح •• **__يقوم بتنزيل الصوت من الرابط المحدد (يدعم جميع المواقع التي تدعم youtube-dl)__\
    \n\n  •  **╮•❐ الامـر ⦂ **`.تحميل ف + الرابط`\
    \n  •  **الشـرح •• **__يقوم بتنزيل الفيديو من الرابط المحدد (يدعم جميع المواقع التي تدعم youtube-dl)__\
    \n\n  •  **╮•❐ الامـر ⦂ **`.يوتيوب و كلمه`/`.يوتيوب وعدد وكلمه`\
    \n  •  **الشـرح •• **__يجلب نتائج بحث يوتيوب مع المشاهدات والمدة مع عدد النتائج المطلوبة بشكل افتراضي ، فإنه يجلب 10 نتائج__\
    \n\n  •  **╮•❐ الامـر ⦂ **`.انستا + رابط`\
    \n  •  **الشـرح •• **__يقـوم بتنزيل الفيديـو والاستـوريات من رابط الانسـتكرام المحـدد__\
    "
    }
)
