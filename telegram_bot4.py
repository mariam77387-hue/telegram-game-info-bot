# telegram_bot4.py
#
# مسؤول عن: قائمة "أفكار ماينكرافت" (صور + مستوى صعوبة)

import io
import random
import requests

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# =========================================================
# قائمة أفكار ماينكرافت
#
# لإضافة فكرة جديدة مستقبلاً:
# 1) ارفع صورة جديدة على GitHub (نفس طريقة الصور السابقة)
# 2) افتحيها واضغطي زر Raw وانسخي الرابط
# 3) أضيفي كتلة جديدة هنا بنفس الشكل بالأسفل
#    (id لازم يكون فريد وبدون مسافات أو رموز)
# لا تحذفي أي كتلة قديمة، فقط أضيفي كتل جديدة.
# =========================================================

MINECRAFT_IDEAS = [
    {
        "id": "wooden_house",
        "name_ar": "🌲 بيت خشبي دافئ للبداية",
        "name_en": "🌲 Cozy Starter Wooden House",
        "difficulty_ar": "🟢 سهل",
        "difficulty_en": "🟢 Easy",
        "image": "https://raw.githubusercontent.com/mariam77387-hue/telegram-game-info-bot/main/IMG_7854.JPG",
    },
    {
        "id": "stone_house",
        "name_ar": "🧱 منزل حجري أنيق",
        "name_en": "🧱 Elegant Stone House",
        "difficulty_ar": "🟡 متوسط",
        "difficulty_en": "🟡 Medium",
        "image": "https://raw.githubusercontent.com/mariam77387-hue/telegram-game-info-bot/main/IMG_7857.JPG",
    },
    {
        "id": "castle",
        "name_ar": "🏰 قلعة أسطورية مهيبة",
        "name_en": "🏰 Epic Legendary Castle",
        "difficulty_ar": "🔴 صعب",
        "difficulty_en": "🔴 Hard",
        "image": "https://raw.githubusercontent.com/mariam77387-hue/telegram-game-info-bot/main/IMG_7859.JPG",
    },
    {
        "id": "farm",
        "name_ar": "🚜 مزرعة ريفية جميلة",
        "name_en": "🚜 Beautiful Country Farm",
        "difficulty_ar": "🟡 متوسط",
        "difficulty_en": "🟡 Medium",
        "image": "https://raw.githubusercontent.com/mariam77387-hue/telegram-game-info-bot/main/E0AF1719-87E8-4E52-B826-34104EED353A.PNG",
    },

    # ضيفي كتل جديدة هنا 👇
    # {
    #     "id": "new_idea",
    #     "name_ar": "اسم الفكرة",
    #     "name_en": "Idea Name",
    #     "difficulty_ar": "🟡 متوسط",
    #     "difficulty_en": "🟡 Medium",
    #     "image": "رابط الصورة هنا",
    # },
]


def get_language(context):
    return context.user_data.get("language", "ar")


def find_idea_by_id(idea_id):
    for idea in MINECRAFT_IDEAS:
        if idea["id"] == idea_id:
            return idea
    return None


# =========================================================
# قائمة الأفكار (النص + الأزرار)
# =========================================================

def ideas_menu_text(language):
    if language == "ar":
        return (
            "🧱 *أفكار بناء ماينكرافت*\n\n"
            "اختر فكرة عشان تشوف صورتها ومستوى صعوبتها 👇"
        )
    return (
        "🧱 *Minecraft Build Ideas*\n\n"
        "Choose an idea to see its photo and difficulty 👇"
    )


def ideas_menu_markup(language):
    keyboard = []

    for idea in MINECRAFT_IDEAS:

        if language == "ar":
            label = f"{idea['name_ar']} — {idea['difficulty_ar']}"
        else:
            label = f"{idea['name_en']} — {idea['difficulty_en']}"

        keyboard.append([
            InlineKeyboardButton(
                label,
                callback_data=f"minecraft_idea:{idea['id']}",
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            "🔙 رجوع" if language == "ar" else "🔙 Back",
            callback_data="minecraft_back",
        )
    ])

    return InlineKeyboardMarkup(keyboard)


async def minecraft_menu(update, context):
    query = update.callback_query
    await query.answer()

    language = get_language(context)

    try:
        await query.edit_message_text(
            ideas_menu_text(language),
            parse_mode="Markdown",
            reply_markup=ideas_menu_markup(language),
        )
    except Exception:
        # الرسالة الحالية صورة (ما تقدر تتحول لنص)، فنرسل رسالة جديدة
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=ideas_menu_text(language),
            parse_mode="Markdown",
            reply_markup=ideas_menu_markup(language),
        )


# =========================================================
# عرض فكرة واحدة (صورة + كابشن)
# =========================================================

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


def idea_detail_markup(language):
    if language == "ar":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 رجوع لقائمة الأفكار", callback_data="minecraft_menu")],
            [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="minecraft_back")],
        ])
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Ideas List", callback_data="minecraft_menu")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="minecraft_back")],
    ])


def download_image(url):
    """
    يحمّل الصورة يدويا باستخدام User-Agent متصفح
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


async def minecraft_idea_show(update, context):
    query = update.callback_query
    await query.answer()

    language = get_language(context)

    idea_id = query.data.split(":", 1)[1]
    idea = find_idea_by_id(idea_id)

    if not idea:
        await query.edit_message_text(
            "❌ الفكرة غير موجودة." if language == "ar" else "❌ Idea not found."
        )
        return

    try:
        photo_file = download_image(idea["image"])
        photo_file.name = "idea.jpg"

        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=photo_file,
            caption=idea_caption(idea, language),
            parse_mode="Markdown",
            reply_markup=idea_detail_markup(language),
        )
    except Exception as error:
        print(
            f"❌ Minecraft idea photo error: {error} | image: {idea['image']}",
            flush=True,
        )
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=(
                "⚠ صار خطأ بجلب الصورة، جرب مرة ثانية."
                if language == "ar"
                else "⚠️ Failed to load the image, please try again."
            ),
            reply_markup=idea_detail_markup(language),
        )


# =========================================================
# رجوع للقائمة الرئيسية للبوت
# =========================================================

async def minecraft_back(update, context):
    from telegram_bot3 import main_menu_text, new_main_menu

    query = update.callback_query
    await query.answer()

    language = get_language(context)

    try:
        await query.edit_message_text(
            main_menu_text(language),
            parse_mode="Markdown",
            reply_markup=new_main_menu(language),
        )
    except Exception:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=main_menu_text(language),
            parse_mode="Markdown",
            reply_markup=new_main_menu(language),
        )
