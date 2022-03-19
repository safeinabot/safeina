#𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢
from userbot.Config import Config
import asyncio

import requests
from telethon import functions
from . import *
from . import ALIVE_NAME


import requests
from telethon import functions
from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot, BotInlineDisabledError as noinline, YouBlockedUserError

botname = Config.TG_BOT_USERNAME

@bot.on(admin_cmd(pattern="انلاين تفعيل ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="انلاين تفعيل ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    tgbotusername = Config.TG_BOT_USERNAME
    chat = "@Botfather"
    if tgbotusername is not None:
        try:
            results = await event.client.inline_query(tgbotusername, "safeina")
            await results[0].click(
                event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
            )
            await event.delete()
        except:
            zelzal = await eor(event, "**❈╎جـارِ الاتصـال ببـوت فـاذر ...⏣**\n**❈╎تـم تفعيـل انـلاين بـوتك .. بنجـاح ☑️**\n\n**❈╎جـاري اعـادة تشغيل البـوت الرجـاء الانتظـار  ▬▭...𓅫**")
            async with bot.conversation(chat) as conv:
                try:
                    first = await conv.send_message("/setinline")
                    second = await conv.get_response()
                    third = await conv.send_message(tgbotusername)
                    fourth = await conv.get_response()
                    fifth = await conv.send_message("safeina1")
                    sixth = await conv.get_response()
                    seventh = await conv.send_message(perf)
                    eighth = await conv.get_response()
                    await bot.send_read_acknowledge(conv.chat_id)
                except YouBlockedUserError:
                    return await zelzal.edit("**❈╎قـم بإلغـاء الحظـر عـن بـوت فـاذر اولا @Botfather .. ثـم اعـد المحـاوله**")
                await bot.edit(f"**❈╎تـم تفعيـل انـلاين بـوتك .. بنجـاح ☑️**")
            await bot.delete_messages(
                conv.chat_id, [first.id, second.id, third.id, fourth.id, fifth.id, sixth.id]
            )
    else:
        await eor(event, "**❈╎هنـالك خطـأ!!⚠️**\n**❈╎الـرجاء التحـقق مـن فـارات TG_BOT_TOKEN & TG_BOT_USERNAME عـلى هيـروكـو ...⏣**")


@bot.on(admin_cmd(pattern="انلاين تعطيل ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="انلاين تعطيل ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    tgbotusername = Config.TG_BOT_USERNAME
    chat = "@Botfather"
    if tgbotusername is not None:
        try:
            results = await event.client.inline_query(tgbotusername, "Zelzal_Ahmed")
            await results[0].click(
                event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
            )
            await event.delete()
        except:
            zelzal = await eor(event, "**❈╎جـارِ الاتصـال ببـوت فـاذر ...⏣**\n**❈╎تـم تعطيـل انـلاين بـوتك .. بنجـاح ☑️**\n\n**❈╎جـاري اعـادة تشغيل البـوت الرجـاء الانتظـار  ▬▭...𓅫**")
            async with bot.conversation(chat) as conv:
                try:
                    first = await conv.send_message("/setinline")
                    second = await conv.get_response()
                    third = await conv.send_message(tgbotusername)
                    fourth = await conv.get_response()
                    fifth = await conv.send_message("/empty")
                    sixth = await conv.get_response()
                    seventh = await conv.send_message(perf)
                    eighth = await conv.get_response()
                    await bot.send_read_acknowledge(conv.chat_id)
                except YouBlockedUserError:
                    return await zelzal.edit("**❈╎قـم بإلغـاء الحظـر عـن بـوت فـاذر اولا @Botfather .. ثـم اعـد المحـاوله**")
                await bot.edit(f"**❈╎تـم تعطيـل انـلاين بـوتك .. بنجـاح ☑️**")
            await bot.delete_messages(
                conv.chat_id, [first.id, second.id, third.id, fourth.id, fifth.id, sixth.id]
            )
    else:
        await eor(event, "**❈╎هنـالك خطـأ!!⚠️**\n**❈╎الـرجاء التحـقق مـن فـارات TG_BOT_TOKEN & TG_BOT_USERNAME عـلى هيـروكـو ...⏣**")



@bot.on(admin_cmd(pattern="تعيين نبذة البوت ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="تعيين نبذة البوت ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    tgbotusername = Config.TG_BOT_USERNAME
    chat = "@Botfather"
    if tgbotusername is not None:
        try:
            results = await event.client.inline_query(tgbotusername, "Zelzal_Ahmed")
            await results[0].click(
                event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
            )
            await event.delete()
        except:
            zelzal = await eor(event, "**❈╎جـارِ الاتصـال ببـوت فـاذر ...⏣**\n**❈╎ارسـل الامـر التـالي لـوضع النبذة ☑️**\n\n**❈╎.وضع نبذة + نبذتـك ...𓅫**")
            async with bot.conversation(chat) as conv:
                try:
                    first = await conv.send_message("/setabouttext")
                    second = await conv.get_response()
                    third = await conv.send_message(tgbotusername)
                    fourth = await conv.get_response()
                    fifth = await conv.send_message(perf)
                    sixth = await conv.get_response()
                    await bot.send_read_acknowledge(conv.chat_id)
                except YouBlockedUserError:
                    return await zelzal.edit("**❈╎قـم بإلغـاء الحظـر عـن بـوت فـاذر اولا @Botfather .. ثـم اعـد المحـاوله**")
                await bot.edit(f"**❈╎تـم تفعيـل نبـذة بـوتك .. بنجـاح ☑️**")
            await bot.delete_messages(
                conv.chat_id, [first.id, second.id, third.id, fourth.id, fifth.id, sixth.id]
            )
    else:
        await eor(event, "**❈╎هنـالك خطـأ!!⚠️**\n**❈╎الـرجاء التحـقق مـن فـارات TG_BOT_TOKEN & TG_BOT_USERNAME عـلى هيـروكـو ...⏣**")


@bot.on(admin_cmd(pattern="تعيين وصف البوت ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="تعيين وصف البوت ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    tgbotusername = Config.TG_BOT_USERNAME
    chat = "@Botfather"
    if tgbotusername is not None:
        try:
            results = await event.client.inline_query(tgbotusername, "Zelzal_Ahmed")
            await results[0].click(
                event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
            )
            await event.delete()
        except:
            zelzal = await eor(event, "**❈╎جـارِ الاتصـال ببـوت فـاذر ...⏣**\n**❈╎ارسـل الامـر التـالي لـوضع الوصف ☑️**\n\n**❈╎.وضع وصف + وصفـك ...𓅫**")
            async with bot.conversation(chat) as conv:
                try:
                    first = await conv.send_message("/setdescription")
                    second = await conv.get_response()
                    third = await conv.send_message(tgbotusername)
                    fourth = await conv.get_response()
                    fifth = await conv.send_message(perf)
                    sixth = await conv.get_response()
                    await bot.send_read_acknowledge(conv.chat_id)
                except YouBlockedUserError:
                    return await zelzal.edit("**❈╎قـم بإلغـاء الحظـر عـن بـوت فـاذر اولا @Botfather .. ثـم اعـد المحـاوله**")
                await bot.edit(f"**❈╎تـم تفعيـل وصـف بـوتك .. بنجـاح ☑️**")
            await bot.delete_messages(
                conv.chat_id, [first.id, second.id, third.id, fourth.id, fifth.id, sixth.id]
            )
    else:
        await eor(event, "**❈╎هنـالك خطـأ!!⚠️**\n**❈╎الـرجاء التحـقق مـن فـارات TG_BOT_TOKEN & TG_BOT_USERNAME عـلى هيـروكـو ...⏣**")


@bot.on(admin_cmd(pattern="تعيين اسم البوت ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="تعيين اسم البوت ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    tgbotusername = Config.TG_BOT_USERNAME
    chat = "@Botfather"
    if tgbotusername is not None:
        try:
            results = await event.client.inline_query(tgbotusername, "Zelzal_Ahmed")
            await results[0].click(
                event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
            )
            await event.delete()
        except:
            zelzal = await eor(event, "**❈╎جـارِ الاتصـال ببـوت فـاذر ...⏣**\n**❈╎ارسـل الامـر التـالي لـوضع الاسم ☑️**\n\n**❈╎.وضع اسم + اسـم البـوت ...𓅫**")
            async with bot.conversation(chat) as conv:
                try:
                    first = await conv.send_message("/setname")
                    second = await conv.get_response()
                    third = await conv.send_message(tgbotusername)
                    fourth = await conv.get_response()
                    fifth = await conv.send_message(perf)
                    sixth = await conv.get_response()
                    await bot.send_read_acknowledge(conv.chat_id)
                except YouBlockedUserError:
                    return await zelzal.edit("**❈╎قـم بإلغـاء الحظـر عـن بـوت فـاذر اولا @Botfather .. ثـم اعـد المحـاوله**")
                await bot.edit(f"**❈╎تـم تفعيـل اسـم بـوتك .. بنجـاح ☑️**")
            await bot.delete_messages(
                conv.chat_id, [first.id, second.id, third.id, fourth.id, fifth.id, sixth.id]
            )
    else:
        await eor(event, "**❈╎هنـالك خطـأ!!⚠️**\n**❈╎الـرجاء التحـقق مـن فـارات TG_BOT_TOKEN & TG_BOT_USERNAME عـلى هيـروكـو ...⏣**")


@bot.on(admin_cmd(pattern="تعيين صورة البوت ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="تعيين صورة البوت ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    tgbotusername = Config.TG_BOT_USERNAME
    chat = "@Botfather"
    if tgbotusername is not None:
        try:
            results = await event.client.inline_query(tgbotusername, "Zelzal_Ahmed")
            await results[0].click(
                event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
            )
            await event.delete()
        except:
            zelzal = await eor(event, "**❈╎جـارِ الاتصـال ببـوت فـاذر ...⏣**\n**❈╎ارسـل الامـر التـالي لـوضع الصورة ☑️**\n\n**❈╎.وضع صورة بالـرد عـلى صـورة ...𓅫**")
            async with bot.conversation(chat) as conv:
                try:
                    first = await conv.send_message("/setuserpic")
                    second = await conv.get_response()
                    third = await conv.send_message(tgbotusername)
                    fourth = await conv.get_response()
                    fifth = await conv.send_message(perf)
                    sixth = await conv.get_response()
                    await bot.send_read_acknowledge(conv.chat_id)
                except YouBlockedUserError:
                    return await zelzal.edit("**❈╎قـم بإلغـاء الحظـر عـن بـوت فـاذر اولا @Botfather .. ثـم اعـد المحـاوله**")
                await bot.edit(f"**❈╎تـم تفعيـل صـورة بـوتك .. بنجـاح ☑️**")
            await bot.delete_messages(
                conv.chat_id, [first.id, second.id, third.id, fourth.id, fifth.id, sixth.id]
            )
    else:
        await eor(event, "**❈╎هنـالك خطـأ!!⚠️**\n**❈╎الـرجاء التحـقق مـن فـارات TG_BOT_TOKEN & TG_BOT_USERNAME عـلى هيـروكـو ...⏣**")



#𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from PIL import Image
from userbot.utils import sudo_cmd

from . import reply_id


@bot.on(admin_cmd(pattern="وضع نبذة ?(.*)"))
@bot.on(sudo_cmd(pattern="وضع نبذة ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    if event.reply_to_msg_id and not event.pattern_match.group(1):
        reply_to_id = await event.get_reply_message()
        reply_to_id = str(reply_to_id.message)
    else:
        reply_to_id = str(event.pattern_match.group(1))
    if not reply_to_id:
        return await edit_or_reply(
            event, "**╮ لتغييـر نبـذة بوتـك المسـاعد بدون الذهاب لبوت فـاذر ارسـل .وضع نبذة + النبذة ...𓅫╰**"
        )
    chat = "@Botfather"
    catevent = await edit_or_reply(event, "**╮•⎚ جـارِ الاتصـال ببـوت فـاذر لوضـع النبـذة لـ بوتـك ... 🧸🎈**")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=93372553)
            )
            await event.client.send_message(chat, "{}".format(input_str))
            response = await response
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("**╮•⎚ تحـقق من انـك لم تقـم بحظر البوت @Botfather .. ثم اعـد استخدام الامـر ...🤖♥️**")
            return
        if response.text.startswith("I can't find that"):
            await catevent.edit("**╮•⎚ عـذراً .. لـم استطـع ايجـاد المطلـوب ☹️💔**")
        else:
            await catevent.delete()
            await event.client.send_message(event.chat_id, response.message)


@bot.on(admin_cmd(pattern="وضع وصف ?(.*)"))
@bot.on(sudo_cmd(pattern="وضع وصف ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    if event.reply_to_msg_id and not event.pattern_match.group(1):
        reply_to_id = await event.get_reply_message()
        reply_to_id = str(reply_to_id.message)
    else:
        reply_to_id = str(event.pattern_match.group(1))
    if not reply_to_id:
        return await edit_or_reply(
            event, "**╮ لتغييـر وصـف بوتـك المسـاعد بدون الذهاب لبوت فـاذر ارسـل .وضع وصف + الوصف ...𓅫╰**"
        )
    chat = "@Botfather"
    catevent = await edit_or_reply(event, "**╮•⎚ جـارِ الاتصـال ببـوت فـاذر لوضـع الوصـف لـ بوتـك ... 🧸🎈**")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=93372553)
            )
            await event.client.send_message(chat, "{}".format(input_str))
            response = await response
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("**╮•⎚ تحـقق من انـك لم تقـم بحظر البوت @Botfather .. ثم اعـد استخدام الامـر ...🤖♥️**")
            return
        if response.text.startswith("I can't find that"):
            await catevent.edit("**╮•⎚ عـذراً .. لـم استطـع ايجـاد المطلـوب ☹️💔**")
        else:
            await catevent.delete()
            await event.client.send_message(event.chat_id, response.message)


@bot.on(admin_cmd(pattern="وضع اسم ?(.*)"))
@bot.on(sudo_cmd(pattern="وضع اسم ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    if event.reply_to_msg_id and not event.pattern_match.group(1):
        reply_to_id = await event.get_reply_message()
        reply_to_id = str(reply_to_id.message)
    else:
        reply_to_id = str(event.pattern_match.group(1))
    if not reply_to_id:
        return await edit_or_reply(
            event, "**╮ لتغييـر اسـم بوتـك المسـاعد بدون الذهاب لبوت فـاذر ارسـل .وضع اسم + اسم البـوت ...🎟𓅫╰**"
        )
    chat = "@Botfather"
    catevent = await edit_or_reply(event, "**╮•⎚ جـارِ الاتصـال ببـوت فـاذر لوضـع الاسـم لـ بوتـك ... 🧸🎈**")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=93372553)
            )
            await event.client.send_message(chat, "{}".format(input_str))
            response = await response
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("**╮•⎚ تحـقق من انـك لم تقـم بحظر البوت @Botfather .. ثم اعـد استخدام الامـر ...🤖♥️**")
            return
        if response.text.startswith("I can't find that"):
            await catevent.edit("**╮•⎚ عـذراً .. لـم استطـع ايجـاد المطلـوب ☹️💔**")
        else:
            await catevent.delete()
            await event.client.send_message(event.chat_id, response.message)


@bot.on(admin_cmd(pattern="وضع صورة$", outgoing=True))
@bot.on(sudo_cmd(pattern="وضع صورة$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    if not reply_message:
        await edit_or_reply(event, "**╮ .وضع صورة بالـرد ﮼؏ الـٓصـورھہ لوضعـها بـروفايـل بـوتك المسـاعـد ...🎆𓅫╰**")
        return
    chat = "@Botfather"
    catevent = await edit_or_reply(event, "**╮•⎚ جـارِ الاتصـال ببـوت فـاذر لوضـع بروفـايل لـ بوتـك ... 🎆🎈**")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=93372553)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit(
                "**╮•⎚ تحـقق من انـك لم تقـم بحظر البوت @Botfather .. ثم اعـد استخدام الامـر ...🤖♥️**"
            )
            return
        if response.text.startswith(""):
            await catevent.edit("**🤨💔...؟**")
        else:
            await catevent.delete()
            await event.client.send_message(event.chat_id, response.message)



CMD_HELP.update(
    {
        "بوت فاذر": """**اسـم الاضـافـه : **`بوت فاذر`
        
**╮•❐ اوامـر تعيين وتفعيل بوت فـاذر لبـوتك بسـهولـة بـدون الذهـاب لبـوت فـاذر ⦂ **


  •  `.انلاين تفعيل`

  •  `.انلاين تعطيل`
  
  •  `.تعيين اسم البوت`
  
  •  `.تعيين نبذة البوت`
  
  •  `.تعيين وصف البوت`
  
  •  `.تعيين صورة البوت`


**للنســخ : ** __اضغط ع الامـر لنسخـه__"""
    }
)
