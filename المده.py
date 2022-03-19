"""
©safeina : @safeina1
  - Safeina UpTime
  - Commend: .المده
"""

import time

from . import ALIVE_NAME, StartTime, get_readable_time, mention, reply_id

DEFULTUSER = ALIVE_NAME or "Safeina1bot"
ZED_IMG = https://telegra.ph/file/d46ae74ee596000f78715.jpg"
Safeina_TEXT = "𓆩 𝑾𝑬𝑳𝑪𝑶𝑴𝑬 𝑻𝑶 𝑺𝑶𝑼𝑹𝑪𝑬 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢 𓆪"
safeina EM = "**⌔∮**"


@bot.on(admin_cmd(outgoing=True, pattern="المده$"))
@bot.on(sudo_cmd(pattern="المده$", allow_sudo=True))
async def uptsafeina(safeina):
    if zed.fwd_from:
        return
    safinaid = await reply_id(safeina)
    safeinaupt = await get_readable_time((time.time() - StartTime))
    if safeina_IMG:
        safeina_c = f"**{safeina_TEXT}**\n"
        safeina_c += f"**{safeina EM} المستخدم :** {mention}\n"
        safeina_c += f"**{safeinaEM} مدة التشغيل :** `{zedupt}`"
        await safeina.client.send_file(safeina.chat_id, Safeina_IMG, caption=safeina_c, reply_to=safeinaid)
        await safeina.delete()
    else:
        await edit_or_reply(
            safeina,
            f"**{SAFEINA_TEXT}**\n\n"
            f"**{SAFEINAEM} المستخدم :** {mention}\n"
            f"**{SAFEINAEM} مدة التشغيل :** `{safeinaupt}`",
        )
