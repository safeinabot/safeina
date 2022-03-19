# Afk plugin from zed ported from uniborg

import asyncio
from datetime import datetime

from telethon import events
from telethon.tl import functions, types

from . import BOTLOG, BOTLOG_CHATID


class AFK:
    def __init__(self):
        self.USERAFK_ON = {}
        self.afk_time = None
        self.last_afk_message = {}
        self.afk_star = {}
        self.afk_end = {}
        self.reason = None
        self.msg_link = False
        self.afk_type = None
        self.media_afk = None


AFK_ = AFK()


@bot.on(events.NewMessage(outgoing=True))
async def set_not_afk(event):
    if event.chat_id in Config.UB_BLACK_LIST_CHAT:
        return
    back_alive = datetime.now()
    AFK_.afk_end = back_alive.replace(microsecond=0)
    if AFK_.afk_star != {}:
        total_afk_time = AFK_.afk_end - AFK_.afk_star
        time = int(total_afk_time.seconds)
        d = time // (24 * 3600)
        time %= 24 * 3600
        h = time // 3600
        time %= 3600
        m = time // 60
        time %= 60
        s = time
        endtime = ""
        if d > 0:
            endtime += f"{d}d {h}h {m}m {s}s"
        else:
            if h > 0:
                endtime += f"{h}h {m}m {s}s"
            else:
                endtime += f"{m}m {s}s" if m > 0 else f"{s}s"
    current_message = event.message.message
    if (("تنبيه" not in current_message) or ("#تنبيه" not in current_message)) and (
        "تفعيل" in AFK_.USERAFK_ON
    ):
        shite = await event.client.send_message(
            event.chat_id,
            "لقد اتيت 😇♩ لا مزيد من الانشغال .\nلقد كنت مشغولا لمدة " + endtime + "`",
        )
        AFK_.USERAFK_ON = {}
        AFK_.afk_time = None
        await asyncio.sleep(5)
        await shite.delete()
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#تعطيـل_التنبيـه \n**تـم ايقـاف وضـع التنبيـه بنجـاح 🔕✅**\n"
                + "لقد اتيت 😇♩ لا مزيد من الانشغال .\nلقد كنت مشغولا لمدة "
                + endtime
                + "`",
            )


@bot.on(
    events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private))
)
async def on_afk(event):
    if event.fwd_from:
        return
    back_alivee = datetime.now()
    AFK_.afk_end = back_alivee.replace(microsecond=0)
    if AFK_.afk_star != {}:
        total_afk_time = AFK_.afk_end - AFK_.afk_star
        time = int(total_afk_time.seconds)
        d = time // (24 * 3600)
        time %= 24 * 3600
        h = time // 3600
        time %= 3600
        m = time // 60
        time %= 60
        s = time
        endtime = ""
        if d > 0:
            endtime += f"{d}d {h}h {m}m {s}s"
        else:
            if h > 0:
                endtime += f"{h}h {m}m {s}s"
            else:
                endtime += f"{m}m {s}s" if m > 0 else f"{s}s"
    current_message_text = event.message.message.lower()
    if "تنبيه" in current_message_text or "#تنبيه" in current_message_text:
        # userbot's should not reply to other userbot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return False
    if not await event.get_sender():
        return
    if AFK_.USERAFK_ON and not (await event.get_sender()).bot:
        msg = None
        if AFK_.afk_type == "text":
            if AFK_.msg_link and AFK_.reason:
                message_to_reply = (
                    f"╮⊹ هها صديقي ⤶ انا غير موجود حـالياً 😇♩\nٴ﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎\n**╮⊹ سـوف اقـوم بالـرد عليك ⤶ في اقـرب وقـت ↻..**\n\n{AFK_.reason}"
                )
            elif AFK_.reason:
                message_to_reply = (
                    f"╮⊹ هها صديقي ⤶ انا غير موجود حـالياً 😇♩\nٴ﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎\n**╮⊹ سـوف اقـوم بالـرد عليك ⤶ في اقـرب وقـت ↻..**\n\n{AFK_.reason}"
                )
            else:
                message_to_reply = f"**╮⊹ هها صديقي ⤶ انا غير موجود حـالياً 😇♩**\nٴ﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎\n**╮⊹ سـوف اقـوم بالـرد عليك ⤶ في اقـرب وقـت ↻..**"
            if event.chat_id not in Config.UB_BLACK_LIST_CHAT:
                msg = await event.reply(message_to_reply)
        elif AFK_.afk_type == "media":
            if AFK_.reason:
                message_to_reply = (
                    f"╮⊹ هها صديقي ⤶ انا غير موجود حـالياً 😇♩\nٴ﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎\n**╮⊹ سـوف اقـوم بالـرد عليك ⤶ في اقـرب وقـت ↻..**\n\n{AFK_.reason}"
                )
            else:
                message_to_reply = f"**╮⊹ هها صديقي ⤶ انا غير موجود حـالياً 😇♩**\nٴ﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎﹎\n**╮⊹ سـوف اقـوم بالـرد عليك ⤶ في اقـرب وقـت ↻..**"
            if event.chat_id not in Config.UB_BLACK_LIST_CHAT:
                msg = await event.reply(message_to_reply, file=AFK_.media_afk.media)
        if event.chat_id in AFK_.last_afk_message:
            await AFK_.last_afk_message[event.chat_id].delete()
        AFK_.last_afk_message[event.chat_id] = msg
        if event.is_private:
            return
        hmm = await event.get_chat()
        if not Config.PM_LOGGER_GROUP_ID:
            return
        full = None
        try:
            full = await event.client.get_entity(event.message.from_id)
        except Exception as e:
            LOGS.info(str(e))
        messaget = media_type(event)
        resalt = f"#تـاكات_النـائم \n<b>المجـموعـه : </b><code>{hmm.title}</code>"
        if full is not None:
            resalt += f"\n<b>المـرسل : </b> 👤{_format.htmlmentionuser(full.first_name , full.id)}"
        if messaget is not None:
            resalt += f"\n<b>نـوع الرسـاله : </b><code>{messaget}</code>"
        else:
            resalt += f"\n<b>الرسـاله : </b>{event.message.message}"
        resalt += f"\n<b>رابـط الرسـاله: </b><a href = 'https://t.me/c/{hmm.id}/{event.message.id}'> link</a>"
        if not event.is_private:
            await event.client.send_message(
                Config.PM_LOGGER_GROUP_ID,
                resalt,
                parse_mode="html",
                link_preview=False,
            )


