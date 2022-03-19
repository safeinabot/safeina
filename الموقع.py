#safeina1

from geopy.geocoders import Nominatim
from telethon.tl import types

from userbot import CMD_HELP
from userbot.utils import sudo_cmd


@bot.on(admin_cmd(pattern="الموقع ?(.*)"))
async def gps(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    input_str = event.pattern_match.group(1)

    if not input_str:
        return await event.edit("what should i find give me location.")

    await event.edit("**جـارِ**")

    geolocator = Nominatim(user_agent="catuserbot")
    geoloc = geolocator.geocode(input_str)

    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await reply_to_id.reply(
            input_str, file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon))
        )
        await event.delete()
    else:
        await event.edit("i coudn't find it")


@bot.on(sudo_cmd(pattern="الموقع ?(.*)", allow_sudo=True))
async def gps(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    input_str = event.pattern_match.group(1)

    if not input_str:
        return await event.reply("what should I find give me location.")

    cat = await event.reply("**جـارِ**")

    geolocator = Nominatim(user_agent="catuserbot")
    geoloc = geolocator.geocode(input_str)

    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await reply_to_id.reply(
            input_str, file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon))
        )
        await cat.delete()
    else:
        await cat.edit("i coudn't find it")


CMD_HELP.update(
    {
        "الموقع": "**اسم الاضافـه :** `خرائط جوجل لتصوير المواقع`\
         \n\n**  ╮•❐ الامـر ⦂ **`.الموقع` + اسم الموقع`\
         \n**  • الشـرح •• **يقـوم بالبحـث علـى الموقـع المحـدد واعطـاء خريطـه للموقـع\
      "
    }
)
