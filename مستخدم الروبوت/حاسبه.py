"""
SOURCE Safeina
@safeina1
"""

import io
import sys
import traceback
from . import Calc, C

@bot.on(
    admin_cmd(pattern="حاسبه (.*)")
)
@bot.on(sudo_cmd(
               pattern="حاسبه (.*)", 
               allow_sudo=True)
           )
async def _(ics):
    tosh = ics.text.split(" ", maxsplit=1)[1]
    event = await eor(ics, "**⌔∮ جاري الحل… **")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    kim = "print(%s)"% tosh
    try:
        await aexec(kim, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "اسف لايمكنني حلها"
    final_output = (C.format(tosh, evaluation))
    await event.edit(final_output)


async def aexec(code, event):
    exec(f"async def __aexec(event): " + "".join(f"\n {l}" for l in code.split("\n")))
    return await locals()["__aexec"](event)

@bot.on(admin_cmd(pattern="م23"))
@bot.on(sudo_cmd(pattern="م23", allow_sudo=True))
async def calc(cmd):
    await eor(cmd, Calc)

CMD_HELP.update(
    {
        "حاسبه": "**Plugin : **`حاسبه`\
        \n\n**Syntax : **`.حاسبه expression` \
        \n**Function : **solves the given maths equation by BODMAS rule. "
    }
)
