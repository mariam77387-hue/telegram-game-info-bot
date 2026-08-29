# telegram_bot4.py
#
# مسؤول عن: زر "أفكار ماينكرافت" (صور + مستوى صعوبة)

import io
import random
import requests

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# =========================================================
# عدّل هذي القائمة: كل فكرة فيها اسم، صعوبة، ورابط صورة
# =========================================================

MINECRAFT_IDEAS = [
    {
        "name_ar": "بيت خشبي بسيط",
        "name_en": "Simple Wooden House",
        "difficulty_ar": "🟢 سهل",
        "difficulty_en": "🟢 Easy",
        "image": "https://raw.githubusercontent.com/mariam77387-hue/telegram-game-info-bot/main/images/IMG_7854.jpeg",
    },
    {
        "name_ar": "منزل حجري متوسط",
        "name_en": "Medium Stone House",
        "difficulty_ar": "🟡 متوسط",
        "difficulty_en": "🟡 Medium",
        "image": "https://raw.githubusercontent.com/mariam77387-hue/telegram-game-info-bot/main/images/IMG_7857.jpeg",
    },
    {
        "name_ar": "قلعة كبيرة",
        "name_en": "Large Castle",
        "difficulty_ar": "🔴 صعب",
        "difficulty_en": "🔴 Hard",
        "image": "https://raw.githubusercontent.com/mariam77387-hue/telegram-game-info-bot/main/images/IMG_7859.jpeg",
    },
    # أضف أي عدد تبغيه بنفس الشكل
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


def download_image(url):
    """
    يحمّل الصورة يدويًا باستخدام User-Agent متصفح
    عشان نتجاوز حماية بعض المواقع ضد الروابط المباشرة.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    return io.BytesIO(response.content)


async def minecraft_ideas(update, context):
    query = update.callback_query
    await query.answer()

    language = get_language(context)
    idea = choose_random_idea(context)

    try:
        photo_file = download_image(idea["image"])
        photo_file.name = "idea.jpg"

        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=photo_file,
            caption=idea_caption(idea, language),
            parse_mode="Markdown",
            reply_markup=idea_markup(language),
        )
    except Exception as error:
        print(
            f"❌ Minecraft idea photo error: {error} | image: {idea['image']}",
            flush=True,
        )
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=(
                "⚠️ صار خطأ بجلب الصورة، جرب مرة ثانية."
                if language == "ar"
                else "⚠️ Failed to load the image, please try again."
            ),
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
