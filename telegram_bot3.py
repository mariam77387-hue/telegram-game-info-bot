# telegram_bot3.py
#
# قائمة الألعاب الجديدة والمنظمة
# --------------------------------
# هذا الملف مسؤول عن:
# 🎮 قائمة الألعاب
# 🏆 تحدي الألعاب
# 🎲 اكتشف لعبة
# 🔎 بحث عن لعبة
# ➕ طلب لعبة
#
# ملاحظة:
# إذا كان عندك telegram_bot.py هو الملف الرئيسي،
# تقدر تستورد منه الدوال الموجودة في هذا الملف.
import random
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
# =========================================================
# الألعاب
# =========================================================
games = {
    "minecraft": {
        "name": "Minecraft",
        "emoji": "⛏️",
        "rating": "93/100",
        "description": "لعبة بناء ومغامرات وبقاء في عالم مفتوح.",
        "developer": "Mojang Studios",
        "release": "18 نوفمبر 2011",
        "genre": "بقاء، مغامرات، بناء",
        "platforms": "PC، PlayStation، Xbox، Nintendo Switch، الجوال",
    },
    "roblox": {
        "name": "Roblox",
        "emoji": "🎮",
        "rating": "غير محدد",
        "description": "منصة ألعاب تتيح للمستخدمين لعب وصناعة تجارب مختلفة.",
        "developer": "Roblox Corporation",
        "release": "1 سبتمبر 2006",
        "genre": "منصة ألعاب، اجتماعية",
        "platforms": "PC، Xbox، PlayStation، الجوال",
    },
    "fortnite": {
        "name": "Fortnite",
        "emoji": "🚌",
        "rating": "83/100",
        "description": "لعبة أونلاين تجمع بين القتال والبناء والاستكشاف.",
        "developer": "Epic Games",
        "release": "25 يوليو 2017",
        "genre": "باتل رويال، أكشن، بناء",
        "platforms": "PC، PlayStation، Xbox، Nintendo Switch، الجوال",
    },
    "valorant": {
        "name": "Valorant",
        "emoji": "🎯",
        "rating": "80/100",
        "description": "لعبة تصويب تكتيكية تنافسية تعتمد على الشخصيات والقدرات.",
        "developer": "Riot Games",
        "release": "2 يونيو 2020",
        "genre": "تصويب تكتيكي، تنافسية",
        "platforms": "PC، PlayStation، Xbox",
    },
    "rocketleague": {
        "name": "Rocket League",
        "emoji": "🏎️",
        "rating": "86/100",
        "description": "لعبة رياضية تجمع بين كرة القدم والسيارات السريعة.",
        "developer": "Psyonix",
        "release": "7 يوليو 2015",
        "genre": "رياضة، سيارات، تنافسية",
        "platforms": "PC، PlayStation، Xbox، Nintendo Switch",
    },
    "brawlstars": {
        "name": "Brawl Stars",
        "emoji": "⭐",
        "rating": "82/100",
        "description": "لعبة أكشن متعددة اللاعبين تضم شخصيات وأنماط لعب مختلفة.",
        "developer": "Supercell",
        "release": "12 ديسمبر 2018",
        "genre": "أكشن، متعددة اللاعبين",
        "platforms": "Android، iOS",
    },
    "gtav": {
        "name": "GTA V",
        "emoji": "🚗",
        "rating": "97/100",
        "description": "لعبة أكشن ومغامرات في عالم مفتوح تدور أحداثها في لوس سانتوس.",
        "developer": "Rockstar Games",
        "release": "17 سبتمبر 2013",
        "genre": "أكشن، مغامرات، عالم مفتوح",
        "platforms": "PC، PlayStation، Xbox",
    },
    "genshinimpact": {
        "name": "Genshin Impact",
        "emoji": "✨",
        "rating": "84/100",
        "description": "لعبة تقمص أدوار وأكشن بعالم مفتوح مليء بالاستكشاف.",
        "developer": "HoYoverse",
        "release": "28 سبتمبر 2020",
        "genre": "أكشن، تقمص أدوار، عالم مفتوح",
        "platforms": "PC، PlayStation، Android، iOS",
    },
    "clashroyale": {
        "name": "Clash Royale",
        "emoji": "👑",
        "rating": "80/100",
        "description": "لعبة استراتيجية في الوقت الحقيقي تعتمد على البطاقات.",
        "developer": "Supercell",
        "release": "2 مارس 2016",
        "genre": "استراتيجية، بطاقات، تنافسية",
        "platforms": "Android، iOS",
    },
    "overwatch": {
        "name": "Overwatch",
        "emoji": "🦸",
        "rating": "91/100",
        "description": "لعبة تصويب جماعية تنافسية تعتمد على شخصيات وقدرات مختلفة.",
        "developer": "Blizzard Entertainment",
        "release": "24 مايو 2016",
        "genre": "تصويب، أكشن، جماعية",
        "platforms": "PC، PlayStation، Xbox، Nintendo Switch",
    },
    "eldenring": {
        "name": "Elden Ring",
        "emoji": "⚔️",
        "rating": "96/100",
        "description": "لعبة أكشن وتقمص أدوار بعالم مفتوح مليء بالاستكشاف.",
        "developer": "FromSoftware",
        "release": "25 فبراير 2022",
        "genre": "أكشن، تقمص أدوار، عالم مفتوح",
        "platforms": "PC، PlayStation، Xbox",
    },
    "reddeadredemption": {
        "name": "Red Dead Redemption",
        "emoji": "🤠",
        "rating": "95/100",
        "description": "لعبة أكشن ومغامرات في الغرب الأمريكي.",
        "developer": "Rockstar San Diego",
        "release": "18 مايو 2010",
        "genre": "أكشن، مغامرات، عالم مفتوح",
        "platforms": "PlayStation، Xbox، Nintendo Switch، PC",
    },
    "reddeadredemption2": {
        "name": "Red Dead Redemption 2",
        "emoji": "🤠",
        "rating": "97/100",
        "description": "مغامرة ملحمية في الغرب الأمريكي تتبع قصة عصابة Van der Linde.",
        "developer": "Rockstar Studios",
        "release": "26 أكتوبر 2018",
        "genre": "أكشن، مغامرات، عالم مفتوح",
        "platforms": "PC، PlayStation، Xbox",
    },
}
# =========================================================
# الأسماء البديلة
# =========================================================
ALIASES = {
    "minecraft": "minecraft",
    "ماينكرافت": "minecraft",
    "roblox": "roblox",
    "روبلوكس": "roblox",
    "fortnite": "fortnite",
    "فورتنايت": "fortnite",
    "valorant": "valorant",
    "فالورانت": "valorant",
    "rocket league": "rocketleague",
    "روكيت ليق": "rocketleague",
    "brawl stars": "brawlstars",
    "براول ستارز": "brawlstars",
    "gta v": "gtav",
    "gta 5": "gtav",
    "gta": "gtav",
    "gta ٥": "gtav",
    "genshin impact": "genshinimpact",
    "genshin": "genshinimpact",
    "clash royale": "clashroyale",
    "overwatch": "overwatch",
    "elden ring": "eldenring",
    "red dead": "reddeadredemption",
    "red dead redemption": "reddeadredemption",
    "red dead redemption 2": "reddeadredemption2",
}
# =========================================================
# اللغة
# =========================================================
def get_language(context):
    return context.user_data.get(
        "language",
        "ar",
    )
