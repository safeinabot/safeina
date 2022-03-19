#    Safeina - Userbot
#    Owner - @S_F_M_L

from telethon import events, Button
from ..Config import Config
from . import TOSH, K, mention


@asst_cmd("/repo|#repo")
async def dev(zelzal):
    await zelzal.reply(
        "⌔∮ 𝙎𝙊𝙐𝙍𝘾𝙀 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢 - 𝙍𝙀𝙋𝙊 𓆪",
        buttons=[[Button.url("🔗 𝙍𝙀𝙋𝙊 🔗", K)]]
    )
   

TOSH_PIC = Config.ALIVE_PIC if Config.ALIVE_PIC else "https://telegra.ph/file/4c406eb5e6932d4834947.jpg"

if Config.TG_BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        me = await bot.get_me()
        if query.startswith("بوت") and event.query.user_id == bot.uid:
            buttons = [
                [
                    Button.url("قنـاة السـورس ⚙️", "https://t.me/safeina1"),
                    Button.url("المطـور 👨🏻‍💻", "https://t.me/S_F_M_L"),
                ]
            ]
            if TOSH_PIC and TOSH_PIC.endswith((".jpg", ".png", "gif", "mp4")):
                result = builder.photo(
                    TOSH_PIC,
                    text=TOSH,
                    buttons=buttons,
                    link_preview=False
                )
            elif TOSH_PIC:
                result = builder.document(
                    TOSH_PIC,
                    title="safeina- USERBOT",
                    text=TOSH,
                    buttons=buttons,
                    link_preview=False,
                )
            else:
                result = builder.article(
                    title="safeina- USERBOT",
                    text=TOSH,
                    buttons=buttons,
                    link_preview=False,
                )
            await event.answer([result] if result else None)

@bot.on(admin_cmd(outgoing=True, pattern="بوت"))
async def repo(event):
    if event.fwd_from:
        return
    KIM = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(KIM, "بوت")
    await response[0].click(event.chat_id)
    await event.delete()

