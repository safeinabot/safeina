alv = (
"""
**𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢 - @safeina1
  - Plugin Alive** 
  - **Commend:** `.السورس`
  - **Function:** لعرض معلومات السورس
"""
)

import time
from platform import python_version
from telethon import version
from resources.strings import *

from . import ALIVE_NAME, StartTime, get_readable_time, icsv, mention
from . import reply_id as rd

DEFAULTUSER = ALIVE_NAME or "safeina "
safeina_MED = Config.safeina_MEDIA or "https://telegra.ph/file/d46ae74ee596000f78715.jpg"
safeina_IMG = Config.ALIVE_PIC or "https://telegra.ph/file/d46ae74ee596000f78715.jpg"
safeina_TEXT = Config.CUSTOM_ALIVE_TEXT or "𓆩 𝑾𝑬𝑳𝑪𝑶𝑴𝑬 𝑻𝑶 𝑺𝑶𝑼𝑹𝑪𝑬 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢 𓆪"
ZEEM = Config.CUSTOM_ALIVE_EMOJI or "  ⌔∮ "


@bot.on(admin_cmd(outgoing=True, pattern="السورس$"))
@bot.on(sudo_cmd(pattern="السورس$", allow_sudo=True))
async def ica(safeina):
    if safeina.fwd_from:
        return
    ze_id = await rd(safeina)
    zeupt = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    if safeina_IMG:
        ze_c = f"**{safeina_TEXT}**\n"
        ze_c += f"𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻 \n"
        ze_c += f"**{ZEEM} قاعدة البيانات ↫** `{check_sgnirts}`\n"
        ze_c += f"**{ZEEM} اصدار التليثون  ↫** `{version.__version__}\n`"
        ze_c += f"**{ZEEM} اصدار زد ثـون ↫** `{icsv}`\n"
        ze_c += f"**{ZEEM} اصدار البايثون ↫** `{python_version()}\n`"
        #        ze_c += f"**{ZEEM} مدة التشغيل ↫** `{zeupt}\n`"
        ze_c += f"**{ZEEM} المستخدم ↫** {mention}\n"
        ze_c += f"**{ZEEM} **  **[قـنـاة الـسـورس]**(https://t.me/safeina1) .\n"
        ze_c += f"𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻\n"
        await safeina.client.send_file(
            safeina.chat_id, safeina_IMG, caption=ze_c, reply_to=ze_id
        )
        await safeina.delete()
    else:
        await eor(
            safeina,
            f"**{safeina_TEXT}**\n\n"
            f"**{ZEEM} قاعدة البيانات ↫**  `{check_sgnirts}`\n"
            f"**{ZEEM} اصدار التليثون  ↫** `{version.__version__}\n`"
            f"**{ZEEM} اصدار زد ثـون ↫** `{icsv}`\n"
            f"**{ZEEM} اصدار البايثون  ↫** `{python_version()}\n`"
            f"**{ZEEM} مدة التشغيل ↫** `{zeupt}\n`"
            f"**{ZEEM} المستخدم ↫** {mention}\n",
        )


def check_data_base_heal_th():
    is_database_working = False
    output = "لم يتم تعيين قاعدة بيانات"
    if not Config.DB_URI:
        return is_database_working, output
    from userbot.plugins.sql_helper import SESSION

    try:
        SESSION.execute("SELECT 1")
    except Exception as e:
        output = f"❌ {str(e)}"
        is_database_working = False
    else:
        output = "تعمل بنجاح"
        is_database_working = True
    return is_database_working, output


@bot.on(admin_cmd(outgoing=True, pattern="فحص$"))
@bot.on(sudo_cmd(pattern="فحص$", allow_sudo=True))
async def ica(safeina):
    if safeina.fwd_from:
        return
    ze_id = await rd(safeina)
    zeupt = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    if safeina_MED:
        ze_c = f"**{safeina_TEXT}**\n"
        ze_c += f"𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻 \n"
        ze_c += f"**{ZEEM} قاعدة البيانات ↫** `{check_sgnirts}`\n"
        ze_c += f"**{ZEEM} اصدار التليثون  ↫** `{version.__version__}\n`"
        ze_c += f"**{ZEEM} اصدار زد ثـون ↫** `{icsv}`\n"
        ze_c += f"**{ZEEM} اصدار البايثون ↫** `{python_version()}\n`"
        #        ze_c += f"**{ZEEM} مدة التشغيل ↫** `{zeupt}\n`"
        ze_c += f"**{ZEEM} المستخدم ↫** {mention}\n"
        ze_c += f"**{ZEEM} **  **[قـنـاة الـسـورس]**(https://t.me/safeina1) .\n"
        ze_c += f"𓍹ⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧⵧ𓍻\n"
        await safeina.client.send_file(
            safeina.chat_id, safeina_MED, caption=ze_c, reply_to=ze_id
        )
        await safeina.delete()
    else:
        await eor(
            safeina,
            f"**{safeina_TEXT}**\n\n"
            f"**{ZEEM} قاعدة البيانات ↫**  `{check_sgnirts}`\n"
            f"**{ZEEM} اصدار التليثون  ↫** `{version.__version__}\n`"
            f"**{ZEEM} اصدار زد ثـون ↫** `{icsv}`\n"
            f"**{ZEEM} اصدار البايثون  ↫** `{python_version()}\n`"
            f"**{ZEEM} مدة التشغيل ↫** `{zeupt}\n`"
            f"**{ZEEM} المستخدم ↫** {mention}\n",
        )


def check_data_base_heal_th():
    is_database_working = False
    output = "لم يتم تعيين قاعدة بيانات"
    if not Config.DB_URI:
        return is_database_working, output
    from userbot.plugins.sql_helper import SESSION

    try:
        SESSION.execute("SELECT 1")
    except Exception as e:
        output = f"❌ {str(e)}"
        is_database_working = False
    else:
        output = "تعمل بنجاح"
        is_database_working = True
    return is_database_working, output


CMD_HELP.update({"alive": f"{alv}"})
