# file summary plugin for zed  by @S_F_M_L

import time

from prettytable import PrettyTable

from . import humanbytes, media_type

TYPES = [
    "Photo",
    "Audio",
    "Video",
    "Document",
    "Sticker",
    "Gif",
    "Voice",
    "Round Video",
]


def weird_division(n, d):
    return n / d if d else 0


@borg.on(admin_cmd(pattern="احصائيات الكروب ?(.*)", outgoing=True))
@borg.on(sudo_cmd(pattern="احصائيات الكروب ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    entity = event.chat_id
    input_str = event.pattern_match.group(1)
    if input_str:
        try:
            entity = int(input_str)
        except ValueError:
            entity = input_str
    starttime = int(time.monotonic())
    x = PrettyTable()
    totalcount = totalsize = msg_count = 0
    x.title = "ملخص الملفات"
    x.field_names = ["الميديا", "العدد", "حجم الملف"]
    largest = "   <b>حجم الميديا</b>\n"
    try:
        chatdata = await event.client.get_entity(entity)
    except Exception as e:
        return await edit_delete(
            event, f"<b>Error : </b><code>{str(e)}</code>", time=5, parse_mode="HTML"
        )
    if type(chatdata).__name__ == "Channel":
        if chatdata.username:
            link = f"<a href='t.me/{chatdata.username}'>{chatdata.title}</a>"
        else:
            link = chatdata.title
    else:
        link = f"<a href='tg://user?id={chatdata.id}'>{chatdata.first_name}</a>"
    catevent = await edit_or_reply(
        event,
        f"<code>جارِ ... عد الميديا وحجم كل ملف لكروب </code><b>{link}</b>\n<code>قد يستغرق هذا بعض الوقت يعتمد أيضًا على عدد رسائل الكروب</code>",
        parse_mode="HTML",
    )
    media_dict = {
        m: {"file_size": 0, "count": 0, "max_size": 0, "max_file_link": ""}
        for m in TYPES
    }
    async for message in event.client.iter_messages(entity=entity, limit=None):
        msg_count += 1
        media = media_type(message)
        if media is not None:
            media_dict[media]["file_size"] += message.file.size
            media_dict[media]["count"] += 1
            if message.file.size > media_dict[media]["max_size"]:
                media_dict[media]["max_size"] = message.file.size
                if type(chatdata).__name__ == "Channel":
                    media_dict[media][
                        "max_file_link"
                    ] = f"https://t.me/c/{chatdata.id}/{message.id}"  # pylint: disable=line-too-long
                else:
                    media_dict[media][
                        "max_file_link"
                    ] = f"tg://openmessage?user_id={chatdata.id}&message_id={message.id}"  # pylint: disable=line-too-long
            totalsize += message.file.size
            totalcount += 1
    for mediax in TYPES:
        x.add_row(
            [
                mediax,
                media_dict[mediax]["count"],
                humanbytes(media_dict[mediax]["file_size"]),
            ]
        )
        if media_dict[mediax]["count"] != 0:
            largest += f"  •  <b><a href='{media_dict[mediax]['max_file_link']}'>{mediax}</a>  : </b><code>{humanbytes(media_dict[mediax]['max_size'])}</code>\n"
    endtime = int(time.monotonic())
    if endtime - starttime >= 120:
        runtime = str(round(((endtime - starttime) / 60), 2)) + " minutes"
    else:
        runtime = str(endtime - starttime) + " seconds"
    avghubytes = humanbytes(weird_division(totalsize, totalcount))
    avgruntime = (
        str(round((weird_division((endtime - starttime), totalcount)) * 1000, 2))
        + " ms"
    )
    totalstring = f"<code><b>العدد الكلي للملفات : </b>       | {str(totalcount)}\
                  \nحجم الميديا الكلي :    | {humanbytes(totalsize)}\
                  \nمعدل الميديا :     | {avghubytes}\
                  \n</code>"
    runtimestring = f"<code>وقت التشغيل :            | {runtime}\
                    \nوقت التشغيل لكل ملف :   | {avgruntime}\
                    \n</code>"
    line = "<code>+--------------------+-----------+</code>\n"
    result = f"<b>كروب : {link}</b>\n\n"
    result += f"<code>عدد الرسائل الكلي: {msg_count}</code>\n"
    result += "<b>ملخص الملفات : </b>\n"
    result += f"<code>{str(x)}</code>\n"
    result += f"{largest}"
    result += line + totalstring + line + runtimestring + line
    await catevent.edit(result, parse_mode="HTML", link_preview=False)


@borg.on(admin_cmd(pattern="احصائيات العضو ?(.*)", outgoing=True))
@borg.on(sudo_cmd(pattern="احصائيات العضو ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    reply = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    if reply and input_str:
        try:
            entity = int(input_str)
        except ValueError:
            entity = input_str
        userentity = reply.sender_id
    elif reply:
        entity = event.chat_id
        userentity = reply.sender_id
    elif input_str:
        entity = event.chat_id
        try:
            userentity = int(input_str)
        except ValueError:
            userentity = input_str
    else:
        entity = event.chat_id
        userentity = event.sender_id
    starttime = int(time.monotonic())
    x = PrettyTable()
    totalcount = totalsize = msg_count = 0
    x.title = "ملخص الملفات"
    x.field_names = ["الميديا", "العدد", "حجم الملف"]
    largest = "   <b>Largest Size</b>\n"
    try:
        chatdata = await event.client.get_entity(entity)
    except Exception as e:
        return await edit_delete(
            event, f"<b>Error : </b><code>{str(e)}</code>", 5, parse_mode="HTML"
        )
    try:
        userdata = await event.client.get_entity(userentity)
    except Exception as e:
        return await edit_delete(
            event, f"<b>Error : </b><code>{str(e)}</code>", time=5, parse_mode="HTML"
        )
    if type(chatdata).__name__ == "Channel":
        if chatdata.username:
            link = f"<a href='t.me/{chatdata.username}'>{chatdata.title}</a>"
        else:
            link = chatdata.title
    else:
        link = f"<a href='tg://user?id={chatdata.id}'>{chatdata.first_name}</a>"
    catevent = await edit_or_reply(
        event,
        f"<code>جارِ ... عد الملفات وحجم كل ملف بواسطة </code>{_format.htmlmentionuser(userdata.first_name,userdata.id)}<code> في كروب </code><b>{link}</b>\n<code>قد يستغرق هذا بعض الوقت يعتمد ايضا على عدد رسائل هذا العضو في الكروب</code>",
        parse_mode="HTML",
    )

    media_dict = {
        m: {"file_size": 0, "count": 0, "max_size": 0, "max_file_link": ""}
        for m in TYPES
    }
    async for message in event.client.iter_messages(
        entity=entity, limit=None, from_user=userentity
    ):
        msg_count += 1
        media = media_type(message)
        if media is not None:
            media_dict[media]["file_size"] += message.file.size
            media_dict[media]["count"] += 1
            if message.file.size > media_dict[media]["max_size"]:
                media_dict[media]["max_size"] = message.file.size
                if type(chatdata).__name__ == "Channel":
                    media_dict[media][
                        "max_file_link"
                    ] = f"https://t.me/c/{chatdata.id}/{message.id}"
                else:
                    media_dict[media][
                        "max_file_link"
                    ] = f"tg://openmessage?user_id={chatdata.id}&message_id={message.id}"
            totalsize += message.file.size
            totalcount += 1
    for mediax in TYPES:
        x.add_row(
            [
                mediax,
                media_dict[mediax]["count"],
                humanbytes(media_dict[mediax]["file_size"]),
            ]
        )
        if media_dict[mediax]["count"] != 0:
            largest += f"  •  <b><a href='{media_dict[mediax]['max_file_link']}'>{mediax}</a>  : </b><code>{humanbytes(media_dict[mediax]['max_size'])}</code>\n"
    endtime = int(time.monotonic())
    if endtime - starttime >= 120:
        runtime = str(round(((endtime - starttime) / 60), 2)) + " minutes"
    else:
        runtime = str(endtime - starttime) + " seconds"
    avghubytes = humanbytes(weird_division(totalsize, totalcount))
    avgruntime = (
        str(round((weird_division((endtime - starttime), totalcount)) * 1000, 2))
        + " ms"
    )
    totalstring = f"<code><b>العدد الكلي للملفات : </b>       | {str(totalcount)}\
                  \nحجم الميديا الكلي :    | {humanbytes(totalsize)}\
                  \nمعدل الميديا :     | {avghubytes}\
                  \n</code>"
    runtimestring = f"<code>وقت التشغيل :            | {runtime}\
                    \nوقت التشغيل لكل ملف :   | {avgruntime}\
                    \n</code>"
    line = "<code>+--------------------+-----------+</code>\n"
    result = f"<b>كروب : {link}\nالعضو : {_format.htmlmentionuser(userdata.first_name,userdata.id)}\n\n"
    result += f"<code>عدد الرسائل الكلي: {msg_count}</code>\n"
    result += "<b>ملخص الملفات : </b>\n"
    result += f"<code>{str(x)}</code>\n"
    result += f"{largest}"
    result += line + totalstring + line + runtimestring + line
    await catevent.edit(result, parse_mode="HTML", link_preview=False)


CMD_HELP.update(
    {
        "الملفات": """**Plugin : **`الملفات`

**Syntax : **
  •  `.احصائيات الكروب`
  •  `.احصائيات الكروب username/id`
**Function : **
  •  __Shows you the complete media/file summary of the that group__

**Syntax : **
  •  `.احصائيات العضو reply`
  •  `.احصائيات العضو chat username/id`
  •  `.احصائيات العضو user username/id`
**Function : **
  •  __Shows you the complete media/file summary of the that User in the group where you want__
"""
    }
)
