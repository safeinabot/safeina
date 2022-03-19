from userbot.Config import Config
from userbot import bot 

O = Config.OWNER_ID
Name = bot.me.first_name
M = f"[{Name}](tg://user?id={O})"

A = "https://t.me/safeina1/105"

B = "**⌔∮ اهلا عزيزي - {} \n⌔∮ رابط التنصيب - [اضغط هنا]({})**"

@bot.on(admin_cmd(pattern="رابط التنصيب"))
async def _(e):
    await eor(e, B.format(M, A))
