#safeina ®

import asyncio
import time
import io
import os
import shutil
import zipfile
import base64
from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from datetime import datetime
from asyncio import sleep
from asyncio.exceptions import TimeoutError
from telethon import functions, types
from telethon import events
from telethon.tl import functions
from telethon.tl.functions.channels import EditBannedRequest, GetFullChannelRequest, GetParticipantsRequest, EditAdminRequest, EditPhotoRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import GetFullChatRequest, GetHistoryRequest, ExportChatInviteRequest
from telethon.errors import ChannelInvalidError, ChannelPrivateError, ChannelPublicGroupNaError, BadRequestError, ChatAdminRequiredError, FloodWaitError, MessageNotModifiedError, UserAdminInvalidError
from telethon.errors.rpcerrorlist import YouBlockedUserError, UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc
from telethon.errors import ImageProcessFailedError, PhotoCropSizeSmallError
from telethon.tl.types import ChatAdminRights, InputChatPhotoEmpty, MessageMediaPhoto
from telethon.tl.types import ChannelParticipantsKicked, ChannelParticipantAdmin, ChatBannedRights, ChannelParticipantCreator, ChannelParticipantsAdmins, ChannelParticipantsBots, MessageActionChannelMigrateFrom, UserStatusEmpty, UserStatusLastMonth, UserStatusLastWeek, UserStatusOffline, UserStatusOnline, UserStatusRecently
from telethon.utils import get_display_name, get_input_location, get_extension
from os import remove
from math import sqrt
from prettytable import PrettyTable
from emoji import emojize
from pathlib import Path
from userbot.utils import admin_cmd, sudo_cmd
from . import humanbytes
from . import BOTLOG, BOTLOG_CHATID, admin_groups, get_user_from_event
from ..helpers import reply_id
from ..helpers.utils import _format, get_user_from_event, reply_id
from ..helpers import media_type
from ..helpers.google_image_download import googleimagesdownload
from ..helpers.tools import media_type
from .sql_helper.locks_sql import get_locks, is_locked, update_lock
from ..utils import is_admin
from . import progress
from .sql_helper import gban_sql_helper as gban_sql
from .sql_helper.mute_sql import is_muted, mute, unmute
from .sql_helper import no_log_pms_sql
from .sql_helper.globals import addgvar, gvarstatus
BANNED_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)
ZELZAL_RIGHTS = ChatBannedRights(until_date=None, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True, send_games=True, send_inline=True, embed_links=True)
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
plugin_category = "utils"

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
thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")

async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call))
    return xx.call

def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]

def zipdir(dirName):
    filePaths = []
    for root, directories, files in os.walk(dirName):
        for filename in files:
            filePath = os.path.join(root, filename)
            filePaths.append(filePath)
    return filePaths

class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0
LOG_CHATS_ = LOG_CHATS()

PP_TOO_SMOL = "**❈╎الصورة صغيرة جدًا  📸** ."
PP_ERROR = "**❈╎فشل أثناء معالجة الصورة  📵** ."
NO_ADMIN = "**❈╎أنا لست مشرف هنا ** ."
NO_PERM = "**❈╎ليس لدي أذونات كافية  🚮** ."
CHAT_PP_CHANGED = "**❈╎تغيّرت صورة الدردشة  🌅** ."
INVALID_MEDIA = "**⌔ ╎ ملحق غير صالح  📳** ."
IMOGE_ZEDTHON = "❈╎"



