import platform
import sys
from datetime import datetime

import psutil
from telethon import __version__

from . import ALIVE_NAME

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "safeina"
# ============================================


@bot.on(admin_cmd(outgoing=True, pattern=r"النظام$"))
@bot.on(sudo_cmd(allow_sudo=True, pattern=r"النظام$"))
async def psu(event):
    uname = platform.uname()
    softw = "** 𓆩 𝑺𝑶𝑼𝑹𝑪𝑬 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢 𓆪 **\n"
    softw += f"** ⌔∮ النظام :↬ ** `{uname.system}`\n"
    softw += f"** ⌔∮ المرجع  :↬ ** `{uname.release}`\n"
    softw += f"** ⌔∮ الاصدار  :↬ ** `{uname.version}`\n"
    softw += f"** ⌔∮ النـوع  :↬ ** `{uname.machine}`\n"
    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"** ⌔∮ تاريـخ التنصيب:↬ ** `{bt.day}/{bt.month}/{bt.year}  {bt.hour}:{bt.minute}:{bt.second}`\n"
    # CPU Cores
    cpuu = "**- معلومات المعالـج**\n"
    cpuu += "**⌔∮ الماديـه   :** `" + str(psutil.cpu_count(logical=False)) + "`\n"
    cpuu += "**⌔∮ الكليـه      :** `" + str(psutil.cpu_count(logical=True)) + "`\n"
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    cpuu += f"** ⌔∮ اعلـى تـردد    :↬ ** `{cpufreq.max:.2f}Mhz`\n"
    cpuu += f"** ⌔∮ اقـل تـردد    :↬ ** `{cpufreq.min:.2f}Mhz`\n"
    cpuu += f"** ⌔∮ التـردد القياسـي:↬ ** `{cpufreq.current:.2f}Mhz`\n\n"
    # CPU usage
    cpuu += "**- استخدامات المعالج لكل وحده**\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpuu += f"** ⌔∮ كـور {i}  :↬ ** `{percentage}%`\n"
    cpuu += "**- Total CPU Usage**\n"
    cpuu += f"** ⌔∮ الكـليه:↬ ** `{psutil.cpu_percent()}%`\n"
    # RAM Usage
    svmem = psutil.virtual_memory()
    memm = "**- استخدامـات الذاكـره**\n"
    memm += f"** ⌔∮ الكـليه     :↬ ** `{get_size(svmem.total)}`\n"
    memm += f"** ⌔∮ الفعليـه :↬ ** `{get_size(svmem.available)}`\n"
    memm += f"** ⌔∮ المستخدمـه      :↬ ** `{get_size(svmem.used)}`\n"
    memm += f"** ⌔∮ المتاحـه:↬ ** `{svmem.percent}%`\n"
    # Bandwidth Usage
    bw = "**- استخدامات الباندويـدث**\n"
    bw += f"** ⌔∮ الرفـع  :↬ ** `{get_size(psutil.net_io_counters().bytes_sent)}`\n"
    bw += f"** ⌔∮ التحميـل :↬ ** `{get_size(psutil.net_io_counters().bytes_recv)}`\n"
    help_string = f"{str(softw)}\n"
    help_string += f"{str(cpuu)}\n"
    help_string += f"{str(memm)}\n"
    help_string += f"{str(bw)}\n"
    help_string += "**Engine Info**\n"
    help_string += f"** ⌔∮ بايثـون ↬ ** `{sys.version}`\n"
    help_string += f"** ⌔∮ تيليثـون ↬ ** `{__version__}`"
    await event.edit(help_string)


def get_size(inputbytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if inputbytes < factor:
            return f"{inputbytes:.2f}{unit}{suffix}"
        inputbytes /= factor


@bot.on(admin_cmd(pattern="cpu$"))
@bot.on(sudo_cmd(pattern="cpu$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    cmd = "ics /proc/cpuinfo | grep 'model name'"
    o = (await _icssutils.runcmd(cmd))[0]
    await edit_or_reply(
        event, f"**[- zed’s](tg://need_update_for_some_feature/) CPU Model:**\n{o}"
    )


@bot.on(admin_cmd(pattern=f"sysd$", outgoing=True))
@bot.on(sudo_cmd(pattern=f"sysd$", allow_sudo=True))
async def sysdetails(sysd):
    cmd = "git clone https://github.com/dylanaraps/neofetch.git"
    await _catutils.runcmd(cmd)
    neo = "neofetch/neofetch --off --color_blocks off --bold off --cpu_temp C \
                    --cpu_speed on --cpu_cores physical --kernel_shorthand off --stdout"
    a, b, c, d = await _catutils.runcmd(neo)
    result = str(a) + str(b)
    await edit_or_reply(sysd, "Neofetch Result: `" + result + "`")


CMD_HELP.update(
    {
        "النظام": "**Plugin : **`النظام`\
        \n\n**Syntax : **`.النظام`\
        \n**Function : **__Show system specification.__\
        \n\n**Syntax : **`.sysd`\
        \n**Function : **__Shows system information using neofetch.__\
        \n\n**Syntax : **`.cpu`\
        \n**Function : **__shows the cpu information__\
    "
    }
)
