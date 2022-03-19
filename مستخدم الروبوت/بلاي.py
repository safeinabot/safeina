from . import R

@bot.on(admin_cmd(pattern="بلاي$"))
@bot.on(sudo_cmd(pattern="بلاي$", allow_sudo=True))
async def zedrepo(zelp):
    await eor(zelp, R)
