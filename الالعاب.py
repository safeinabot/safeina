""" 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢™ - @S_F_M_L"""

import asyncio
import random
import pyfiglet
from telethon.tl.types import InputMediaDice
from time import sleep
from datetime import datetime
from telethon import Button, events
from telethon.events import CallbackQuery
from telethon.utils import get_display_name
from collections import deque
from random import choice
from . import ALIVE_NAME
from ..helpers import fonts as emojify
from ..helpers.utils import reply_id, _icssutils, parse_pre, install_pip, get_user_from_event, _format
from . import deEmojify
from ..helpers import get_user_from_event
# EMOJI CONSTANTS
DART_E_MOJI = "🎯"
DICE_E_MOJI = "🎲"
BALL_E_MOJI = "🏀"
FOOT_E_MOJI = "⚽️"
SLOT_E_MOJI = "🎰"
# EMOJI CONSTANTS

U = "𓆰 [𝑺𝑶𝑼𝑹𝑪𝑬 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢 - 𝑪𝑶𝑴𝑴𝑨𝑵𝑫𝑺](t.me/safeina1) 𓆪\n\n\n**⌔∮ قائـمه اوامر الالعاب :** \n\n⪼ `.بلاي` لعرض قائمـة الالعـاب الاحترافيـه\n⪼ `.كت` لعبـة كـت تـويت \n⪼ `.اكس او`\n⪼ `.سهم`\n⪼ `.نرد`\n⪼ `.سلة`\n⪼ `.قدم`\n⪼ `.حظ` \n\n𓆩 [𝙎𝙊𝙐𝙍𝘾𝞝 𝑺𝑨𝑭𝑬𝑰𝑵𝑨 𖠢](t.me/S_F_M_L) 𓆪"

@bot.on(admin_cmd(pattern="م22"))
@bot.on(sudo_cmd(pattern="م22", allow_sudo=True))
async def wspr(kimo):
    await eor(kimo, U)

@bot.on(admin_cmd(pattern="اكس او$"))
@bot.on(sudo_cmd(pattern="اكس او$", allow_sudo=True))
async def gamez(event):
    if event.fwd_from:
        return
    botusername = "@xobot"
    noob = "play"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, noob)
    await tap[0].click(event.chat_id)
    await event.delete()


@bot.on(admin_cmd(pattern=f"({DART_E_MOJI}|سهم)( ([1-6])|$)"))
@bot.on(
    sudo_cmd(
        pattern=f"({DART_E_MOJI}|سهم)( ([1-6])|$)",
        allow_sudo=True,
    )
)
async def _(event):
    if event.fwd_from:
        return
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    if emoticon == "سهم":
        emoticon = "🎯"
    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except BaseException:
            pass
    else:
        if event.sender_id == event.client.uid:
            await event.edit(file=InputMediaDice(emoticon=emoticon))
        else:
            await event.reply(file=InputMediaDice(emoticon=emoticon))


@bot.on(admin_cmd(pattern=f"({DICE_E_MOJI}|نرد)( ([1-6])|$)"))
@bot.on(
    sudo_cmd(
        pattern=f"({DICE_E_MOJI}|نرد)( ([1-6])|$)",
        allow_sudo=True,
    )
)
async def _(event):
    if event.fwd_from:
        return
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    if emoticon == "نرد":
        emoticon = "🎲"
    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except BaseException:
            pass
    else:
        if event.sender_id == event.client.uid:
            await event.edit(file=InputMediaDice(emoticon=emoticon))
        else:
            await event.reply(file=InputMediaDice(emoticon=emoticon))


@bot.on(admin_cmd(pattern=f"({BALL_E_MOJI}|سلة)( ([1-5])|$)"))
@bot.on(
    sudo_cmd(
        pattern=f"({BALL_E_MOJI}|سلة)( ([1-5])|$)",
        allow_sudo=True,
    )
)
async def _(event):
    if event.fwd_from:
        return
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    if emoticon == "سلة":
        emoticon = "🏀"
    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except BaseException:
            pass
    else:
        if event.sender_id == event.client.uid:
            await event.edit(file=InputMediaDice(emoticon=emoticon))
        else:
            await event.reply(file=InputMediaDice(emoticon=emoticon))


