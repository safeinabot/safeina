import os
import re

import requests

try:
    from pyquery import PyQuery as pq
except ModuleNotFoundError:
    os.system("pip3 install pyquery")
    from pyquery import PyQuery as pq

plugin_category = "extra"


def get_download_url(link):
    post_request = requests.post(
        "https://www.expertsphp.com/download.php", data={"url": link}
    )

    request_content = post_request.content
    str_request_content = str(request_content, "utf-8")
    download_url = pq(str_request_content)("table.table-condensed")("tbody")("td")(
        "a"
    ).attr("href")
    return download_url


@bot.on(admin_cmd(pattern="ترست?(?:\s|$)([\s\S]*)"))
async def _(event):
    M = event.pattern_match.group(1)
    links = re.findall(r"\bhttps?://.*\.\S+", M)
    await event.delete()
    if not links:
        N = await event.respond("**ارسل الامـر + الرابـط ... 🧸🎈**")
        await asyncio.sleep(2)
        await N.delete()
    else:
        pass
    A = await event.respond("**╮•⎚ جـارِ التحميل ... 🧸🎈**")
    S_F_M_L= get_download_url(M)
    await event.client.send_file(event.chat.id, S_F_M_L)
    await A.delete()


CMD_HELP.update(
    {
        "بنترست": "**اسم الاضافـه :**`بنترست`\
    \n\n**  ╮•❐ الامـر ⦂** `.ترست + رابط ` )`\
    \n**  •  الشـرح •• **تحمـيل مقاطـع الفيديـو والصـور مـن موقـع بنترست عبـر الرابـط."
    }
)
