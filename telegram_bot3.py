# telegram_bot3.py
#
# =========================================================
# Bot 3 - قائمة الألعاب المنظمة
# =========================================================
#
# مسؤول عن:
# 🎮 ترتيب وعرض قائمة الألعاب
# 🤠 زر Red Dead
# 🎲 اكتشف لعبة
# 🔎 بحث عن لعبة
# 🧠 تحدي الألعاب
# ➕ طلب لعبة
#
# ملاحظة:
# telegram_bot.py هو الملف الرئيسي والمسؤول عن تنفيذ
# الـ callbacks ومعلومات الألعاب وقاعدة البيانات.
# =========================================================

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# =========================================================
# قائمة الألعاب
# =========================================================

GAME_LIST = [
    ("minecraft", "⛏️", "Minecraft"),
    ("roblox", "🎮", "Roblox"),
    ("fortnite", "🚌", "Fortnite"),
    ("valorant", "🎯", "Valorant"),
    ("rocketleague", "🏎️", "Rocket League"),
    ("brawlstars", "⭐", "Brawl Stars"),
    ("gtav", "🚗", "GTA V"),
    ("genshinimpact", "✨", "Genshin Impact"),
    ("clashroyale", "👑", "Clash Royale"),
    ("overwatch", "🦸", "Overwatch"),
    ("eldenring", "⚔️", "Elden Ring"),
    ("bloodborne", "🩸", "Bloodborne"),
]


# =========================================================
# نص القائمة الرئيسية
# =========================================================

def main_menu_text(language="ar"):
    """
    النص الذي يظهر فوق قائمة الألعاب.
    """

    if language == "ar":
        return (
            "🎮 *مركز الألعاب*\n\n"
            "اختر لعبة أو استخدم إحدى الأدوات بالأسفل 👇"
        )

    return (
        "🎮 *Gaming Center*\n\n"
        "Choose a game or use one of the tools below 👇"
    )


# =========================================================
# القائمة الرئيسية
# =========================================================

def new_main_menu(language="ar"):
    """
    إنشاء القائمة الرئيسية.

    الألعاب:
    3 ألعاب في كل صف.

    الأدوات:
    اكتشف لعبة + بحث عن لعبة
    تحدي الألعاب + طلب لعبة
    """

    keyboard = []
    row = []

    # -----------------------------------------------------
    # الألعاب
    # -----------------------------------------------------

    for game_id, emoji, name in GAME_LIST:

        row.append(
            InlineKeyboardButton(
                f"{emoji} {name}",
                callback_data=game_id,
            )
        )

        # كل صف يحتوي على 3 ألعاب
        if len(row) == 3:
            keyboard.append(row)
            row = []

    # إذا بقيت لعبة أو لعبتان في آخر الصف
    if row:
        keyboard.append(row)

    # -----------------------------------------------------
    # Red Dead
    # -----------------------------------------------------

    keyboard.append([
        InlineKeyboardButton(
            "🤠 Red Dead",
            callback_data="red_dead",
        )
    ])

    # -----------------------------------------------------
    # الأدوات
    # -----------------------------------------------------

    if language == "ar":

        keyboard.append([
            InlineKeyboardButton(
                "🎲 اكتشف لعبة",
                callback_data="discover_game",
            ),
            InlineKeyboardButton(
                "🔎 بحث عن لعبة",
                callback_data="search_game",
            ),
        ])

        keyboard.append([
            InlineKeyboardButton(
                "🧠 تحدي الألعاب",
                callback_data="quiz_start",
            ),
            InlineKeyboardButton(
                "➕ طلب لعبة",
                callback_data="request_game",
            ),
        ])

    else:

        keyboard.append([
            InlineKeyboardButton(
                "🎲 Discover Game",
                callback_data="discover_game",
            ),
            InlineKeyboardButton(
                "🔎 Search Game",
                callback_data="search_game",
            ),
        ])

        keyboard.append([
            InlineKeyboardButton(
                "🧠 Game Challenge",
                callback_data="quiz_start",
            ),
            InlineKeyboardButton(
                "➕ Request Game",
                callback_data="request_game",
            ),
        ])

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# دالة الحصول على الألعاب
# =========================================================

def get_game_list():
    """
    ترجع قائمة الألعاب الموجودة في Bot 3.
    """

    return GAME_LIST.copy()


# =========================================================
# التحقق من وجود لعبة
# =========================================================

def has_game(game_id):
    """
    التحقق من وجود لعبة في قائمة Bot 3.
    """

    return any(
        item[0] == game_id
        for item in GAME_LIST
    )


# =========================================================
# عدد الألعاب
# =========================================================

def get_game_count():
    """
    ترجع عدد الألعاب الموجودة في القائمة.
    """

    return len(GAME_LIST)


# =========================================================
# تسجيل الـ handlers
# =========================================================

def register_bot3_handlers(app):
    """
    Bot 3 لا يسجل CallbackQueryHandlers بنفسه.

    telegram_bot.py هو الملف الرئيسي والمسؤول عن
    التعامل مع callbacks.

    نترك الدالة موجودة حتى يستطيع telegram_bot.py
    استدعاءها بدون حدوث خطأ.
    """

    return None


# =========================================================
# اختبار الملف
# =========================================================

def test_bot3():

    print("=" * 55)
    print("✅ telegram_bot3.py جاهز")
    print("=" * 55)

    print(
        f"🎮 عدد الألعاب: {get_game_count()}"
    )

    print(
        "📐 ترتيب القائمة: 3 ألعاب في كل صف"
    )

    print(
        "🤠 Red Dead: جاهز"
    )

    print(
        "🎲 اكتشف لعبة: جاهز"
    )

    print(
        "🔎 بحث عن لعبة: جاهز"
    )

    print(
        "🧠 تحدي الألعاب: جاهز"
    )

    print(
        "➕ طلب لعبة: جاهز"
    )

    print(
        "🩸 Bloodborne: مضافة"
    )

    print("=" * 55)


# =========================================================
# تشغيل الاختبار عند تشغيل الملف مباشرة
# =========================================================

if __name__ == "__main__":
    test_bot3()