@bot.on(admin_cmd(pattern=f"({FOOT_E_MOJI}|قدم)( ([1-5])|$)"))
@bot.on(
    sudo_cmd(
        pattern=f"({FOOT_E_MOJI}|قدم)( ([1-5])|$)",
        allow_sudo=True,
    )
)
async def _(event):
    if event.fwd_from:
        return
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    if emoticon == "قدم":
        emoticon = "⚽️"
    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except BaseException:
            pass
    else:
        if event.sender_id == event.client.uid:
            await event.edit(file=InputMediaDice(emoticon=emoticon))
        else:
            await event.reply(file=InputMediaDice(emoticon=emoticon))


@bot.on(admin_cmd(pattern=f"({SLOT_E_MOJI}|حظ)( ([1-64])|$)"))
@bot.on(
    sudo_cmd(
        pattern=f"({SLOT_E_MOJI}|حظ)( ([1-64])|$)",
        allow_sudo=True,
    )
)
async def _(event):
    if event.fwd_from:
        return
    reply_message = event
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
    emoticon = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    await event.delete()
    if emoticon == "حظ":
        emoticon = "🎰"
    r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
    if input_str:
        try:
            required_number = int(input_str)
            while r.media.value != required_number:
                await r.delete()
                r = await reply_message.reply(file=InputMediaDice(emoticon=emoticon))
        except BaseException:
            pass
    else:
        if event.sender_id == event.client.uid:
            await event.edit(file=InputMediaDice(emoticon=emoticon))
        else:
            await event.reply(file=InputMediaDice(emoticon=emoticon))


