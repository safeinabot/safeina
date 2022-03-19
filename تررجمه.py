#safeina

import os
from datetime import datetime

import requests


@bot.on(admin_cmd(pattern="تررجمه (.*)"))
@bot.on(sudo_cmd(pattern="تررجمه (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    icssevent = await edit_or_reply(event, "Downloading to my local, for analysis  🙇")
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        required_file_name = await event.client.download_media(
            previous_message, Config.TMP_DOWNLOAD_DIRECTORY
        )
        lan = input_str
        if (
            Config.IBM_WATSON_CRED_URL is None
            or Config.IBM_WATSON_CRED_PASSWORD is None
        ):
            await icssevent.edit(
                "You need to set the required ENV variables for this module. \nModule stopping"
            )
        else:
            await icssevent.edit("Starting analysis, using IBM WatSon Speech To Text")
            headers = {
                "Content-Type": previous_message.media.document.mime_type,
            }
            data = open(required_file_name, "rb").read()
            response = requests.post(
                Config.IBM_WATSON_CRED_URL + "/v1/recognize",
                headers=headers,
                data=data,
                auth=("apikey", Config.IBM_WATSON_CRED_PASSWORD),
            )
            r = response.json()
            if "results" in r:
                # process the json to appropriate string format
                results = r["results"]
                transcript_response = ""
                transcript_confidence = ""
                for alternative in results:
                    alternatives = alternative["alternatives"][0]
                    transcript_response += " " + str(alternatives["transcript"]) + " + "
                    transcript_confidence += (
                        " " + str(alternatives["confidence"]) + " + "
                    )
                end = datetime.now()
                ms = (end - start).seconds
                if transcript_response != "":
                    string_to_show = "**Language : **`{}`\n**Transcript : **`{}`\n**Time Taken : **`{} seconds`\n**Confidence : **`{}`".format(
                        lan, transcript_response, ms, transcript_confidence
                    )
                else:
                    string_to_show = "**Language : **`{}`\n**Time Taken : **`{} seconds`\n**No Results Found**".format(
                        lan, ms
                    )
                await icssevent.edit(string_to_show)
            else:
                await catevent.edit(r["error"])
            # now, remove the temporary file
            os.remove(required_file_name)
    else:
        await icssevent.edit(
            "Reply to a voice message, to get the relevant transcript."
        )


CMD_HELP.update(
    {
        "تررجمه": "**اسم الاضافـه : **`تررجمه`\
    \n\n**╮•❐ الامـر ⦂** `.تررجمه en` بالرد على الرسالـه الصوتيـه\
    \n**الشـرح •• **ترجمـة صوت الـى نـص"
    }
)