@bot.on(admin_cmd(pattern=r"الاعضاء(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"الاعضاء ?(.*)", allow_sudo=True))
async def get_users(show):
    mentions = "**مستخدمين هذه المجموعة**: \n"
    await reply_id(show)
    input_str = show.pattern_match.group(1)
    if input_str:
        mentions = "𓆩 𝑺𝑶𝑼𝑹𝑪𝑬 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢 𓆪\n**❈╎الأعضاء في {} من المجموعات 𓎤:**\n".format(input_str)
        try:
            chat = await show.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(show, f"`{str(e)}`", 10)
    else:
        if not show.is_group:
            return await edit_or_reply(show, "**❈╎هـذه ليسـت مجموعـة ✕**")
    catevent = await edit_or_reply(show, "**❈╎جـاري سحـب قائمـة معرّفـات الأعضـاء 🝛**")
    try:
        if show.pattern_match.group(1):
            async for user in show.client.iter_participants(chat.id):
                if user.deleted:
                    mentions += f"\n**❈╎الحسـابات المحذوفـة ⌦** `{user.id}`"
                else:
                    mentions += (f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`")
        else:
            async for user in show.client.iter_participants(show.chat_id):
                if user.deleted:
                    mentions += f"\n**❈╎الحسـابات المحذوفـة ⌦** `{user.id}`"
                else:
                    mentions += (f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`")
    except Exception as e:
        mentions += " " + str(e) + "\n"
    await edit_or_reply(catevent, mentions)

@bot.on(admin_cmd(pattern=r"معلومات(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern=r"معلومات(?: |$)(.*)", allow_sudo=True))
async def info(event):
    catevent = await edit_or_reply(event, "**❈╎يتـمّ جلـب معلومـات الدردشـة، إنتظـر ⅏**")
    chat = await get_chatinfo(event, catevent)
    caption = await fetch_info(chat, event)
    try:
        await catevent.edit(caption, parse_mode="html")
    except Exception as e:
        if BOTLOG:
            await event.client.send_message(BOTLOG_CHATID, f"**❈╎هنـاك خطـأ في معلومـات الدردشـة ✕ : **\n`{str(e)}`")
        await catevent.edit("**❈╎حـدث خـطأ مـا، يرجـى التحقق من الأمـر ⎌**")
async def get_chatinfo(event, catevent):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except BaseException:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await catevent.edit("**❈╎لـم يتـمّ العثـور على القنـاة/المجموعـة ✕**")
            return None
        except ChannelPrivateError:
            await catevent.edit(
                '**❈╎هـذه مجموعـة أو قنـاة خاصـة أو لقد تمّ حظـري منه ⛞**'
            )
            return None
        except ChannelPublicGroupNaError:
            await catevent.edit("**❈╎القنـاة أو المجموعـة الخارقـة غيـر موجـودة ✕**")
            return None
        except (TypeError, ValueError) as err:
            await catevent.edit(str(err))
            return None
    return chat_info

async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("**❈╎لم يتم العثور على المجموعة او القناة**")
            return None
        except ChannelPrivateError:
            await event.reply(
                "**❈╎لا يمكنني استخدام الامر من الكروبات او القنوات الخاصة**"
            )
            return None
        except ChannelPublicGroupNaError:
            await event.reply("**❈╎لم يتم العثور على المجموعة او القناة**")
            return None
        except (TypeError, ValueError):
            await event.reply("**❈╎رابط الكروب غير صحيح**")
            return None
    return chat_info


def make_mention(user):
    if user.username:
        return f"@{user.username}"
    else:
        return inline_mention(user)


def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    full_name = " ".join(names)
    return full_name


async def fetch_info(chat, event):  # sourcery no-metrics
    # chat.chats is a list so we use get_entity() to avoid IndexError
    chat_obj_info = await event.client.get_entity(chat.full_chat.id)
    broadcast = (
        chat_obj_info.broadcast if hasattr(chat_obj_info, "broadcast") else False
    )
    chat_type = "Channel" if broadcast else "Group"
    chat_title = chat_obj_info.title
    warn_emoji = emojize(":warning:")
    try:
        msg_info = await event.client(
            GetHistoryRequest(
                peer=chat_obj_info.id,
                offset_id=0,
                offset_date=datetime(2010, 1, 1),
                add_offset=-1,
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
    except Exception as e:
        msg_info = None
        print("Exception:", e)
    # No chance for IndexError as it checks for msg_info.messages first
    first_msg_valid = (
        True
        if msg_info and msg_info.messages and msg_info.messages[0].id == 1
        else False
    )

    
    creator_valid = bool(first_msg_valid and msg_info.users)
    creator_id = msg_info.users[0].id if creator_valid else None
    creator_firstname = (
        msg_info.users[0].first_name
        if creator_valid and msg_info.users[0].first_name is not None
        else "Deleted Account"
    )
    creator_username = (
        msg_info.users[0].username
        if creator_valid and msg_info.users[0].username is not None
        else None
    )
    created = msg_info.messages[0].date if first_msg_valid else None
    former_title = (
        msg_info.messages[0].action.title
        if first_msg_valid
        and isinstance(msg_info.messages[0].action, MessageActionChannelMigrateFrom)
        and msg_info.messages[0].action.title != chat_title
        else None
    )
    try:
        dc_id, location = get_input_location(chat.full_chat.chat_photo)
    except Exception:
        dc_id = "Unknown"

    # this is some spaghetti I need to change
    description = chat.full_chat.about
    members = (
        chat.full_chat.participants_count
        if hasattr(chat.full_chat, "participants_count")
        else chat_obj_info.participants_count
    )
    admins = (
        chat.full_chat.admins_count if hasattr(chat.full_chat, "admins_count") else None
    )
    banned_users = (
        chat.full_chat.kicked_count if hasattr(chat.full_chat, "kicked_count") else None
    )
    restrcited_users = (
        chat.full_chat.banned_count if hasattr(chat.full_chat, "banned_count") else None
    )
    members_online = (
        chat.full_chat.online_count if hasattr(chat.full_chat, "online_count") else 0
    )
    group_stickers = (
        chat.full_chat.stickerset.title
        if hasattr(chat.full_chat, "stickerset") and chat.full_chat.stickerset
        else None
    )
    messages_viewable = msg_info.count if msg_info else None
    messages_sent = (
        chat.full_chat.read_inbox_max_id
        if hasattr(chat.full_chat, "read_inbox_max_id")
        else None
    )
    messages_sent_alt = (
        chat.full_chat.read_outbox_max_id
        if hasattr(chat.full_chat, "read_outbox_max_id")
        else None
    )
    exp_count = chat.full_chat.pts if hasattr(chat.full_chat, "pts") else None
    username = chat_obj_info.username if hasattr(chat_obj_info, "username") else None
    bots_list = chat.full_chat.bot_info  # this is a list
    bots = 0
    supergroup = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "megagroup") and chat_obj_info.megagroup
        else "No"
    )
    slowmode = (
        "<b>مـفعل</b>"
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else "غير مفـعل"
    )
    slowmode_time = (
        chat.full_chat.slowmode_seconds
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else None
    )
    restricted = (
        "<b>نـعم</b>"
        if hasattr(chat_obj_info, "restricted") and chat_obj_info.restricted
        else "لا"
    )
    verified = (
        "<b>مـوثق</b>"
        if hasattr(chat_obj_info, "verified") and chat_obj_info.verified
        else "غيـر موثق"
    )
    username = "@{}".format(username) if username else None
    creator_username = "@{}".format(creator_username) if creator_username else None
    # end of spaghetti block

    if admins is None:
        # use this alternative way if chat.full_chat.admins_count is None,
        # works even without being an admin
        try:
            participants_admins = await event.client(
                GetParticipantsRequest(
                    channel=chat.full_chat.id,
                    filter=ChannelParticipantsAdmins(),
                    offset=0,
                    limit=0,
                    hash=0,
                )
            )
            admins = participants_admins.count if participants_admins else None
        except Exception as e:
            print("Exception:", e)
    if bots_list:
        for bot in bots_list:
            bots += 1

    caption = "<b>❈╎معلومـات الدردشـة  🝢 :</b>\n"
    caption += f"❈╎الآيـدي  : <code>{chat_obj_info.id}</code>\n"
    if chat_title is not None:
        caption += f"❈╎إسـم المجموعـة  :{chat_title}\n"
    if former_title is not None:  # Meant is the very first title
        caption += f"❈╎الإسم السابـق  : {former_title}\n"
    if username is not None:
        caption += f"❈╎نـوع المجموعـة ⌂ : مجموعـة عامّـة  \n"
        caption += f"❈╎الرابـط  : \n {username}\n"
    else:
        caption += f"❈╎نـوع المجموعـة ⌂ : مجموعـة عامّـة  \n"
    if creator_username is not None:
        caption += f"❈╎المالـك  :  {creator_username}\n"
    elif creator_valid:
        caption += ('❈╎المالـك  : <a href="tg://user?id={creator_id}">{creator_firstname}</a>\n')
    if created is not None:
        caption += f"❈╎تاريـخ الإنشـاء  : \n <code>{created.date().strftime('%b %d, %Y')} - {created.time()}</code>\n"
    else:
        caption += f"❈╎الإنتـاج  :   <code>{chat_obj_info.date.date().strftime('%b %d, %Y')} - {chat_obj_info.date.time()}</code> {warn_emoji}\n"
    caption += f"❈╎آيـدي قاعـدة البيانـات : {dc_id}\n"
    if exp_count is not None:
        chat_level = int((1 + sqrt(1 + 7 * exp_count / 14)) / 2)
        caption += f"❈╎الأعضـاء : <code>{chat_level}</code>\n"
    if messages_viewable is not None:
        caption += f"❈╎الرسائـل التي يمڪن مشاهدتها : <code>{messages_viewable}</code>\n"
    if messages_sent:
        caption += f"❈╎الرسائـل المرسلـة  :<code>{messages_sent}</code>\n"
    elif messages_sent_alt:
        caption += f"❈╎الرسـائل المرسلة: <code>{messages_sent_alt}</code> {warn_emoji}\n"
    if members is not None:
        caption += f"❈╎الأعضـاء : <code>{members}</code>\n"
    if admins is not None:
        caption += f"❈╎المشرفيـن : <code>{admins}</code>\n"
    if bots_list:
        caption += f"❈╎البـوتات : <code>{bots}</code>\n"
    if members_online:
        caption += f"❈╎المتصليـن حـالياً : <code>{members_online}</code>\n"
    if restrcited_users is not None:
        caption += f"❈╎الأعضـاء المقيّديـن : <code>{restrcited_users}</code>\n"
    if banned_users is not None:
        caption += f"❈╎الأعضـاء المحظوريـن : <code>{banned_users}</code>"
    if group_stickers is not None:
        caption += f'{chat_type} ❈╎الملصقـات : <a href="t.me/addstickers/{chat.full_chat.stickerset.short_name}">{group_stickers}</a>'
    caption += "\n"
    if not broadcast:
        caption += f"❈╎الوضـع البطيئ : {slowmode}"
        if (
            hasattr(chat_obj_info, "slowmode_enabled")
            and chat_obj_info.slowmode_enabled):
            caption += f", <code>{slowmode_time}s</code>\n"
        else:
            caption += "\n"
        caption += f"❈╎الـمجموعـة الخارقـة  : {supergroup}\n"
    if hasattr(chat_obj_info, "restricted"):
        caption += f"❈╎المقيّـد : {restricted}"
        if chat_obj_info.restricted:
            caption += f"> : {chat_obj_info.restriction_reason[0].platform}\n"
            caption += f"> ❈╎السـبب  : {chat_obj_info.restriction_reason[0].reason}\n"
            caption += f"> ❈╎النّـص  : {chat_obj_info.restriction_reason[0].text}\n\n"
        else:
            caption += "\n"
    if hasattr(chat_obj_info, "scam") and chat_obj_info.scam:
        caption += "❈╎السارقيـن : <b>Yes</b>\n"
    if hasattr(chat_obj_info, "verified"):
        caption += f"❈╎الحسابـات الموثقـة   : {verified}\n"
    if description:
        caption += f"❈╎الوصـف  : \n<code>{description}</code>\n"
    return caption


@bot.on(admin_cmd(pattern="رفع الحظر ?(.*)"))
@bot.on(sudo_cmd(pattern="رفع الحظر ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str:
        LOGS.info("TODO: Not yet Implemented")
    else:
        if event.is_private:
            return False
        et = await edit_or_reply(event, "**↫ البحث في قوائم المشاركين ⇲**")
        p = 0
        async for i in event.client.iter_participants(
            event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
        ):
            rights = ChatBannedRights(until_date=0, view_messages=False)
            try:
                await event.client(
                    functions.channels.EditBannedRequest(event.chat_id, i, rights)
                )
            except Exception as ex:
                await et.edit(str(ex))
            else:
                p += 1
        await et.edit("⪼ {} **↫** {} **رفع الحظر عنهم**".format(event.chat_id, p))


@bot.on(admin_cmd(pattern="الاحصائيات ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="الاحصائيات ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return False
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not chat.admin_rights and not chat.creator:
            await edit_or_reply(event, "**⪼ يجب ان تكون مشرف اولاً 𓆰**")
            return False
    p = 0
    b = 0
    c = 0
    d = 0
    e = []
    m = 0
    n = 0
    y = 0
    w = 0
    o = 0
    q = 0
    r = 0
    et = await edit_or_reply(event, "**↫ البحث في قوائم المشاركين ⇲**")
    async for i in event.client.iter_participants(event.chat_id):
        p += 1
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChatBannedRights(until_date=None, view_messages=True)
        if isinstance(i.status, UserStatusEmpty):
            y += 1
            if "y" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**↫ احتاج الى صلاحيات المشرف اولا ⇲**")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastMonth):
            m += 1
            if "m" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**↫ احتاج الى صلاحيات المشرف اولا ⇲**")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastWeek):
            w += 1
            if "w" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**↫ احتاج الى صلاحيات المشرف اولا ⇲**")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusOffline):
            o += 1
            if "o" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("**↫ احتاج الى صلاحيات المشرف اولا ⇲**")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusOnline):
            q += 1
            if "q" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("**↫ احتاج الى صلاحيات المشرف اولا ⇲**")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusRecently):
            r += 1
            if "r" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**↫ احتاج الى صلاحيات المشرف اولا ⇲**")
                    e.append(str(e))
                    break
        if i.bot:
            b += 1
            if "b" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("**↫ احتاج الى صلاحيات المشرف اولا ⇲**")
                    e.append(str(e))
                    break
                else:
                    c += 1
        elif i.deleted:
            d += 1
            if "d" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**↫ احتاج الى صلاحيات المشرف اولا ⇲**")
                    e.append(str(e))
        elif i.status is None:
            n += 1
    if input_str:
        required_string = """𓆰 𝑺𝑶𝑼𝑹𝑪𝑬 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢   𓆪\n𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻
**⌔∮ المطرودين {} / {} المستخدمين 
**⌔∮ الحسابات المحذوفه :** {}
**⌔∮ اخر ظهور منذ زمن طويل :** {}
**⌔∮ اخر ظهور منذ شهر :** {}
**⌔∮ اخر ظهور منذ اسبوع :** {}
**⌔∮ متصل :** {}
**⌔∮ غير متصل :** {}
**⌔∮ اخر ظهور منذ قليل :** {}
**⌔∮ البوتات :** {}
𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻"""
        await et.edit(required_string.format(c, p, d, y, m, w, o, q, r, b, n))
        await sleep(5)
    await et.edit(
        """𓆰 𝑺𝑶𝑼𝑹𝑪𝑬 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢 𓆪\n𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻
**⌔∮ العدد : ** {} مستخدم 
**⌔∮ الحسابات المحذوفه :** {}
**⌔∮ اخر ظهور منذ زمن طويل :** {}
**⌔∮ اخر ظهور منذ شهر :** {}
**⌔∮ اخر ظهور منذ اسبوع :** {}
**⌔∮ متصل :** {}
**⌔∮ غير متصل :** {}
**⌔∮ اخر ظهور منذ قليل :** {}
**⌔∮ البوتات :** {}
𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻""".format(
            p, d, y, m, w, o, q, r, b, n
        )
    )


@bot.on(admin_cmd(pattern=f"الحسابات المحذوفه ?(.*)"))
@bot.on(sudo_cmd(pattern="الحسابات المحذوفه ?(.*)", allow_sudo=True))
async def rm_deletedacc(show):
    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "**لم يتم العثور على حسابات محذوفـه في هذه المجموعة ، المجموعة نظيفـه**"
    if con != "تنظييف":
        event = await edit_or_reply(
            show, "**╮ ❐ جـارِ البحث عن الحسابات المحذوفـه ☠╰**"
        )
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(0.5)
        if del_u > 0:
            del_status = f"تم العثور على {del_u} حساب (حسابات) محذوفـه في هذه المجموعه\nنظفهم باستخدام الامر .تنظييف الحسابات المحذوفه"
        await event.edit(del_status)
        return
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_delete(show, "**انت لست مسؤول هنا ...**", 5)
        return
    event = await edit_or_reply(
        show, "**╮ ❐ جـارِ حذف الحسابات المحذوفـه ...  ☠╰**"
    )
    del_u = 0
    del_a = 0
    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client.kick_participant(show.chat_id, user.id)
                await sleep(0.5)
                del_u += 1
            except ChatAdminRequiredError:
                await edit_delete(event, "**عذراً انت لا تملك صلاحية الحذف هنا...**", 5)
                return
            except UserAdminInvalidError:
                del_a += 1
    if del_u > 0:
        del_status = f"تم تنظيـف **{del_u}** من الحسابات المحذوفـه"
    if del_a > 0:
        del_status = f"تم تنظيـف**{del_u}** من الحسابات المحذوفـه \n**{del_a}** لـم تتم إزالة حسابات المشـرفين المحذوفـه"
    await edit_delete(event, del_status, 5)
    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID,
            f"#CLEANUP\
            \n{del_status}\
            \nCHAT: {show.chat.title}(`{show.chat_id}`)",
        )


async def ban_user(chat_id, i, rights):
    try:
        await bot(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)


@bot.on(admin_cmd(pattern=r"ضيف ?(.*)"))
@bot.on(sudo_cmd(pattern=r"ضيف ?(.*)", allow_sudo=True))
async def get_users(event):
    sender = await event.get_sender()
    me = await event.client.get_me()
    if not sender.id == me.id:
        kno = await event.reply("**❈╎تتـم العـملية انتظـࢪ قليلا ..**")
    else:
        kno = await event.edit("**❈╎تتـم العـملية انتظـࢪ قليلا ..**.")
    ZEDTHON = await get_chatinfo(event)
    chat = await event.get_chat()
    if event.is_private:
        return await kno.edit("**❈╎لا يمكننـي اضافـة المـستخدمين هـنا**")
    s = 0
    f = 0
    error = "None"

    await kno.edit("**❈╎حـالة الأضافة:**\n\n**❈╎تتـم جـمع معـلومات الـمستخدمين 🔄 ...⏣**")
    async for user in event.client.iter_participants(ZEDTHON.full_chat.id):
        try:
            if error.startswith("Too"):
                return (
                    await kno.edit(
                        f"**❈╎حـالة الأضـافة انتـهت مـع الأخـطاء**\n- (**ربـما هـنالك ضغـط عـلى الأمر حاول مجـدا لاحقـا **) \n**❈╎الـخطأ ** : \n`{error}`\n\n❈╎اضالـة `{s}` \n❈╎خـطأ بأضافـة `{f}`"
                    ),
                )
            await event.client(
                functions.channels.InviteToChannelRequest(channel=chat, users=[user.id])
            )
            s = s + 1
            await kno.edit(f"**❈╎تتـم الأضـافة :**\n\n❈╎اضـيف `{s}` \n❈╎ خـطأ بأضافـة `{f}` \n\n**❈╎× اخـر خـطأ:** `{error}`")
        except Exception as e:
            error = str(e)
            f = f + 1
    return await kno.edit(f"**❈╎اڪتـملت الأضافـة ✅** : \n\n❈╎تـم بنجـاح اضافـة `{s}` \n❈╎خـطأ بأضافـة `{f}`")
    
@bot.on(admin_cmd(pattern=r"تفليش(.*)"))
@bot.on(sudo_cmd(pattern=r"تفليش(.*)", allow_sudo=True))
async def _(event):
    result = await event.client(functions.channels.GetParticipantRequest(event.chat_id, event.client.uid))
    if not result:
        return await edit_or_reply(event, "**❈╎ليس لديك صلاحيه الحظـر في هـذه الدردشـه**")
    zedthonevent = await edit_or_reply(event, "**❈╎جـاري اتمـام العمليـه .. الرجـاء الانتظـار 🚸**")
    admins = await event.client.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client(EditBannedRequest(event.chat_id, user.id, ZELZAL_RIGHTS))
                success += 15
                await sleep(0.2)  
        except Exception as e:
            LOGS.info(str(e))
    await zedthonevent.edit(f"**❈╎تـم  تفلـيش {total} عضـو .. بنجـاح ☑️🗑**")
    
async def ban_user(chat_id, i, rights):
    try:
        await zedthon(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)


@bot.on(admin_cmd(pattern=r"غادر(.*)"))
@bot.on(sudo_cmd(pattern=r"غادر(.*)", allow_sudo=True))
async def kickme(leave):
    await leave.edit("**❈╎جـاري مـغادرة المجـموعة مـع السـلامة  🚶‍♂️  ..**")
    await leave.client.kick_participant(leave.chat_id, "me")

@bot.on(admin_cmd(pattern=r"مسح المحظورين(.*)"))
@bot.on(sudo_cmd(pattern=r"مسح المحظورين(.*)", allow_sudo=True))
async def _(event):
    catevent = await edit_or_reply(event, "**❈╎ إلغاء حظر جميع الحسابات المحظورة في هذه المجموعة 🆘**")
    succ = 0
    total = 0
    flag = False
    chat = await event.get_chat()
    async for i in event.client.iter_participants(event.chat_id, filter=ChannelParticipantsKicked, aggressive=True):
        total += 1
        rights = ChatBannedRights(until_date=0, view_messages=False)
        try:
            await event.client(functions.channels.EditBannedRequest(event.chat_id, i, rights))
        except FloodWaitError as e:
            LOGS.warn(f"**❈╎هناك ضغط كبير بالاستخدام يرجى الانتضار .. ‼️ بسبب  : {e.seconds} **")
            await catevent.edit(f"**❈╎{readable_time(e.seconds)} مطلـوب المـعاودة مـرة اخـرى للـمسح 🔁 **")
            await sleep(e.seconds + 5)
        except Exception as ex:
            await catevent.edit(str(ex))
        else:
            succ += 1
            if flag:
                await sleep(2)
            else:
                await sleep(1)
            try:
                if succ % 10 == 0:
                    await catevent.edit(f"**❈╎جـاري مسـح المحـظورين ⭕️  : \n {succ} الحسـابات الـتي غيـر محظـورة لحـد الان.**")
            except MessageNotModifiedError:
                pass
    await catevent.edit(f"**❈╎تـم مسـح المحـظورين مـن أصـل 🆘 :**{succ}/{total} \n اسـم المجـموعـة 📄 : {chat.title}")

@bot.on(admin_cmd(pattern=r"المحذوفين ?([\s\S]*)"))
@bot.on(sudo_cmd(pattern=r"المحذوفين ?([\s\S]*)", allow_sudo=True))
async def rm_deletedacc(show):
    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "**❈╎لا توجـد حـسابات محذوفـة في هـذه المجموعـة !**"
    if con != "تنظيف":
        event = await edit_or_reply(show, "**❈╎جـاري البحـث عـن الحسابـات المحذوفـة ⌯**")
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(0.5)
        if del_u > 0:
            del_status = f"**❈╎تم ايجـاد  {del_u}  من  الحسابـات المحذوفـه في هـذه المجموعـه**\n**❈╎لحذفهـم إستخـدم الأمـر  ⩥ :**  `.المحذوفين تنظيف`"
        await event.edit(del_status)
        return
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_delete(show, "❈╎أنـا لسـت مشـرفـاً هنـا !", 5)
        return
    event = await edit_or_reply(show, "**❈╎جـاري حـذف الحسـابات المحذوفـة ⌯**")
    del_u = 0
    del_a = 0
    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client.kick_participant(show.chat_id, user.id)
                await sleep(0.5)
                del_u += 1
            except ChatAdminRequiredError:
                await edit_delete(event, "**❈╎ ليس لدي صلاحيات الحظر هنا**", 5)
                return
            except UserAdminInvalidError:
                del_a += 1
    if del_u > 0:
        del_status = f"**❈╎تـم حـذف  {del_u}  الحسـابات المحذوفـة ✓**"
    if del_a > 0:
        del_status = f"**❈╎تـم حـذف {del_u} الحسـابات المحذوفـة، ولڪـن لـم يتـم حذف الحسـابات المحذوفـة للمشرفيـن !**"
    await edit_delete(event, del_status, 5)
    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID,
            f"**❈╎تنظيف :**\
            \n❈╎{del_status}\
            \n*❈╎المحادثـة ⌂** {show.chat.title}(`{show.chat_id}`)",
        )

@bot.on(admin_cmd(pattern=r"احصائيات الاعضاء ?([\s\S]*)"))
@bot.on(sudo_cmd(pattern=r"احصائيات الاعضاء ?([\s\S]*)", allow_sudo=True))
async def _(event):  # sourcery no-metrics
    "To get breif summary of members in the group.1 11"
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not chat.admin_rights and not chat.creator:
            await edit_or_reply(event, "**❈╎انت لست مشرف هنا**")
            return False
    p = 0
    b = 0
    c = 0
    d = 0
    e = []
    m = 0
    n = 0
    y = 0
    w = 0
    o = 0
    q = 0
    r = 0
    et = await edit_or_reply(event, "**❈╎جـاري البحـث عـن قوائـم المشارڪيـن ⌯**")
    async for i in event.client.iter_participants(event.chat_id):
        p += 1
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChatBannedRights(until_date=None, view_messages=True)
        if isinstance(i.status, UserStatusEmpty):
            y += 1
            if "y" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**❈╎أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastMonth):
            m += 1
            if "m" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**❈╎أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastWeek):
            w += 1
            if "w" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**❈╎أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusOffline):
            o += 1
            if "o" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("**❈╎أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusOnline):
            q += 1
            if "q" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("**❈╎أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusRecently):
            r += 1
            if "r" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**❈╎أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
                    break
        if i.bot:
            b += 1
            if "b" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("**❈╎احتاج الى صلاحيات المشرفين للقيام بهذا الامر **")
                    e.append(str(e))
                    break
                else:
                    c += 1
        elif i.deleted:
            d += 1
            if "d" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("**❈╎أحتـاج إلى صلاحيـات المشـرف لإجـراء هـذا الأمـر !**")
                    e.append(str(e))
        elif i.status is None:
            n += 1
    if input_str:
        required_string = """**❈╎الـمطرودين {} / {} الأعـضاء
❈╎الحـسابـات المـحذوفة: {}
❈╎حـالة المستـخدم الفـارغه: {}
❈╎اخر ظهور منذ شـهر: {}
❈╎اخر ظـهور منـذ اسبوع: {}
❈╎غير متصل: {}
❈╎المستخدمين النشطون: {}
❈╎اخر ظهور قبل قليل: {}
❈╎البوتات: {}
❈╎مـلاحظة: {}**"""
        await et.edit(required_string.format(c, p, d, y, m, w, o, q, r, b, n))
        await sleep(5)
    await et.edit(
        """**❈╎: {} مـجموع المـستخدمين
❈╎الحـسابـات المـحذوفة: {}
❈╎حـالة المستـخدم الفـارغه: {}
❈╎اخر ظهور منذ شـهر: {}
❈╎اخر ظـهور منـذ اسبوع: {}
❈╎غير متصل: {}
❈╎المستخدمين النشطون: {}
❈╎اخر ظهور قبل قليل: {}
❈╎البوتات: {}
❈╎مـلاحظة: {}**""".format(
            p, d, y, m, w, o, q, r, b, n
        )
    )    

def weird_division(n, d):
    return n / d if d else 0

@bot.on(admin_cmd(pattern=r"معلومات تخزين المجموعه(?:\s|$)([\s\S]*)"))
@bot.on(sudo_cmd(pattern=r"معلومات تخزين المجموعه(?:\s|$)([\s\S]*)", allow_sudo=True))
async def _(event):  # sourcery no-metrics
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
    x.title = "File Summary"
    x.field_names = ["Media", "Count", "File size"]
    largest = "   <b>أكبر حجم</b>\n"
    try:
        chatdata = await event.client.get_entity(entity)
    except Exception as e:
        return await edit_delete(
            event, f"<b>❈╎خطـأ ⚠️ : </b><code>{str(e)}</code>", 5, parse_mode="HTML"
        )
    try:
        userdata = await event.client.get_entity(userentity)
    except Exception as e:
        return await edit_delete(
            event, f"<b>❈╎خطـأ ⚠️ : </b><code>{str(e)}</code>", time=5, parse_mode="HTML"
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
        f"<code>❈╎حسـاب عـدد الملفـات وحجـم الملـف حسـب ✦ </code>{_format.htmlmentionuser(userdata.first_name,userdata.id)}<code> in Group </code><b>{link}</b>\n<code>This may take some time also depends on number of user messages</code>",
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
    totalstring = f"<code><b> ❈╎إجمالـي الملفـات ✦ : </b>       | {str(totalcount)}\
                  \n <b> ❈╎الحجـم الإجمالـي للملـف ✦ : </b>   | {humanbytes(totalsize)}\
                  \n <b> حجم الملف  : </b>    | {avghubytes}\
                  \n</code>"
    runtimestring = f"<code><b> ❈╎وقـت التشغيـل ✦ :</b>            | {runtime}\
                    \n <b> وقـت التشغيـل لڪل ملـف ✦ :</b>   | {avgruntime}\
                    \n</code>"
    line = "<code>+--------------------+-----------+</code>\n"
    result = f"<b>❈╎المجموعـة ✦ : {link}\nUser : {_format.htmlmentionuser(userdata.first_name,userdata.id)}\n\n"
    result += f"<code><b>❈╎مجمـوع الرسائـل ✦ :</b> {msg_count}</code>\n"
    result += "<b>❈╎ملخـص الملـف ✦ : </b>\n"
    result += f"<code>{str(x)}</code>\n"
    result += f"{largest}"
    result += line + totalstring + line + runtimestring + line
    await catevent.edit(result, parse_mode="HTML", link_preview=False)    
    
@bot.on(admin_cmd(pattern="الرابط ?(.*)"))
@bot.on(sudo_cmd(pattern="الرابط ?(.*)", allow_sudo=True))
async def zed(SLQ):
    await SLQ.edit("**⇜ جـاري جلـب رابـط المجموعـه ⇜**")
    try:
        l5 = await SLQ.client(
            ExportChatInviteRequest(SLQ.chat_id),
        )
    except ChatAdminRequiredError:
        return await bot.send_message(f"**❈╎عزيزي {ALIVE_NAME} لسـت مشرفـاً في هـذه المجموعـه **")
    await SLQ.edit(f"**❈╎رابـط الـمجموعـه : ✓**\n\n➥ {l5.link}")   
    
@bot.on(admin_cmd(pattern="رسائلي ?(.*)"))
@bot.on(sudo_cmd(pattern="رسائلي ?(.*)", allow_sudo=True))
async def zed(SLQ):
    k = await SLQ.get_reply_message()
    if k:
        a = await bot.get_messages(SLQ.chat_id, 0, from_user=k.sender_id)
        return await SLQ.edit(
            f"**مجموع** `{a.total}` **الرسائل** {thon} **هنا**"
        )
    thon = SLQ.pattern_match.group(1)
    if not thon:
        thon = "me"
    a = await bot.get_messages(SLQ.chat_id, 0, from_user=thon)
    await SLQ.edit(
        f"**❈╎لديـك هنـا ⇽**  `{a.total}`  **رسـالـه 📩**"
    )   

@bot.on(admin_cmd(pattern="تغير صوره( المجموعه| -d)$"))
@bot.on(sudo_cmd(pattern="تغير صوره( المجموعه| -d)$", allow_sudo=True))
async def set_group_photo(event):  # sourcery no-metrics
    "For changing Group dp"
    flag = (event.pattern_match.group(1)).strip()
    if flag == "المجموعة":
        replymsg = await event.get_reply_message()
        photo = None
        if replymsg and replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await event.client.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split("/"):
                photo = await event.client.download_file(replymsg.media.document)
            else:
                return await edit_delete(event, INVALID_MEDIA)
        if photo:
            try:
                await event.client(
                    EditPhotoRequest(
                        event.chat_id, await event.client.upload_file(photo)
                    )
                )
                await edit_delete(event, CHAT_PP_CHANGED)
            except PhotoCropSizeSmallError:
                return await edit_delete(event, PP_TOO_SMOL)
            except ImageProcessFailedError:
                return await edit_delete(event, PP_ERROR)
            except Exception as e:
                return await edit_delete(event, f"**Error : **`{str(e)}`")
            process = "updated"
    else:
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await edit_delete(event, f"**Error : **`{e}`")
        process = "deleted"
        await edit_delete(event, "```successfully group profile pic deleted.```")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "❈╎صوره_المجموعة\n"
            f"❈╎صورة المجموعه {process} بنجاح "
            f"❈╎المحادثة  📜 : {event.chat.title}(`{event.chat_id}`)",
        )

async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("**❈╎لم يتم العثور على المجموعة او القناة**")
            return None
        except ChannelPrivateError:
            await event.reply(
                "**❈╎لا يمكنني استخدام الامر من الكروبات او القنوات الخاصة**"
            )
            return None
        except ChannelPublicGroupNaError:
            await event.reply("**❈╎لم يتم العثور على المجموعة او القناة**")
            return None
        except (TypeError, ValueError):
            await event.reply("**❈╎رابط الكروب غير صحيح**")
            return None
    return chat_info


def make_mention(user):
    if user.username:
        return f"@{user.username}"
    else:
        return inline_mention(user)


def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    full_name = " ".join(names)
    return full_name

@bot.on(admin_cmd(pattern="تفعيل ([\s\S]*)"))    
@bot.on(sudo_cmd(pattern="تفعيل ([\s\S]*)", allow_sudo=True))
async def _(event):  
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    if not event.is_group:
        return await edit_delete(event, "**❈╎ هذه ليست مجموعة لقفل الأشياء**")
    chat_per = (await event.get_chat()).default_banned_rights
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if input_str in (("bots", "commands", "email", "forward", "url")):
        update_lock(peer_id, input_str, True)
        await edit_or_reply(event, "`Locked {}`".format(input_str))
    else:
        msg = chat_per.send_messages
        media = chat_per.send_media
        sticker = chat_per.send_stickers
        gif = chat_per.send_gifs
        gamee = chat_per.send_games
        ainline = chat_per.send_inline
        embed_link = chat_per.embed_links
        gpoll = chat_per.send_polls
        adduser = chat_per.invite_users
        cpin = chat_per.pin_messages
        changeinfo = chat_per.change_info
        if input_str == "msg":
            if msg:
                return await edit_delete(event, "**❈╎ هذه المجموعة مؤمنة بالفعل بإذن المراسلة**")
            msg = True
            locktype = "messages"
        elif input_str == "حمايه المجموعه":
            msg = False
            media = True
            sticker = True
            gif = True
            gamee = True
            ainline = True
            embed_link = True
            gpoll = True
            adduser = True
            cpin = True
            changeinfo = True
            locktype = "everything"
        elif input_str:
            return await edit_delete(event, f"**❈╎ عذرا خطا بكتابه الأمر :** `{input_str}`", time=5)

        else:
            return await edit_or_reply(event, "**❈╎ لااستطيع تفعيل حمايه المجموعه**")
        try:
            cat = Get(cat)
            await event.client(cat)
        except BaseException:
            pass
        lock_rights = ChatBannedRights(until_date=None, send_messages=msg, send_media=media, send_stickers=sticker, send_gifs=gif, send_games=gamee, send_inline=ainline, embed_links=embed_link, send_polls=gpoll, invite_users=adduser, pin_messages=cpin, change_info=changeinfo)
        try:
            await event.client(EditChatDefaultBannedRightsRequest(peer=peer_id, banned_rights=lock_rights))
            await edit_or_reply(event, f"**❈╎ تفعيل حمايه المجموعه تم بنجاح**")
        except BaseException as e:
            await edit_delete(event,f"**❈╎ هناك خطا:** `{e}`", time=5)
@bot.on(admin_cmd(pattern="تعطيل ([\s\S]*)"))    
@bot.on(sudo_cmd(pattern="تعطيل ([\s\S]*)", allow_sudo=True))
async def _(event):  
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    if not event.is_group:
        return await edit_delete(event, "**❈╎ هذه ليست مجموعة لقفل الأشياء**")
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    chat_per = (await event.get_chat()).default_banned_rights
    if input_str in (("bots", "commands", "email", "forward", "url")):
        update_lock(peer_id, input_str, False)
        await edit_or_reply(event, "**❈╎ تعطيل حمايه المجموعه تم بنجاح**".format(input_str))
    else:
        msg = chat_per.send_messages
        media = chat_per.send_media
        sticker = chat_per.send_stickers
        gif = chat_per.send_gifs
        gamee = chat_per.send_games
        ainline = chat_per.send_inline
        gpoll = chat_per.send_polls
        embed_link = chat_per.embed_links
        adduser = chat_per.invite_users
        cpin = chat_per.pin_messages
        changeinfo = chat_per.change_info
        if input_str == "msg":
            if not msg:
                return await edit_delete(event, "**❈╎ هذه المجموعة غير مؤمنة بالفعل بإذن المراسلة**")
            msg = False
            locktype = "messages"
        elif input_str == "حمايه المجموعه":
            msg = False
            media = False
            sticker = False
            gif = False
            gamee = False
            ainline = False
            gpoll = False
            embed_link = False
            adduser = True
            cpin = True
            changeinfo = True
            locktype = "everything"
        elif input_str:
            return await edit_delete(event, f"**❈╎ عذرا خطا بكتابه الأمر :** `{input_str}`", time=5)

        else:
            return await edit_or_reply(event, "**❈╎ لااستطيع تعطيل حمايه المجموعه**")
        try:
            cat = Get(cat)
            await event.client(cat)
        except BaseException:
            pass
        unlock_rights = ChatBannedRights(until_date=None, send_messages=msg, send_media=media, send_stickers=sticker, send_gifs=gif, send_games=gamee, send_inline=ainline, send_polls=gpoll, embed_links=embed_link, invite_users=adduser, pin_messages=cpin, change_info=changeinfo)
        try:
            await event.client(EditChatDefaultBannedRightsRequest(peer=peer_id, banned_rights=unlock_rights))
            await edit_or_reply(event, "**❈╎ تعطيل حمايه المجموعه تم بنجاح**")
        except BaseException as e:
            return await edit_delete(event, f"**❈╎ هناك خطا:** `{e}`", time=5)
@bot.on(admin_cmd(pattern="الاعدادات$"))    
@bot.on(sudo_cmd(pattern="الاعدادات$", allow_sudo=True))
async def _(event):  
    res = ""
    current_db_locks = get_locks(event.chat_id)
    if not current_db_locks:
        res = "لا توجد إعدادات في هذه الدردشة"
    else:
        res = "**❈╎ أذونات الصلاحيه في هذه الدردشة : **\n"
        ubots = "❌" if current_db_locks.bots else "✅"
        ucommands = "❌" if current_db_locks.commands else "✅"
        uemail = "❌" if current_db_locks.email else "✅"
        uforward = "❌" if current_db_locks.forward else "✅"
        uurl = "❌" if current_db_locks.url else "✅"
        res += f"**❈╎ البوتات :** `{ubots}`\n"
        res += f"**❈╎ الرسائل :** `{ucommands}`\n"
        res += f"**❈╎ التوجيهات :** `{uforward}`\n"
        res += f"**❈╎ الروابط :** `{uurl}`\n"
    current_chat = await event.get_chat()
    try:
        chat_per = current_chat.default_banned_rights
    except AttributeError as e:
        logger.info(str(e))
    else:
        umsg = "❌" if chat_per.send_messages else "✅"
        umedia = "❌" if chat_per.send_media else "✅"
        usticker = "❌" if chat_per.send_stickers else "✅"
        ugif = "❌" if chat_per.send_gifs else "✅"
        ugamee = "❌" if chat_per.send_games else "✅"
        uainline = "❌" if chat_per.send_inline else "✅"
        uembed_link = "❌" if chat_per.embed_links else "✅"
        ugpoll = "❌" if chat_per.send_polls else "✅"
        uadduser = "❌" if chat_per.invite_users else "✅"
        ucpin = "❌" if chat_per.pin_messages else "✅"
        uchangeinfo = "❌" if chat_per.change_info else "✅"
        res += "\n**❈╎ هذه هي الأذونات الحالية لهذه الدردشة :** \n"
        res += f"**❈╎ الرسائل :** `{umsg}`\n"
        res += f"**❈╎ الميديا :** `{umedia}`\n"
        res += f"**❈╎ الملصقات :** `{usticker}`\n"
        res += f"**❈╎ المتحركه :** `{ugif}`\n"
        res += f"**❈╎ معاينه الروابط :** `{uembed_link}`\n"
        res += f"**❈╎ الالعاب :** `{ugamee}`\n"
        res += f"**❈╎ الاونلاين :** `{uainline}`\n"
        res += f"**❈╎ اضافه الاعضاء :** `{uadduser}`\n"
        res += f"**❈╎ تغير معلومات :** `{uchangeinfo}`\n"
    await edit_or_reply(event, res)
@bot.on(events.ChatAction())
async def _(event):
    if not event.is_private:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return
    if not is_locked(event.chat_id, "bots"):
        return
    if event.user_added:
        users_added_by = event.action_message.sender_id
        is_ban_able = False
        rights = types.ChatBannedRights(until_date=None, view_messages=True)
        added_users = event.action_message.action.users
        for user_id in added_users:
            user_obj = await event.client.get_entity(user_id)
            if user_obj.bot:
                is_ban_able = True
                try:
                    await event.client(
                        functions.channels.EditBannedRequest(event.chat_id, user_obj, rights))
                except Exception as e:
                    await event.reply("**❈╎ لا يبدو أن لدي صلاحيه هنا. **\n`{}`".format(str(e)))
                    update_lock(event.chat_id, "bots", False)
                    break
        if BOTLOG and is_ban_able:
            ban_reason_msg = await event.reply("**❈╎ تحذير [user](tg://user?id={}) من فضلك لا تضيف الروبوتات إلى هذه الدردشة.**".format(users_added_by))



CMD_HELP.update(
    {
        "كروب2": "**اسم الاضافـه : **`كروب2`\
    \n\n  **╮•❐ الامـر ⦂ **`.غادر`\
    \n•  **الشـرح •• **__لمغـادرة المجموعـه_\
    \n\n  **╮•❐ الامـر ⦂ **`.تفليش `\
    \n•  **الشـرح •• **__لحظـر وطـرد جميـع اعضـاء المجموعـه__\
    \n\n  **╮•❐ الامـر ⦂ **`.رفع الحظر`\
    \n•  **الشـرح •• **__لمسـح جميـع المحظورين من المجموعـه__\
    \n\n  **╮•❐  الامـر ⦂ **`.ضيف `+ رابـط المجموعـه\
    \n•  **الشـرح •• **__اضـافه اعضـاء المجمـوعه لـمجموعتك .. سوي الامر بمجمـوعتك واضف رابط المجموعه الثانيه للامر__\
    \n\n  **╮•❐  الامـر ⦂ **`.المحذوفين `\
    \n•  **الشـرح •• **__لعـرض قائمـه بعـدد الحسـابات المحذوفـه في المجموعـه__\
    \n\n  **╮•❐ الامـر ⦂ **`.الاحصائيات`\
    \n•  **الشـرح •• **__لعـرض قائمـه باحصائيات المجموعـه__\
    \n\n  **╮•❐ الامـر ⦂ **`.معلومات `\
    \n•  **الشـرح •• **__لعـرض قائمـه بمعلومـات المجموعـه__\
    \n\n  **╮•❐ الامـر ⦂ **`.معلومات تخزين المجموعه `\
    \n•  **الشـرح •• **__لعـرض قائمـه بوسائـط المجمـوعـه المخزنـه فيـها__\
    \n\n  **╮•❐ الامـر ⦂ **`.تخزين الخاص تفعيل/تعطيل `\
    \n•  **الشـرح •• **__لتفعيل/تعطيل تخزين كروب الرسائل للخـاص__\
    \n\n  **╮•❐ الامـر ⦂ **`.تخزين المجموعات تفعيل/تعطيل `\
    \n•  **الشـرح •• **__لتفعيل/تعطيل تخزين كروب الرسائل لتخزين رسائل وتاكات المجموعات__\
    \n\n  **╮•❐ الامـر ⦂ **`.الرابط `\
    \n•  **الشـرح •• **__لجلب رابـط المجموعـه .. يجب ان تكون مشرفـاً فيهـا__\
    \n\n  **╮•❐ الامـر ⦂ **`.رسائلي `\
    \n•  **الشـرح •• **__لمعـرفة عـدد رسائلك في المجموعـه__\
    \n\n  **╮•❐ الامـر ⦂ **`.تفعيل/تعطيل حمايه المجموعه `\
    \n•  **الشـرح •• **__لقفل اعدادات المجموعـه لحمايتهـا من التخريب__\
    \n\n  **╮•❐ الامـر ⦂ **`.الاعدادات `\
    \n•  **الشـرح •• **__لعـرض اعـدادات المجموعـه__\
    \n\n  **╮•❐ الامـر ⦂ **`.تغير صوره المجموعه ` بالـرد ع صـوره\
    \n•  **الشـرح •• **__لتغيير صـورة المجموعـه__\
    \n\n  **╮•❐ الامـر ⦂ **`.الحسابات المحذوفه`\
    \n•  **الشـرح •• **__للبحث عن الحسـابات المحذوفـة في المجموعـه .. ثم استخـدم الامـر `.الحسابات المحذوفه تنظيف` لطـرد جميـع الحسـابات المحذوفـه من المجموعـه.__"
    }
)
