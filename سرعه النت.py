# speedtest for safeina edit by @safeina1

from datetime import datetime

import speedtest

from . import reply_id


@bot.on(admin_cmd(pattern="سرعه النت ?(.*)"))
@bot.on(sudo_cmd(pattern="سرعه النت ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    as_text = False
    as_document = False
    if input_str == "صوره":
        as_document = False
    elif input_str == "ملف":
        as_document = True
    elif input_str == "نص":
        as_text = True
    icssevent = await edit_or_reply(event, "** ▷ يتم قياس سرعه الانترنيت ◃**")
    start = datetime.now()
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    client_infos = response.get("client")
    i_s_p = client_infos.get("isp")
    i_s_p_rating = client_infos.get("isprating")
    reply_msg_id = await reply_id(event)
    try:
        response = s.results.share()
        speedtest_image = response
        if as_text:
            await icssevent.edit(
                """**قياس سرعـه النت اكتمـلت في {} ثانيـه**

**التحميـل ⦂** {}
**الرفـع ⦂** {}
**بنـك ⦂** {}
**مزود خدمـة الإنترنت ⦂** {}
**مـعدل ISP ⦂** {}""".format(
                    ms,
                    convert_from_bytes(download_speed),
                    convert_from_bytes(upload_speed),
                    ping_time,
                    i_s_p,
                    i_s_p_rating,
                )
            )
        else:
            await event.client.send_file(
                event.chat_id,
                speedtest_image,
                caption="𓆩 𝑺𝑶𝑼𝑹𝑪𝑬 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢𓆪\n 𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻\n**⪼ اڪتمل اختبار السرعه في ** {} **ثانيه** 𓆰.".format(
                    ms
                ),
                force_document=as_document,
                reply_to=reply_msg_id,
                allow_cache=False,
            )
            await event.delete()
    except Exception as exc:
        await icssevent.edit(
            """**قياس سرعـه النت اكتمـلت في {} ثانيـه**
**التحميـل ⦂** {}
**الرفـع ⦂** {}
**بنـك ⦂** {}

__With the Following ERRORs__
{}""".format(
                ms,
                convert_from_bytes(download_speed),
                convert_from_bytes(upload_speed),
                ping_time,
                str(exc),
            )
        )


def convert_from_bytes(size):
    power = 2 ** 10
    n = 0
    units = {0: "", 1: "kilobytes", 2: "megabytes", 3: "gigabytes", 4: "terabytes"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"


CMD_HELP.update(
    {
        "سرعه النت": """**اسم الاضافـه : **`سرعه النت`

  •  **╮•❐ الامـر ⦂ **`.سرعه النت نص/صوره/ملف`
  •  **الشـرح •• **__يظهر سرعة الخادم الخاص بك بالرفـع والتحميـل المحدد إذا اذا تم كتابة الامر فقط سوف يظهر كصورة__"""
    }
)
