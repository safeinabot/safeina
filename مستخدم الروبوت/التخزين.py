# pm and tagged messages logger for safeina edit by:  @S_F_M_L

import asyncio

from telethon import events

from . import BOTLOG, BOTLOG_CHATID, LOGS
from .sql_helper import no_log_pms_sql
from .sql_helper.globals import addgvar, gvarstatus


class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0


LOG_CHATS_ = LOG_CHATS()


@bot.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def monito_p_m_s(event):
    if not Config.PM_LOGGER_GROUP_ID:
        return
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        return
    sender = await event.get_sender()
    if not sender.bot:
        chat = await event.get_chat()
        if not no_log_pms_sql.is_approved(chat.id) and chat.id != 777000:
            if LOG_CHATS_.RECENT_USER != chat.id:
                LOG_CHATS_.RECENT_USER = chat.id
                if LOG_CHATS_.NEWPM:
                    if LOG_CHATS_.COUNT > 1:
                        await LOG_CHATS_.NEWPM.edit(
                            LOG_CHATS_.NEWPM.text.replace(
                                "**رسـاله جديـده 📬**", f"{LOG_CHATS_.COUNT} **رسالـه**"
                            )
                        )
                    else:
                        await LOG_CHATS_.NEWPM.edit(
                            LOG_CHATS_.NEWPM.text.replace(
                                "**رسـاله جديـده 📬**", f"{LOG_CHATS_.COUNT} **رسالـه**"
                            )
                        )
                    LOG_CHATS_.COUNT = 0
                LOG_CHATS_.NEWPM = await event.client.send_message(
                    Config.PM_LOGGER_GROUP_ID,
                    f"❈╎{_format.mentionuser(sender.first_name , sender.id)} أرسـل لك رسالـة جديـدة  \n❈╎الايـدي : `{chat.id}`",
                )
            try:
                if event.message:
                    await event.client.forward_messages(
                        Config.PM_LOGGER_GROUP_ID, event.message, silent=True
                    )
                LOG_CHATS_.COUNT += 1
            except Exception as e:
                LOGS.warn(str(e))


@bot.on(events.NewMessage(incoming=True, func=lambda e: e.mentioned))
async def log_tagged_messages(event):
    hmm = await event.get_chat()
    from ._afk import AFK_

    if gvarstatus("GRPLOG") and gvarstatus("GRPLOG") == "false":
        return
    if (
        (no_log_pms_sql.is_approved(hmm.id))
        or (not Config.PM_LOGGER_GROUP_ID)
        or ("on" in AFK_.USERAFK_ON)
        or (await event.get_sender() and (await event.get_sender()).bot)
    ):
        return
    full = None
    try:
        full = await event.client.get_entity(event.message.from_id)
    except Exception as e:
        LOGS.info(str(e))
    messaget = media_type(event)
    resalt = f"#التاكـات \n<b>الكـروب : </b><code>{hmm.title}</code>"
    if full is not None:
        resalt += (
            f"\n<b>مـن : </b> ❈╎{_format.htmlmentionuser(full.first_name , full.id)}"
        )
    if messaget is not None:
        resalt += f"\n<b>نـوع الرسالـه : </b><code>{messaget}</code>"
    else:
        resalt += f"\n<b>الرسالـه : </b>{event.message.message}"
    resalt += f"\n<b>رابـط الرسالـه: </b><a href = 'https://t.me/c/{hmm.id}/{event.message.id}'> link</a>"
    if not event.is_private:
        await event.client.send_message(
            Config.PM_LOGGER_GROUP_ID,
            resalt,
            parse_mode="html",
            link_preview=False,
        )


@bot.on(admin_cmd(outgoing=True, pattern=r"حفظ(?: |$)(.*)"))
async def log(log_text):
    if BOTLOG:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(BOTLOG_CHATID)
        elif log_text.pattern_match.group(1):
            user = f"#الحفظ / ايدي الدردشـه: {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await log_text.client.send_message(BOTLOG_CHATID, textx)
        else:
            await log_text.edit("`What am I supposed to log?`")
            return
        await log_text.edit("**❈╎تـم الحفـظ بنجـاح ✅...**")
    else:
        await log_text.edit("**❈╎تتطلب هذه الميزة تمكين التخزين! ...**")
    await asyncio.sleep(2)
    await log_text.delete()


