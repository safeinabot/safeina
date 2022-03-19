# 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢

import time

from . import StartTime, mention
from . import get_readable_time as grt

@bot.on(
    admin_cmd(
       pattern="مده", outgoing=True
    )
)
@bot.on(
    sudo_cmd(
       pattern="مده", allow_sudo=True
    )
)
async def tim(lon):
    icst = await grt((time.time() - StartTime))
    await eor(
        lon, f"⌔∮ مستخدم البوت : \n  - {mention} \n⌔∮ مدة تشغيل البوت : \n  - {icst}"
    )
