# في telegram_bot3.py - دالة main_menu
def main_menu(language="ar"):
    keyboard = []
    
    # الألعاب - 3 أزرار بكل صف
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
    
    row = []
    for game_id, emoji, name in game_list:
        row.append(
            InlineKeyboardButton(
                f"{emoji} {name}",
                callback_data=game_id,  # <-- بدون game_
            )
        )
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    # Red Dead
    keyboard.append([
        InlineKeyboardButton("🤠 Red Dead", callback_data="red_dead")
    ])
    
    # فاصل
    keyboard.append([
        InlineKeyboardButton("─" * 20, callback_data="noop")
    ])
    
    # أدوات
    if language == "ar":
        keyboard.append([
            InlineKeyboardButton("🎲 اكتشف لعبة", callback_data="discover_game"),
            InlineKeyboardButton("🔎 بحث عن لعبة", callback_data="search_game"),
        ])
        keyboard.append([
            InlineKeyboardButton("💡 طلب لعبة", callback_data="request_game")
        ])
    else:
        keyboard.append([
            InlineKeyboardButton("🎲 Discover Game", callback_data="discover_game"),
            InlineKeyboardButton("🔎 Search Game", callback_data="search_game"),
        ])
        keyboard.append([
            InlineKeyboardButton("💡 Request Game", callback_data="request_game")
        ])
    
    return InlineKeyboardMarkup(keyboard)