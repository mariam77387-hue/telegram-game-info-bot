# telegram_bot4.py
#
# مسؤول عن: زر "أفكار ماينكرافت" (صور + مستوى صعوبة)

import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# =========================================================
# عدّلي هذي القائمة: كل فكرة فيها اسم، صعوبة، ورابط صورة
# رابط الصورة لازم يكون رابط مباشر لصورة (ينتهي بـ .jpg أو .png)
# ارفعي صورك على imgur مثلاً وخذي الرابط المباشر (Direct link)
# =========================================================

MINECRAFT_IDEAS = [
    {
        "name_ar": "بيت خشبي بسيط",
        "name_en": "Simple Wooden House",
        "difficulty_ar": "🟢 سهل",
        "difficulty_en": "🟢 Easy",
        "image": "https://j.top4top.io/p_3893k4yg40.jpeg",
    },
    {
        "name_ar": "منزل حجري متوسط",
        "name_en": "Medium Stone House",
        "difficulty_ar": "🟡 متوسط",
        "difficulty_en": "🟡 Medium",
        "image": "https://c.top4top.io/p_3893uefjv0.jpeg",
    },
    {
        "name_ar": "قلعة كبيرة",
        "name_en": "Large Castle",
        "difficulty_ar": "🔴 صعب",
        "difficulty_en": "🔴 Hard",
        "image": "ضعي_رابط_الصورة_هنا_3.jpg",
    },
    # أضيفي أي عدد تبغينه بنفس الشكل
]


def get_language(context):
    return context.user_data.get("language", "ar")


def choose_random_idea(context):
    previous = context.user_data.get("last_idea")
    choices = list(range(len(MINECRAFT_IDEAS)))

    if previous in choices and len(choices) > 1:
        choices.remove(previous)

    index = random.choice(choices)
    context.user_data["last_idea"] = index
    return MINECRAFT_IDEAS[index]


def idea_caption(idea, language):
    if language == "ar":
        return (
            f"🧱 *{idea['name_ar']}*\n\n"
            f"🎯 مستوى الصعوبة: {idea['difficulty_ar']}"
        )
    return (
        f"🧱 *{idea['name_en']}*\n\n"
        f"🎯 Difficulty: {idea['difficulty_en']}"
    )


def idea_markup(language):
    if language == "ar":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 فكرة ثانية", callback_data="minecraft_ideas")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="minecraft_back")],
        ])
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Another Idea", callback_data="minecraft_ideas")],
        [InlineKeyboardButton("🔙 Back", callback_data="minecraft_back")],
    ])


async def minecraft_ideas(update, context):
    query = update.callback_query
    await query.answer()

    language = get_language(context)
    idea = choose_random_idea(context)

    await context.bot.send_photo(
        chat_id=query.message.chat_id,
        photo=idea["image"],
        caption=idea_caption(idea, language),
        parse_mode="Markdown",
        reply_markup=idea_markup(language),
    )


async def minecraft_back(update, context):
    # الرسالة الحالية صورة، فما نقدر نستخدم edit_message_text عليها
    # نرسل القائمة كرسالة جديدة بدل التعديل
    from telegram_bot3 import main_menu_text, new_main_menu

    query = update.callback_query
    await query.answer()

    language = get_language(context)

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=main_menu_text(language),
        parse_mode="Markdown",
        reply_markup=new_main_menu(language),
    )
