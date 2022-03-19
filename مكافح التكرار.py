#safeina

import asyncio
import base64
from datetime import datetime

from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights

import userbot.plugins.sql_helper.antiflood_sql as sql

from .sql_helper import mute_sql as mute_sql

NO_ADMIN = "⪼ **أنا لست مشرف هنا!!** 𓆰."
NO_PERM = "⪼ **ليس لدي أذونات كافية!** 𓆰."

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)
CHAT_FLOOD = sql.__load_flood_settings()
# warn mode for anti flood
ANTI_FLOOD_WARN_MODE = ChatBannedRights(
    until_date=None, view_messages=None, send_messages=True
)


@bot.on(admin_cmd(incoming=True))
async def _(event):
    if not CHAT_FLOOD:
        return
    if str(event.chat_id) not in CHAT_FLOOD:
        return
    should_ban = sql.update_flood(event.chat_id, event.message.sender_id)
    if not should_ban:
        return
    try:
        await event.client(
            EditBannedRequest(
                event.chat_id, event.message.sender_id, ANTI_FLOOD_WARN_MODE
            )
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        no_admin_privilege_message = await event.client.send_message(
            entity=event.chat_id,
            message="""** مكافـح السبام التلقائـي**@admin [User](tg://user?id={}) **يقوم بالتكرار ويزعج الاعضاء**`{}`""".format(
                event.message.sender_id, str(e)
            ),
            reply_to=event.message.id,
        )
        await asyncio.sleep(10)
        await no_admin_privilege_message.edit(
            "**⚠ توقف عن التكرار والا سيتم تقييدك تلقائياً...** ", link_preview=False
        )
    else:
        try:
            mute(userid, "gmute")
        except Exception as e:
            await event.client.send_message(
                 entity=event.chat_id,
                 message="""** - ❝ ⌊⚠**[هـذا الشخـص](tg://user?id={}) ** تم تقييده تلقائيـاً لأنـه وصل إلى حد التكـرار المحـدد ...𓆰 **""".format(
                     event.message.sender_id
                 ),
                 reply_to=event.message.id,
             )

@bot.on(admin_cmd(pattern="ضع التكرار(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="ضع التكرار(?: |$)(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    event = await edit_or_reply(event, "**جـارِ تحديث حد التكـرار...**")
    try:
        sql.set_flood(event.chat_id, input_str)
        sql.__load_flood_settings()
        await event.edit(
            "**تم وضـع حد التكـرار الى {} في هذه الدردشه...**".format(input_str)
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))


CMD_HELP.update(
    {
        "مكافح التكرار": ".ضع التكرار + عدد\
\nUsage: لتقييد الشخص تلقائيا بعد تحذيره ... \
"
    }
)
