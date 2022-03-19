from telethon.errors import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelPublicGroupNaError,
)
from telethon.tl import functions
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest

from userbot.utils import admin_cmd


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
            await event.reply("**╮ عـذراً ..﮼ لم يتم العثور ؏ المجموعة او القناة 𓅫╰**")
            return None
        except ChannelPrivateError:
            await event.reply(
                "**╮  لا يمكنني استخدام الامر ﮼؏ المجموعات او القنوات الخاصة ...𓅫╰**"
            )
            return None
        except ChannelPublicGroupNaError:
            await event.reply("**╮ عـذراً ..﮼ لم يتم العثور ؏ المجموعة او القناة 𓅫╰**")
            return None
        except (TypeError, ValueError):
            await event.reply("**╮  رابط المجموعـه غير صحيح ..𓅫╰**")
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



@bot.on(admin_cmd(pattern=r"اضافة ?(.*)"))
async def get_users(event):
    sender = await event.get_sender()
    me = await event.client.get_me()
    if not sender.id == me.id:
        eva = await event.reply("**╮  جـاري الاضـافه .. الࢪجـاء الانتظـار ...𓅫╰**")
    else:
        eva = await event.edit("**╮  جـاري الاضـافه .. الࢪجـاء الانتظـار ...𓅫╰**.")
    ZEDTHON = await get_chatinfo(event)
    chat = await event.get_chat()
    if event.is_private:
        return await eva.edit("**╮  لا استطـيع اضافـة الاعضـاء هـنا 𓅫╰**")
    s = 0
    f = 0
    error = "None"

    await eva.edit(
        "**╮  حـالة الإضافـه :**\n\n**╮  جـاري جـمع معـلومات الاعضـاء ...⏳**"
    )
    async for user in event.client.iter_participants( safina.full_chat.id):
        try:
            if error.startswith("Too"):
                return (
                    await eva.edit(
                        f"**حـالة الأضـافة انتـهت مـع الأخـطاء**\n- (**ربـما هـنالك ضغـط عـلى الأمࢪ حاول مججـدا لاحقـا 🧸**) \n**الـخطأ** : \n`{error}`\n\n• اضالـة `{s}` \n• خـطأ بأضافـة `{f}`"
                    ),
                )
            await event.client(
                functions.channels.InviteToChannelRequest(channel=chat, users=[user.id])
            )
            s = s + 1
            await eva.edit(
                f"**╮ جـاري الإضـافـه...⧑**\n\n• تـم اضافـة `{s}` \n•  خـطأ بإضافـة `{f}` \n\n**× آخـر خـطأ:** `{error}`"
            )
        except Exception as e:
            error = str(e)
            f = f + 1
    return await eva.edit(
        f"**⌔∮تـمت الإضافـه بنجـاح ✅** \n\n• تـم اضـافة `{s}` \n• خـطأ بإضافـة `{f}`"
    )


CMD_HELP.update(
    {
        "اضافة اعضاء": "**اسم الاضافـه :**`اضافة اعضاء`\
    \n\n**  ╮•❐ الامـر ⦂** `.اضف + رابط الكروب` )`\
    \n**  •  الشـرح •• **اضـافة الاعضـاء من كروب لــ كروب آخر .. تدز الامر + رابط الكروب التريد تخمط منه اعضاء وتدز الامـر بالكروب التريد تضيفله اعضـاء."
    }
)