@bot.on(admin_cmd(pattern=r"تنبيه ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    AFK_.USERAFK_ON = {}
    AFK_.afk_time = None
    AFK_.last_afk_message = {}
    AFK_.afk_end = {}
    AFK_.afk_type = "text"
    start_1 = datetime.now()
    AFK_.afk_star = start_1.replace(microsecond=0)
    if not AFK_.USERAFK_ON:
        input_str = event.pattern_match.group(1)
        if ";" in input_str:
            msg, mlink = input_str.split(";", 1)
            AFK_.reason = f"[{msg.strip()}]({mlink.strip()})"
            AFK_.msg_link = True
        else:
            AFK_.reason = input_str
            AFK_.msg_link = False
        last_seen_status = await event.client(
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            AFK_.afk_time = datetime.now()
        AFK_.USERAFK_ON = f"**عـلى :** {AFK_.reason}"
        if AFK_.reason:
            await edit_delete(
                event, f"**╮ سأذهب بعيدًا الـى النـوم 🥱🔕♥️والسبب ~ ╰** {AFK_.reason}", 5
            )
        else:
            await edit_delete(event, f"**╮ سأذهب بعيدًا الـى النـوم 🥱🔕♥️╰**", 5)
        if BOTLOG:
            if AFK_.reason:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"#تفعيل_التنبيه \ n**╮ تـم تفعيـل التنبيـه 🔊╰، والسبب هـو {AFK_.reason} **",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"#تفعيل_التنبيه \ n **تـم تفعيـل التنبيـه ، مـع عـدم ذكر السبب**",
                )


@bot.on(admin_cmd(pattern=r"منبه ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    reply = await event.get_reply_message()
    media_t = media_type(reply)
    if media_t == "Sticker" or not media_t:
        return await edit_or_reply(
            event, "**╮ بالـرد ﮼؏ الميـديا لتفعيل تنبيـه الوسائـط 🔊╰**"
        )
    if not BOTLOG:
        return await edit_or_reply(
            event, "** لاستخدام منبـه الوسائـط تحتاج إلى ضبط فـار  PRIVATE_GROUP_BOT_API_ID config**"
        )
    AFK_.USERAFK_ON = {}
    AFK_.afk_time = None
    AFK_.last_afk_message = {}
    AFK_.afk_end = {}
    AFK_.media_afk = None
    AFK_.afk_type = "media"
    start_1 = datetime.now()
    AFK_.afk_star = start_1.replace(microsecond=0)
    if not AFK_.USERAFK_ON:
        input_str = event.pattern_match.group(1)
        AFK_.reason = input_str
        last_seen_status = await event.client(
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            AFK_.afk_time = datetime.now()
        AFK_.USERAFK_ON = f"**عـلى :** {AFK_.reason}"
        if AFK_.reason:
            await edit_delete(
                event, f"**╮ سأذهب بعيدًا الـى النـوم 🥱🔕♥️والسبب ~ ╰** {AFK_.reason}", 5
            )
        else:
            await edit_delete(event, f"**╮ سأذهب بعيدًا الـى النـوم 🥱🔕♥️╰**", 5)
        AFK_.media_afk = await reply.forward_to(BOTLOG_CHATID)
        if AFK_.reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#تفعيل_التنبيه \ n**╮ تـم تفعيـل التنبيـه 🔊╰، والسبب هـو {AFK_.reason} **",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#تفعيل_التنبيه \ n **تـم تفعيـل التنبيـه ، مـع عـدم ذكر السبب**",
            )


CMD_HELP.update(
    {
        "الرد التلقائي": """**اسم الاضافـه : **`الرد التلقائي`
__الرد التلقائي والمنبه الخاص بسورس زد ثــون__

•  **╮•❐ الامـر ⦂ **`.منبه + سبب اختياري`
•  **الشـرح •• **__يجيب لك تنبيـه والرد على أي شخص يقوم بعمل تاك لك تخبرهم أنك في حالة نوم او غير موجود (السبب) مع الوسائط التي قمت بالرد عليها باستخدام الامـر تنبيه .__

•  **╮•❐ الامـر ⦂ **`.تنبيه + سبب اختياري`
•  **الشـرح •• **__ يقـوم بتنبيهـك ويرد على أي شخص يقوم بعمل تاك لك تخبرهم أنك نائـم او غير موجـود (السبب) .__

• ** ملاحظـه : ** إذا كنت تريد امـر النوم مع استخدام الفاصلـه [ ؛ ] بعد السبب ، قم بلصق رابط الوسائط.
• ** مثال : ** `.تنبيه مشغول الآن ؛ رابـط الميديا `

• ** ملاحظة: ** __إيقاف تشغيل التنبيه عند إعادة كتابة أي شيء في أي مكان. يمكنك استخدام #تنبيه في الرساله للمتابعة في التنبيه دون ايقافـها __ \
        """
    }
)
