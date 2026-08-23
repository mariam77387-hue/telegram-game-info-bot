# telegram_bot3.py
#
# =========================================================
# Bot 3 - قائمة الألعاب المنظمة
# =========================================================

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


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
# القائمة الرئيسية - 3 ألعاب في كل صف
# =========================================================

def new_main_menu(language="ar"):
    
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
    
    # الألعاب - 3 أزرار في كل صف
    for game_id, emoji, name in game_list:
        row.append(
            InlineKeyboardButton(
                f"{emoji} {name}",
                callback_data=game_id,
            )
        )
        if len(row) == 3:
            keyboard.append(row)
            row = []
    
    if row:
        keyboard.append(row)
    
    # Red Dead
    keyboard.append([
        InlineKeyboardButton(
            "🤠 Red Dead",
            callback_data="red_dead",
        )
    ])
    
    # الأدوات
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
    
    # ملاحظة: حذفت زر "🏠 القائمة الرئيسية" لأنه ما له داعي هنا
    
    return InlineKeyboardMarkup(keyboard)


# =========================================================
# Handlers
# =========================================================

def register_bot3_handlers(app):
    # جميع الـ callbacks تتعامل معها telegram_bot.py
    pass


# =========================================================
# اختبار
# =========================================================

if __name__ == "__main__":
    print("=" * 50)
    print("✅ telegram_bot3.py جاهز")
    print("🎮 الألعاب: 11")
    print("🤠 Red Dead: جاهز")
    print("📐 القائمة: 3 ألعاب في كل صف")
    print("🔗 متوافق مع telegram_bot.py")
    print("=" * 50)