@bot.on(admin_cmd(pattern="تفعيل التخزين$"))
async def set_no_log_p_m(event):
    if Config.PM_LOGGER_GROUP_ID is not None:
        chat = await event.get_chat()
        if no_log_pms_sql.is_approved(chat.id):
            no_log_pms_sql.disapprove(chat.id)
            await edit_delete(
                event, "**❈╎تم بـدئ تسجيـل الرسـائل من هـذه المجموعـه ✅...**", 5
            )


@bot.on(admin_cmd(pattern="تعطيل التخزين$"))
async def set_no_log_p_m(event):
    if Config.PM_LOGGER_GROUP_ID is not None:
        chat = await event.get_chat()
        if not no_log_pms_sql.is_approved(chat.id):
            no_log_pms_sql.approve(chat.id)
            await edit_delete(
                event, "**❈╎تم ايقـاف تسجيـل الرسـائل من هـذه المجموعـه ✅...**", 5
            )


@bot.on(admin_cmd(pattern="تخزين الخاص (تفعيل|تعطيل)$"))
async def set_pmlog(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str == "تعطيل":
        h_type = False
    elif input_str == "تفعيل":
        h_type = True
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        PMLOG = False
    else:
        PMLOG = True
    if PMLOG:
        if h_type:
            await event.edit("**❈╎تخـزين رسائـل الخـاص ممكّن بالفعـل ✅...**")
        else:
            addgvar("PMLOG", h_type)
            await event.edit("**❈╎تم تعطيـل تخـزين رسائـل الخـاص .. بنجـاح✅**")
    else:
        if h_type:
            addgvar("PMLOG", h_type)
            await event.edit("**❈╎تم تفعيـل تخـزين رسائـل الخـاص .. بنجـاح✅**")
        else:
            await event.edit("**❈╎تخـزين رسائـل الخـاص معطـل بالفعـل ✅...**")


@bot.on(admin_cmd(pattern="تخزين المجموعه (تفعيل|تعطيل)$"))
async def set_grplog(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str == "تعطيل":
        h_type = False
    elif input_str == "تفعيل":
        h_type = True
    if gvarstatus("GRPLOG") and gvarstatus("GRPLOG") == "false":
        GRPLOG = False
    else:
        GRPLOG = True
    if GRPLOG:
        if h_type:
            await event.edit("**❈╎تخـزين المجموعـات ممكّن بالفعـل ✅...**")
        else:
            addgvar("GRPLOG", h_type)
            await event.edit("**❈╎تم تعطيـل تخـزين المجموعـات .. بنجـاح ✅**")
    else:
        if h_type:
            addgvar("GRPLOG", h_type)
            await event.edit("**❈╎تم تفعيـل تخـزين المجموعـات .. بنجـاح✅**")
        else:
            await event.edit("**❈╎تخـزين المجموعـات معطـل بالفعـل ✅...**")


CMD_HELP.update(
    {
        "التخزين": "**اسم الاضافـه : **`التخزين`\
        \n\n  **╮•❐ الامـر ⦂ **`.حفظ`\
        \n•  **الشـرح •• **__يحفظ الرسائـل المحـدده في مجموعـتك الخاصـه ( كروب حافظة بوتك ) .__\
        \n\n  **╮•❐ الامـر ⦂ **`.تفعيل التخزين`\
        \n•  **الشـرح •• **__لـتفعيـل  التخزين لرسـائل محـادثات الخـاص والمجموعـات ...__\
        \n\n  **╮•❐ الامـر ⦂ **`.تعطيل التخزين`\
        \n•  **الشـرح •• **__لـتعطيـل  التخزين لرسـائل محـادثات الخـاص والمجموعـات ...__\
        \n\n  **╮•❐ الامـر ⦂ **`.تخزين الخاص تفعيل/تعطيل`\
        \n•  **الشـرح •• **__لتشغيل وإيقاف تشغيل تسجيـل الرسائل الشخصيـه ...__\
        \n\n  **╮•❐ الامـر ⦂ **`.تخزين المجموعه تفعيل/تعطيل`\
        \n•  **الشـرح •• **__لتشغيل وإيقاف تشغيل تسجيـل الرسائل الشخصيـه والمحذوفـه .. من تشغل الامر هذا اي رساله يدزها حدا وانته مو موجود ويحذفها راح توصلك لكروب الحافظـه ...__\
        "
    }
)