# =========================================================
# النص الرئيسي
# =========================================================
def main_menu_text(language):
    if language == "ar":
        return (
            "🎮 *ألعاب قيمنق*\n\n"
            "اختر لعبة لمعرفة معلومات عنها، "
            "أو استخدم إحدى الميزات الموجودة بالأسفل."
        )
    return (
        "🎮 *Gaming Games*\n\n"
        "Choose a game to view its information, "
        "or use one of the features below."
    )
# =========================================================
# القائمة الجديدة
# =========================================================
def new_main_menu(language="ar"):
    keyboard = []
    # -----------------------------------------------------
    # الألعاب
    # -----------------------------------------------------
    game_ids = [
        "minecraft",
        "roblox",
        "fortnite",
        "valorant",
        "rocketleague",
        "brawlstars",
        "gtav",
        "genshinimpact",
        "clashroyale",
        "overwatch",
        "eldenring",
    ]
    for game_id in game_ids:
        game = games[game_id]
        keyboard.append([
            InlineKeyboardButton(
                f"{game['emoji']} {game['name']}",
                callback_data=f"game_{game_id}",
            )
        ])
    # -----------------------------------------------------
    # Red Dead
    # -----------------------------------------------------
    keyboard.append([
        InlineKeyboardButton(
            "🤠 Red Dead",
            callback_data="red_dead_menu",
        )
    ])
    # -----------------------------------------------------
    # فاصل بصري
    # -----------------------------------------------------
    # تحدي الألعاب يكون بارزًا
    keyboard.append([
        InlineKeyboardButton(
            "🏆 🧠 تحدي الألعاب",
            callback_data="quiz_start",
        )
    ])
    # -----------------------------------------------------
    # استكشف
    # -----------------------------------------------------
    if language == "ar":
        keyboard.append([
            InlineKeyboardButton(
                "✨ استكشف",
                callback_data="explore_menu",
            )
        ])
    else:
        keyboard.append([
            InlineKeyboardButton(
                "✨ Explore",
                callback_data="explore_menu",
            )
        ])
    # -----------------------------------------------------
    # طلب لعبة
    # -----------------------------------------------------
    keyboard.append([
        InlineKeyboardButton(
            "💡 طلب لعبة"
            if language == "ar"
            else "💡 Request a Game",
            callback_data="request_game",
        )
    ])
    return InlineKeyboardMarkup(
        keyboard
    )
