#safeina

from datetime import datetime

@bot.on(
    admin_cmd(pattern="حساب العمر")
)
async def _(e):
    zelt = e.txt
    yar = zelt[4:5]
    if not yar:
       yar = "2"
    YearNow = datetime.now().year
    MyAge = YearNow - yar
    await eor(e, "عمرك هوه {}".format(MyAge))
