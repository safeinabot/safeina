# fonts for safeina edit by: @S_F_M_L

import random

from . import fonts


@bot.on(admin_cmd(pattern="زغرفه10(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="زغرفه10(?: |$)(.*)", allow_sudo=True))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            egyptfontcharacter = fonts.egyptfontfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, egyptfontcharacter)
    await edit_or_reply(event, string)


@bot.on(admin_cmd(pattern="زغرفه11(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="زغرفه11(?: |$)(.*)", allow_sudo=True))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            nightmarecharacter = fonts.nightmarefont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, nightmarecharacter)
    await edit_or_reply(event, string)


@bot.on(admin_cmd(pattern="زغرفه12(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="زغرفه12(?: |$)(.*)", allow_sudo=True))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            hwcapitalcharacter = fonts.hwcapitalfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, hwcapitalcharacter)
    await edit_or_reply(event, string)


@bot.on(admin_cmd(pattern="زغرفه13(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="زغرفه13(?: |$)(.*)", allow_sudo=True))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            doubletextcharacter = fonts.doubletextfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, doubletextcharacter)
    await edit_or_reply(event, string)


@bot.on(admin_cmd(pattern="زغرفه14(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="زغرفه14(?: |$)(.*)", allow_sudo=True))
async def spongemocktext(mock):
    reply_text = []
    textx = await mock.get_reply_message()
    message = mock.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await edit_or_reply(mock, "`gIvE sOMEtHInG tO MoCk!`")
        return

    for charac in message:
        if charac.isalpha() and random.randint(0, 1):
            to_app = charac.upper() if charac.islower() else charac.lower()
            reply_text.append(to_app)
        else:
            reply_text.append(charac)

    await edit_or_reply(mock, "".join(reply_text))


@bot.on(admin_cmd(pattern="زغرفه15(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="زغرفه15(?: |$)(.*)", allow_sudo=True))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            ghostfontcharacter = fonts.ghostfontfont[
                fonts.normaltext.index(normaltextcharacter)
            ]
            string = string.replace(normaltextcharacter, ghostfontcharacter)
    await edit_or_reply(event, string)


@bot.on(admin_cmd(pattern="زغرفه16(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="زغرفه16(?: |$)(.*)", allow_sudo=True))
async def stylish_generator(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(event, "What I am Supposed to change give text")
        return
    string = "  ".join(args).lower()
    for normaltextcharacter in string:
        if normaltextcharacter in fonts.normaltext:
            hwslcharacter = fonts.hwslfont[fonts.normaltext.index(normaltextcharacter)]
            string = string.replace(normaltextcharacter, hwslcharacter)
    await edit_or_reply(event, string)


CMD_HELP.update(
    {
        "زغارف2": """**Plugin : **`زغارف2`
        
**Commands found in fonts2 are**
  •  `.egyptf`
  •  `.maref`
  •  `.handcf`
  •  `.doublef`
  •  `.mock`
  •  `.ghostf`
  •  `.handsf`
  
**Function : **__Reply the command to the text message or give input along with command to convert that text to given font style__"""
    }
)
