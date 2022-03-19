# reverse search and google search  plugin for safeina
import io
import os
import re
import urllib
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from PIL import Image
from search_engine_parser import GoogleSearch

from ..utils import errors_handler
from . import BOTLOG, BOTLOG_CHATID

opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
opener.addheaders = [("User-agent", useragent)]


@bot.on(admin_cmd(outgoing=True, pattern=r"جوجل (.*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern=r"جوجل (.*)"))
async def gsearch(q_event):
    catevent = await edit_or_reply(q_event, "** ⌔∮جـارِ البـحث ♥️ ،**" )
    match = q_event.pattern_match.group(1)
    page = re.findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1
    search_args = (str(match), int(page))
    gsearch = GoogleSearch()
    gresults = await gsearch.async_search(*search_args)
    msg = ""
    for i in range(len(gresults["links"])):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"👉[{title}]({link})\n`{desc}`\n\n"
        except IndexError:
            break
    await catevent.edit(
        "**اسـم البحث:**\n`" + match + "`\n\n**النتائـج:**\n" + msg, link_preview=False
    )
    if BOTLOG:
        await q_event.client.send_message(
            BOTLOG_CHATID,
            "Google Search query `" + match + "` was executed successfully",
        )


@bot.on(admin_cmd(pattern="تحليل$"))
@bot.on(sudo_cmd(pattern="تحليل$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    OUTPUT_STR = "**بالرد على الصـورة للبحث عن شبيهاتها في جوجل ريـفرس**"
    if event.reply_to_msg_id:
        catevent = await edit_or_reply(event, "** ⌔∮جـارِ البـحث عن المصادر 🎆♥️ ،**")
        previous_message = await event.get_reply_message()
        previous_message_text = previous_message.message
        BASE_URL = "http://www.google.com"
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message, Config.TMP_DOWNLOAD_DIRECTORY
            )
            SEARCH_URL = "{}/searchbyimage/upload".format(BASE_URL)
            multipart = {
                "encoded_image": (
                    downloaded_file_name,
                    open(downloaded_file_name, "rb"),
                ),
                "image_content": "",
            }
            # https://stackoverflow.com/a/28792943/4723940
            google_rs_response = requests.post(
                SEARCH_URL, files=multipart, allow_redirects=False
            )
            the_location = google_rs_response.headers.get("Location")
            os.remove(downloaded_file_name)
        else:
            previous_message_text = previous_message.message
            SEARCH_URL = "{}/searchbyimage?image_url={}"
            request_url = SEARCH_URL.format(BASE_URL, previous_message_text)
            google_rs_response = requests.get(request_url, allow_redirects=False)
            the_location = google_rs_response.headers.get("Location")
        await catevent.edit("**تم العثور على نتيجة في جوجل...**")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
        }
        response = requests.get(the_location, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        # document.getElementsByClassName("r5a77d"): PRS
        try:
            prs_div = soup.find_all("div", {"class": "r5a77d"})[0]
            prs_anchor_element = prs_div.find("a")
            prs_url = BASE_URL + prs_anchor_element.get("href")
            prs_text = prs_anchor_element.text
            # document.getElementById("jHnbRc")
            img_size_div = soup.find(id="jHnbRc")
            img_size = img_size_div.find_all("div")
        except Exception:
            return await edit_delete(
                catevent, "**معـذرةً لم استطـع ايجـاد نتائـج مشابهـه**"
            )
        end = datetime.now()
        ms = (end - start).seconds
        OUTPUT_STR = """{img_size}
<b>بحث ذو صـله : </b> <a href="{prs_url}">{prs_text}</a> 
<b>لعرض النتائـج المشابهـه : </b> اضغط هنا <a href="{the_location}">الرابط</a> 
<i>سرعة البحث {ms} ثواني</i>""".format(
            **locals()
        )
    await catevent.edit(OUTPUT_STR, parse_mode="HTML", link_preview=False)


@bot.on(admin_cmd(pattern=r"تخمين(?: |$)(\d*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"تخمين(?: |$)(\d*)", allow_sudo=True))
@errors_handler
async def _(img):
    if os.path.isfile("okgoogle.png"):
        os.remove("okgoogle.png")
    message = await img.get_reply_message()
    if message and message.media:
        photo = io.BytesIO()
        await bot.download_media(message, photo)
    else:
        await edit_or_reply(img, "**بالرد على الملصق للبحث عن مصادرها في جوجل ريـفرس**")
        return
    if photo:
        catevent = await edit_or_reply(img, "** ⌔∮جـارِ البـحث عن المصادر 🎆♥️ ،**")
        try:
            image = Image.open(photo)
        except OSError:
            await catevent.edit("**غير مدعوم ، على الأرجح ...**")
            return
        name = "okgoogle.png"
        image.save(name, "PNG")
        image.close()
        # https://stackoverflow.com/questions/23270175/google-reverse-image-search-using-post-request#28792943
        searchUrl = "https://www.google.com/searchbyimage/upload"
        multipart = {"encoded_image": (name, open(name, "rb")), "image_content": ""}
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        fetchUrl = response.headers["Location"]
        if response != 400:
            await img.edit(
                "**تم تحميل الصورة بنجاح إلى جوجل. يمكن.**"
                "\n**تم تحليل المصدر الآن...**"
            )
        else:
            await catevent.edit("`Google told me to fuck off.`")
            return
        os.remove(name)
        match = await ParseSauce(fetchUrl + "&preferences?hl=en&fg=1#languages")
        guess = match["best_guess"]
        imgspage = match["similar_images"]
        if guess and imgspage:
            await catevent.edit(f"[{guess}]({fetchUrl})\n\n**البحث عن هذه الصورة ...**")
        else:
            await catevent.edit("**معـذرةً لم استطـع ايجـاد أي نتائـج مشابهـه**")
            return

        lim = img.pattern_match.group(1) or 3
        images = await scam(match, lim)
        yeet = []
        for i in images:
            k = requests.get(i)
            yeet.append(k.content)
        try:
            await img.client.send_file(
                entity=await img.client.get_input_entity(img.chat_id),
                file=yeet,
                reply_to=img,
            )
        except TypeError:
            pass
        await catevent.edit(
            f"[{guess}]({fetchUrl})\n\n[لصـور مشابهـه اخـرى اضغط هنا...]({imgspage})"
        )


async def ParseSauce(googleurl):
    """Parse/Scrape the HTML code for the info we want."""
    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, "html.parser")
    results = {"similar_images": "", "best_guess": ""}
    try:
        for similar_image in soup.findAll("input", {"class": "gLFyf"}):
            url = "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote_plus(
                similar_image.get("value")
            )
            results["similar_images"] = url
    except BaseException:
        pass
    for best_guess in soup.findAll("div", attrs={"class": "r5a77d"}):
        results["best_guess"] = best_guess.get_text()
    return results


async def scam(results, lim):
    single = opener.open(results["similar_images"]).read()
    decoded = single.decode("utf-8")
    imglinks = []
    counter = 0
    pattern = r"^,\[\"(.*[.png|.jpg|.jpeg])\",[0-9]+,[0-9]+\]$"
    oboi = re.findall(pattern, decoded, re.I | re.M)
    for imglink in oboi:
        counter += 2
        if counter <= int(lim):
            imglinks.append(imglink)
        else:
            break
    return imglinks


CMD_HELP.update(
    {
        "جوجل": "**اسم الاضافـه :**`جوجل`\
        \n\n  **╮•❐ الامـر ⦂** `.جوجل (عدد) (كلمه)` او `.جوجل (عدد) (بالرد على الرساله)`\
        \n•  **الشـرح •• **يقوم بالبحـث فـي جوجـل وارسال عشـر نتائـج للروابـط.\
        \n\n  **╮•❐ الامـر ⦂** `.تحليل` بالرد على الصوره\
        \n•  **الشـرح •• **للبحث عن مصادر الصوره الاصليه وشبيهاتها على جـوجل واعطـاء رابـط بمصـدر الصـوره الاصليـه.\
        \n\n  **╮•❐ الامـر ⦂ **`.تخمين + عدد`\
        \n•  **الشـرح •• **للبحث عن مصادر الصوره الاصليه للملصق على جـوجل واعطـاء رابـط بمصـدر الصـوره الاصليـه"
    }
)
