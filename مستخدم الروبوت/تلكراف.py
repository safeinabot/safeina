"""
𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢 : @safeina1
  - Telegraph Utils For safeina
  - Telegraph Media Commend: .تلكراف ميديا
  - Telegraph Text Commend: .تلكراف نص
"""


# telegraph utils for Source Safeina1

import os
from datetime import datetime

from PIL import Image
from telegraph import Telegraph, exceptions, upload_file

from . import BOTLOG_CHATID, mention

telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]


@bot.on(
    admin_cmd(
       pattern="تلكراف (ميديا|نص) ?(.*)"
    )
)
@bot.on(sudo_cmd(pattern="تلكراف(ميديا|نص) ?(.*)", allow_sudo=True))
@bot.on(
    admin_cmd(
       pattern="tg(m|t) ?(.*)"
    )
)
@bot.on(sudo_cmd(pattern="tg(m|t) ?(.*)", allow_sudo=True))
async def _(tosh):
    if tosh.fwd_from:
        return
    ice = await eor(tosh, "** ⪼ جاري المعالجه ༗...**")
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
        #     if BOTLOG:
        await tosh.client.send_message(
            BOTLOG_CHATID,
            "**⌔∮ تم إنشاء حساب Telegraph جديد {} للدورة الحالية‌‌** \n**⌔∮ لا تعطي عنوان url هذا لأي شخص**".format(
                auth_url
            ),
        )
    optional_title = tosh.pattern_match.group(2)
    if tosh.reply_to_msg_id:
        start = datetime.now()
        r_message = await tosh.get_reply_message()
        input_str = tosh.pattern_match.group(1)
        if input_str in ["ميديا", "m"]:
            downloaded_file_name = await tosh.client.download_media(
                r_message, Config.TEMP_DIR
            )
            end = datetime.now()
            ms = (end - start).seconds
            await ice.edit(
                f"** ⪼ تم تحميل {downloaded_file_name} في وقت {ms} ثانيه.**"
            )
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await ice.edit("**⌔∮ خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                await ice.edit(
                    "**⌔∮ الرابط : **[اضغط هنا](https://telegra.ph{})\
                    \n**⌔∮ الوقت : **`{} ثانيه.` \n**⌔∮ تم التحميل بواسطه :** {}".format(
                        media_urls[0], (ms + ms_two), (mention)
                    ),
                    link_preview=True,
                )
        elif input_str in ["نص", "t"]:
            user_object = await tosh.client.get_entity(r_message.sender_id)
            title_of_page = user_object.first_name  # + " " + user_object.last_name
            # apparently, all Users do not have last_name field
            if optional_title:
                title_of_page = optional_title
            page_content = r_message.message
            if r_message.media:
                if page_content != "":
                    title_of_page = page_content
                downloaded_file_name = await tosh.client.download_media(
                    r_message, Config.TEMP_DIR
                )
                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()
                for m in m_list:
                    page_content += m.decode("UTF-8") + "\n"
                os.remove(downloaded_file_name)
            page_content = page_content.replace("\n", "<br>")
            response = telegraph.create_page(title_of_page, html_content=page_content)
            end = datetime.now()
            ms = (end - start).seconds
            kimo = f"https://telegra.ph/{response['path']}"
            await ice.edit(
                f"**الرابط : ** [اضغط هنا]({kimo})\
                 \n**الوقت : **`{ms} ثانيه.`",
                link_preview=True,
            )
    else:
        await ice.edit(
            "قم بالرد على رسالة للحصول على رابط تللكراف دائم.",
        )


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


CMD_HELP.update(
    {
        "تلكراف": "**Plugin :**`تلكراف`\
     \n\n  •  **Syntax :** `.تلكراف ميديا` `or` `tgm`\
     \n  •  **Function :**__Reply to any image or video to upload it to telegraph (video must be less than 5mb)__\
     \n\n  •  **Syntax :** `.تلكراف نص` `or` `.tgt`\
     \n  •  **Function :** __reply to any text file or any message to paste it to telegraph__\
    "
    }
)