kettuet = [  
  "اكثر شي ينرفزك .. ؟!",
  "اخر مكان رحتله ..؟!",
  "سـوي تـاك @ لـ شخص تريـد تعترفلـه بشي ؟",
  "تغار ..؟!",
  "هـل تعتقـد ان في أحـد يراقبـك 👩🏼‍💻..؟!",
  "أشخاص ردتهم يبقون وياك ومن عرفو هلشي سوو العكس صارت معك؟",
  "ولادتك بنفس المكان الي هسة عايش بي او لا؟",
  "اكثر شي ينرفزك ؟",
  "تغار ؟",
  "كم تبلغ ذاكرة هاتفك؟",
  "صندوق اسرارك ؟",
  "شخص @ تعترفلة بشي ؟",
  "يومك ضاع على ؟",
  "اغرب شيء حدث في حياتك ؟",
  " نسبة حبك للاكل ؟",
  " حكمة تأمان بيها ؟",
  " اكثر شي ينرفزك ؟",
  " هل تعرضت للظلم من قبل؟",
  " خانوك ؟",
  " تزعلك الدنيا ويرضيك ؟",
  " تاريخ غير حياتك ؟",
  " أجمل سنة ميلادية مرت عليك ؟",
  " ولادتك بنفس المكان الي هسة عايش بي او لا؟",
  " تزعلك الدنيا ويرضيك ؟",
  " ماهي هوايتك؟",
  " دوله ندمت انك سافرت لها ؟",
  "شخص اذا جان بلطلعة تتونس بوجود؟",
  " تاخذ مليون دولار و تضرب خويك؟",
  " تاريخ ميلادك؟",
  "اشكم مره حبيت ؟",
  " يقولون ان الحياة دروس ، ماهو أقوى درس تعلمته من الحياة ؟",
  " هل تثق في نفسك ؟",
  " كم مره نمت مع واحده ؟",
  " اسمك الثلاثي ؟",
  "كلمة لشخص خذلك؟",
  "هل انت متسامح ؟",
  "طريقتك المعتادة في التخلّص من الطاقة السلبية؟",
  "عصير لو قهوة؟",
  " صديق أمك ولا أبوك. ؟",
  "تثق بـ احد ؟",
  "كم مره حبيت ؟",
  "اكمل الجملة التالية..... قال رسول الله ص،، انا مدينة العلم وعلي ؟",
  " اوصف حياتك بكلمتين ؟",
  " حياتك محلوا بدون ؟",
  " وش روتينك اليومي؟",
  " شي تسوي من تحس بلملل؟",
  " يوم ميلادك ؟",
  " اكثر مشاكلك بسبب ؟",
  " تزعلك الدنيا ويرضيك ؟",
  " تتوقع فيه احد حاقد عليك ويكرهك ؟",
  "كلمة غريبة من لهجتك ومعناها؟",
"   هل تحب اسمك أو تتمنى تغييره وأي الأسماء ستختار" ,
"  كيف تشوف الجيل ذا؟",
"  تاريخ لن تنساه📅؟",
"  هل من الممكن أن تقتل أحدهم من أجل المال؟",
"  تؤمن ان في حُب من أول نظرة ولا لا ؟.",
"  ‏ماذا ستختار من الكلمات لتعبر لنا عن حياتك التي عشتها الى الآن؟💭",
"  طبع يمكن يخليك تكره شخص حتى لو كنت تُحبه🙅🏻‍♀️؟",
"  ما هو نوع الموسيقى المفضل لديك والذي تستمع إليه دائمًا؟ ولماذا قمت باختياره تحديدًا؟",
"  أطول مدة نمت فيها كم ساعة؟",
"  كلمة غريبة من لهجتك ومعناها؟🤓",
"  ردة فعلك لو مزح معك شخص م تعرفه ؟",
"  شخص تحب تستفزه😈؟",
"  تشوف الغيره انانيه او حب؟",
"  مع او ضد : النوم افضل حل لـ مشاكل الحياة؟",
"  اذا اكتشفت أن أعز أصدقائك يضمر لك السوء، موقفك الصريح؟",
"  ‏للشباب | آخر مرة وصلك غزل من فتاة؟🌚",
"  أوصف نفسك بكلمة؟",
"  شيء من صغرك ماتغير فيك؟",
"  ردة فعلك لو مزح معك شخص م تعرفه ؟",
"  | اذا شفت حد واعجبك وعندك الجرأه انك تروح وتتعرف عليه ، مقدمة الحديث شو راح تكون ؟.",
"  كلمة لشخص أسعدك رغم حزنك في يومٍ من الأيام ؟",
"  حاجة تشوف نفسك مبدع فيها ؟",
"  يهمك ملابسك تكون ماركة ؟",
"  يومك ضاع على؟",
"  اذا اكتشفت أن أعز أصدقائك يضمر لك"," السوء، موقفك الصريح؟",
"  هل من الممكن أن تقتل أحدهم من أجل المال؟",
"  كلمه ماسكه معك الفترة هذي ؟",
"  كيف هي أحوال قلبك؟",
"  صريح، مشتاق؟",
"  اغرب اسم مر عليك ؟",
"  تختار أن تكون غبي أو قبيح؟",
"  آخر مرة أكلت أكلتك المفضّلة؟",
"  دوله ندمت انك سافرت لها😁؟",
"  اشياء صعب تتقبلها بسرعه ؟",
"  كلمة لشخص غالي اشتقت إليه؟💕",
"  اكثر شيء تحس انه مات ف مجتمعنا؟",
"  هل يمكنك مسامحة شخص أخطأ بحقك لكنه قدم الاعتذار وشعر بالندم؟",
"  آخر شيء ضاع منك؟",
"  تشوف الغيره انانيه او حب؟",
"  لو فزعت/ي لصديق/ه وقالك مالك دخل وش بتسوي/ين؟",
"  شيء كل م تذكرته تبتسم ...",
"  هل تحبها ولماذا قمت باختيارها؟",
"  هل تنفق مرتبك بالكامل أم أنك تمتلك هدف يجعلك توفر المال؟",
"  متى تكره الشخص الذي أمامك حتى لو كنت مِن أشد معجبينه؟",
"  أقبح القبحين في العلاقة: الغدر أو الإهمال🤷🏼؟", 
"  هل وصلك رسالة غير متوقعة من شخص وأثرت فيك ؟",
"  هل تشعر أن هنالك مَن يُحبك؟",
"  وش الشيء الي تطلع حرتك فيه و زعلت ؟",
"  صوت مغني م تحبه",
"  كم في حسابك البنكي ؟",
"  اذكر موقف ماتنساه بعمرك؟",
"  ردة فعلك لو مزح معك شخص م تعرفه ؟",
"  عندك حس فكاهي ولا نفسية؟",
"  من وجهة نظرك ما هي الأشياء التي تحافظ على قوة وثبات العلاقة؟",
"  ما هو نوع الموسيقى المفضل لديك والذي تستمع إليه دائمًا؟ ولماذا قمت باختياره تحديدًا؟",
"  هل تنفق مرتبك بالكامل أم أنك تمتلك هدف يجعلك توفر المال؟",
"  هل وصلك رسالة غير متوقعة من شخص وأثرت فيك ؟",
"  شيء من صغرك ماتغير فيك؟",
"  هل يمكنك أن تضحي بأكثر شيء تحبه وتعبت للحصول عليه لأجل شخص تحبه؟",
"  هل تحبها ولماذا قمت باختيارها؟",
"  لو فزعت/ي لصديق/ه وقالك مالك دخل وش بتسوي/ين؟",
"  كلمة لشخص أسعدك رغم حزنك في يومٍ من الأيام ؟",
"  كم مره تسبح باليوم",
"  أفضل صفة تحبه بنفسك؟",
"  أجمل شيء حصل معك خلال هاليوم؟",
"  ‏شيء سمعته عالق في ذهنك هاليومين؟",
"  هل يمكنك تغيير صفة تتصف بها فقط لأجل شخص تحبه ولكن لا يحب تلك الصفة؟",
"  ‏أبرز صفة حسنة في صديقك المقرب؟",
"  ما الذي يشغل بالك في الفترة الحالية؟",
"  آخر مرة ضحكت من كل قلبك؟",
"  احقر الناس هو من ...",
"  اكثر دوله ودك تسافر لها🏞؟",
"  آخر خبر سعيد، متى وصلك؟",
"  ‏نسبة احتياجك للعزلة من 10📊؟",
"  هل تنفق مرتبك بالكامل أم أنك تمتلك هدف يجعلك توفر المال؟",
"  أكثر جملة أثرت بك في حياتك؟",
"  لو قالوا لك  تناول صنف واحد فقط من الطعام لمدة شهر .",
"  هل تنفق مرتبك بالكامل أم أنك تمتلك هدف يجعلك توفر المال؟",
"  آخر مرة ضحكت من كل قلبك؟",
"  وش الشيء الي تطلع حرتك فيه و زعلت ؟",
"  تزعلك الدنيا ويرضيك ؟",
"  متى تكره الشخص الذي أمامك حتى لو كنت مِن أشد معجبينه؟",
"  تعتقد فيه أحد يراقبك👩🏼‍💻؟",
"  احقر الناس هو من ...",
"  شيء من صغرك ماتغير فيك؟",
"  وين نلقى السعاده برايك؟",
"  هل تغارين من صديقاتك؟",
"  أكثر جملة أثرت بك في حياتك؟",
"  كم عدد اللي معطيهم بلوك👹؟",
"  أجمل سنة ميلادية مرت عليك ؟",
"  أوصف نفسك بكلمة؟",
 ]

@bot.on(admin_cmd(pattern="كت(?: |$)(.*)"))
async def permalink(mention):
    zedt = random.choice(kettuet)
    await edit_or_reply(mention, f"**⌔╎{zedt} **")


CMD_HELP.update(
    {
        "الالعاب": "**Syntax :** `.🎯 [1-6]` or `.سهم [1-6]`\
    \n**Usage : **each number shows different animation for dart\
    \n\n**Syntax : **`.🎲 [1-6]` or `.نرد [1-6]`\
    \n**Usage : **each number shows different animation for dice\
    \n\n**Syntax : **`.🏀 [1-5]` or `.سلة [1-5]`\
    \n**Usage : **each number shows different animation for basket ball\
    \n\n**Syntax : **`.⚽️ [1-5] `or `.قدم [1-5]`\
    \n**Usage : **each number shows different animation for football\
    \n\n**Syntax : **`.🎰 [1-64] `or `.حظ [1-64]`\
    \n**Usage : **each number shows different animation for slot machine(jackpot)\
    "
    }
)