# =========================================================
# قائمة الاستكشاف
# =========================================================
def explore_menu(language):
    if language == "ar":
        keyboard = [
            [
                InlineKeyboardButton(
                    "🎲 اكتشف لعبة",
                    callback_data="discover_game",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔎 بحث عن لعبة",
                    callback_data="search_game",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 رجوع",
                    callback_data="back",
                )
            ],
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton(
                    "🎲 Discover a Game",
                    callback_data="discover_game",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔎 Search for a Game",
                    callback_data="search_game",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="back",
                )
            ],
        ]
    return InlineKeyboardMarkup(
        keyboard
    )
# =========================================================
# قائمة Red Dead
# =========================================================
def red_dead_menu(language):
    if language == "ar":
        keyboard = [
            [
                InlineKeyboardButton(
                    "🤠 Red Dead Redemption",
                    callback_data="game_reddeadredemption",
                )
            ],
            [
                InlineKeyboardButton(
                    "🤠 Red Dead Redemption 2",
                    callback_data="game_reddeadredemption2",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 رجوع",
                    callback_data="back",
                )
            ],
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton(
                    "🤠 Red Dead Redemption",
                    callback_data="game_reddeadredemption",
                )
            ],
            [
                InlineKeyboardButton(
                    "🤠 Red Dead Redemption 2",
                    callback_data="game_reddeadredemption2",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="back",
                )
            ],
        ]
    return InlineKeyboardMarkup(
        keyboard
    )
# =========================================================
# معلومات اللعبة
# =========================================================
def game_info_text(
    game_id,
    language,
):
    game = games[game_id]
    if language == "ar":
        return (
            f"{game['emoji']} *{game['name']}*\n\n"
            f"📖 *الوصف:*\n"
            f"{game['description']}\n\n"
            f"👨‍💻 *المطور:*\n"
            f"{game['developer']}\n\n"
            f"📅 *تاريخ الإصدار:*\n"
            f"{game['release']}\n\n"
            f"🎯 *النوع:*\n"
            f"{game['genre']}\n\n"
            f"💻 *المنصات:*\n"
            f"{game['platforms']}\n\n"
            f"⭐ *التقييم:*\n"
            f"{game['rating']}"
        )
    return (
        f"{game['emoji']} *{game['name']}*\n\n"
        f"📖 *Description:*\n"
        f"{game['description']}\n\n"
        f"👨‍💻 *Developer:*\n"
        f"{game['developer']}\n\n"
        f"📅 *Release Date:*\n"
        f"{game['release']}\n\n"
        f"🎯 *Genre:*\n"
        f"{game['genre']}\n\n"
        f"💻 *Platforms:*\n"
        f"{game['platforms']}\n\n"
        f"⭐ *Rating:*\n"
        f"{game['rating']}"
    )
# =========================================================
# زر الرجوع
# =========================================================
def back_button(language):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔙 رجوع"
                if language == "ar"
                else "🔙 Back",
                callback_data="back",
            )
        ]
    ])
# =========================================================
# اكتشف لعبة
# =========================================================
def discover_game_id(context):
    available = list(games.keys())
    previous = context.user_data.get(
        "last_discovered_game"
    )
    if (
        previous in available
        and len(available) > 1
    ):
        available.remove(previous)
    game_id = random.choice(
        available
    )
    context.user_data[
        "last_discovered_game"
    ] = game_id
    return game_id
def discover_text(
    game_id,
    language,
):
    game = games[game_id]
    if language == "ar":
        return (
            "🎲 *اكتشف لعبة*\n\n"
            f"{game['emoji']} *{game['name']}*\n\n"
            f"🎯 النوع: {game['genre']}\n"
            f"💻 المنصات: {game['platforms']}\n"
            f"⭐ التقييم: {game['rating']}\n\n"
            "✨ يمكن تكون لعبتك القادمة!"
        )
    return (
        "🎲 *Discover a Game*\n\n"
        f"{game['emoji']} *{game['name']}*\n\n"
        f"🎯 Genre: {game['genre']}\n"
        f"💻 Platforms: {game['platforms']}\n"
        f"⭐ Rating: {game['rating']}\n\n"
        "✨ Maybe this could be your next game!"
    )
