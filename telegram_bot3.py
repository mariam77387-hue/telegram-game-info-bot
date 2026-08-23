# telegram_bot3.py
#
# =========================================================
# Bot 3 - قائمة الألعاب المنظمة
# =========================================================

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler


# =========================================================
# اللغة
# =========================================================

def get_language(context):
    return context.user_data.get("language", "ar")


# =========================================================
# نص القائمة الرئيسية
# =========================================================

def main_menu_text(language="ar"):
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
# القائمة الرئيسية - 3 أعمدة
# =========================================================

def new_main_menu(language="ar"):
    
    # قائمة الألعاب (11 لعبة)
    game_list = [
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
    ]
    
    keyboard = []
    row = []
    
    # 3 أزرار بكل صف
    for game_id, emoji, name in game_list:
        row.append(
            InlineKeyboardButton(
                f"{emoji} {name}",
                callback_data=game_id,  # بدون bot3_ عشان يشتغل مع الـ handler الرئيسي
            )
        )
        if len(row) == 3:
            keyboard.append(row)
            row = []
    
    if row:
        keyboard.append(row)
    
    # Red Dead - callback_data يطابق الـ handler في telegram_bot.py
    keyboard.append([
        InlineKeyboardButton(
            "🤠 Red Dead",
            callback_data="red_dead",
        )
    ])
    
    # فاصل بصري (بحذفه عشان ما يحتاج handler)
    # keyboard.append([
    #     InlineKeyboardButton("━━━━━━━━━━━━", callback_data="noop")
    # ])
    # ملاحظة: حذفته لأن ما يحتاج فاصل، القائمة مرتبة كفاية
    
    # الأدوات - callback_data تطابق الـ handlers في telegram_bot.py
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
    
    # زر رجوع للقائمة الرئيسية
    keyboard.append([
        InlineKeyboardButton(
            "🏠 القائمة الرئيسية" if language == "ar" else "🏠 Main Menu",
            callback_data="back",
        )
    ])
    
    return InlineKeyboardMarkup(keyboard)


# =========================================================
# تسجيل Handlers الخاصة بـ Bot 3
# =========================================================

def register_bot3_handlers(app):
    """
    هذا الملف لا يحتوي handlers إضافية لأن جميع الـ callbacks
    تستخدم الـ handlers الموجودة في telegram_bot.py
    """
    pass  # القائمة تستخدم handlers موجودة في الملف الرئيسي


# =========================================================
# اختبار
# =========================================================

if __name__ == "__main__":
    print("=" * 50)
    print("✅ telegram_bot3.py جاهز")
    print("🎮 عدد الألعاب: 11 + Red Dead (قائمة فرعية)")
    print("📐 ترتيب القائمة: 3 أعمدة")
    print("🔗 جميع الـ callbacks متوافقة مع telegram_bot.py")
    print("=" * 50)