def discover_markup(language):
    if language == "ar":
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🎲 لعبة ثانية",
                    callback_data="discover_game",
                )
            ],
            [
                InlineKeyboardButton(
                    "📖 معلومات اللعبة",
                    callback_data="discover_info",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 رجوع",
                    callback_data="back",
                )
            ],
        ])
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🎲 Another Game",
                callback_data="discover_game",
            )
        ],
        [
            InlineKeyboardButton(
                "📖 Game Information",
                callback_data="discover_info",
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="back",
            )
        ],
    ])
# =========================================================
# Handlers
# =========================================================
async def show_new_menu(
    update,
    context,
):
    language = get_language(
        context
    )
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(
            main_menu_text(language),
            parse_mode="Markdown",
            reply_markup=new_main_menu(
                language
            ),
        )
        return
    if update.message:
        await update.message.reply_text(
            main_menu_text(language),
            parse_mode="Markdown",
            reply_markup=new_main_menu(
                language
            ),
        )
async def open_explore_menu(
    update,
    context,
):
    query = update.callback_query
    await query.answer()
    language = get_language(
        context
    )
    text = (
        "✨ *استكشف الألعاب*\n\n"
        "اختر الطريقة التي تريد استكشاف الألعاب بها:"
        if language == "ar"
        else
        "✨ *Explore Games*\n\n"
        "Choose how you want to explore games:"
    )
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=explore_menu(
            language
        ),
    )
async def open_red_dead_menu(
    update,
    context,
):
    query = update.callback_query
    await query.answer()
    language = get_language(
        context
    )
    text = (
        "🤠 *Red Dead*\n\n"
        "اختر اللعبة:"
        if language == "ar"
        else
        "🤠 *Red Dead*\n\n"
        "Choose a game:"
    )
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=red_dead_menu(
            language
        ),
    )
async def show_new_game(
    update,
    context,
):
    query = update.callback_query
    await query.answer()
    game_id = query.data.replace(
        "game_",
        "",
    )
    if game_id not in games:
        await query.edit_message_text(
            "❌ اللعبة غير موجودة."
        )
        return
    language = get_language(
        context
    )
    await query.edit_message_text(
        game_info_text(
            game_id,
            language,
        ),
        parse_mode="Markdown",
        reply_markup=back_button(
            language
        ),
    )
async def discover_game(
    update,
    context,
):
    query = update.callback_query
    await query.answer()
    language = get_language(
        context
    )
    game_id = discover_game_id(
        context
    )
    await query.edit_message_text(
        discover_text(
            game_id,
            language,
        ),
        parse_mode="Markdown",
        reply_markup=discover_markup(
            language
        ),
    )
async def discover_info(
    update,
    context,
):
    query = update.callback_query
    await query.answer()
    language = get_language(
        context
    )
    game_id = context.user_data.get(
        "last_discovered_game"
    )
    if not game_id:
        game_id = discover_game_id(
            context
        )
    await query.edit_message_text(
        game_info_text(
            game_id,
            language,
        ),
        parse_mode="Markdown",
        reply_markup=back_button(
            language
        ),
    )
# =========================================================
# تسجيل الـ handlers
# =========================================================
def register_bot3_handlers(app):
    # القائمة الرئيسية
    app.add_handler(
        CallbackQueryHandler(
            show_new_menu,
            pattern=r"^bot3_menu$",
        )
    )
    # استكشف
    app.add_handler(
        CallbackQueryHandler(
            open_explore_menu,
            pattern=r"^explore_menu$",
        )
    )
    # Red Dead
    app.add_handler(
        CallbackQueryHandler(
            open_red_dead_menu,
            pattern=r"^red_dead_menu$",
        )
    )
    # الألعاب
    app.add_handler(
        CallbackQueryHandler(
            show_new_game,
            pattern=r"^game_(minecraft|roblox|fortnite|"
                    r"valorant|rocketleague|brawlstars|"
                    r"gtav|genshinimpact|clashroyale|"
                    r"overwatch|eldenring|"
                    r"reddeadredemption|reddeadredemption2)$",
        )
    )
    # اكتشف لعبة
    app.add_handler(
        CallbackQueryHandler(
            discover_game,
            pattern=r"^discover_game$",
        )
    )
    # معلومات اللعبة المكتشفة
    app.add_handler(
        CallbackQueryHandler(
            discover_info,
            pattern=r"^discover_info$",
        )
    )
# =========================================================
# دالة اختبار
# =========================================================
def test_menu():
    print(
        "✅ telegram.bot3.py جاهز."
    )
    print(
        f"🎮 عدد الألعاب: {len(games)}"
    )
    print(
        "🏆 تحدي الألعاب: جاهز للربط"
    )
    print(
        "✨ اكتشف لعبة: جاهز"
    )
    print(
        "🔎 بحث عن لعبة: جاهز للربط"
    )
    print(
        "💡 طلب لعبة: جاهز للربط"
    )
if __name__ == "__main__":
    test_menu()
