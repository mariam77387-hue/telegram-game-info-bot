# telegram_bot3.py
#
# =========================================================
# Telegram Bot 3
# قائمة الألعاب المنظمة + الاستكشاف
# =========================================================

import random

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import CallbackQueryHandler


# =========================================================
# الألعاب
# =========================================================

BOT3_GAMES = {
    "minecraft": {
        "name": "Minecraft",
        "emoji": "⛏️",
        "description": "لعبة بناء ومغامرات وبقاء في عالم مفتوح.",
        "genre": "بقاء، مغامرات، بناء",
    },

    "roblox": {
        "name": "Roblox",
        "emoji": "🎮",
        "description": "منصة ألعاب تتيح للمستخدمين لعب وصناعة تجارب مختلفة.",
        "genre": "منصة ألعاب، اجتماعية",
    },

    "fortnite": {
        "name": "Fortnite",
        "emoji": "🚌",
        "description": "لعبة أونلاين تجمع بين القتال والبناء والاستكشاف.",
        "genre": "باتل رويال، أكشن",
    },

    "valorant": {
        "name": "Valorant",
        "emoji": "🎯",
        "description": "لعبة تصويب تكتيكية تنافسية.",
        "genre": "تصويب تكتيكي",
    },

    "rocketleague": {
        "name": "Rocket League",
        "emoji": "🏎️",
        "description": "لعبة رياضية تجمع بين كرة القدم والسيارات.",
        "genre": "رياضة، سيارات",
    },

    "brawlstars": {
        "name": "Brawl Stars",
        "emoji": "⭐",
        "description": "لعبة أكشن متعددة اللاعبين.",
        "genre": "أكشن، متعددة اللاعبين",
    },

    "gtav": {
        "name": "GTA V",
        "emoji": "🚗",
        "description": "لعبة أكشن ومغامرات في عالم مفتوح.",
        "genre": "أكشن، عالم مفتوح",
    },

    "genshinimpact": {
        "name": "Genshin Impact",
        "emoji": "✨",
        "description": "لعبة أكشن وتقمص أدوار بعالم مفتوح.",
        "genre": "أكشن، RPG",
    },

    "clashroyale": {
        "name": "Clash Royale",
        "emoji": "👑",
        "description": "لعبة استراتيجية تعتمد على البطاقات.",
        "genre": "استراتيجية، بطاقات",
    },

    "overwatch": {
        "name": "Overwatch",
        "emoji": "🦸",
        "description": "لعبة تصويب جماعية تنافسية.",
        "genre": "تصويب، جماعية",
    },

    "eldenring": {
        "name": "Elden Ring",
        "emoji": "⚔️",
        "description": "لعبة أكشن وتقمص أدوار بعالم مفتوح.",
        "genre": "أكشن، RPG",
    },
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
# القائمة الرئيسية لـ Bot 3
# =========================================================

def bot3_menu_markup(language):

    if language == "ar":

        keyboard = [

            [
                InlineKeyboardButton(
                    "⛏️ Minecraft",
                    callback_data="bot3_game_minecraft",
                )
            ],

            [
                InlineKeyboardButton(
                    "🎮 Roblox",
                    callback_data="bot3_game_roblox",
                )
            ],

            [
                InlineKeyboardButton(
                    "🚌 Fortnite",
                    callback_data="bot3_game_fortnite",
                )
            ],

            [
                InlineKeyboardButton(
                    "🎯 Valorant",
                    callback_data="bot3_game_valorant",
                )
            ],

            [
                InlineKeyboardButton(
                    "🏎️ Rocket League",
                    callback_data="bot3_game_rocketleague",
                )
            ],

            [
                InlineKeyboardButton(
                    "⭐ Brawl Stars",
                    callback_data="bot3_game_brawlstars",
                )
            ],

            [
                InlineKeyboardButton(
                    "🚗 GTA V",
                    callback_data="bot3_game_gtav",
                )
            ],

            [
                InlineKeyboardButton(
                    "✨ Genshin Impact",
                    callback_data="bot3_game_genshinimpact",
                )
            ],

            [
                InlineKeyboardButton(
                    "👑 Clash Royale",
                    callback_data="bot3_game_clashroyale",
                )
            ],

            [
                InlineKeyboardButton(
                    "🦸 Overwatch",
                    callback_data="bot3_game_overwatch",
                )
            ],

            [
                InlineKeyboardButton(
                    "⚔️ Elden Ring",
                    callback_data="bot3_game_eldenring",
                )
            ],

            [
                InlineKeyboardButton(
                    "🤠 Red Dead",
                    callback_data="bot3_red_dead",
                )
            ],

            [
                InlineKeyboardButton(
                    "✨ استكشف الألعاب",
                    callback_data="bot3_explore",
                )
            ],

            [
                InlineKeyboardButton(
                    "🏠 القائمة الرئيسية",
                    callback_data="back",
                )
            ],
        ]

    else:

        keyboard = [

            [
                InlineKeyboardButton(
                    "⛏️ Minecraft",
                    callback_data="bot3_game_minecraft",
                )
            ],

            [
                InlineKeyboardButton(
                    "🎮 Roblox",
                    callback_data="bot3_game_roblox",
                )
            ],

            [
                InlineKeyboardButton(
                    "🚌 Fortnite",
                    callback_data="bot3_game_fortnite",
                )
            ],

            [
                InlineKeyboardButton(
                    "🎯 Valorant",
                    callback_data="bot3_game_valorant",
                )
            ],

            [
                InlineKeyboardButton(
                    "🏎️ Rocket League",
                    callback_data="bot3_game_rocketleague",
                )
            ],

            [
                InlineKeyboardButton(
                    "⭐ Brawl Stars",
                    callback_data="bot3_game_brawlstars",
                )
            ],

            [
                InlineKeyboardButton(
                    "🚗 GTA V",
                    callback_data="bot3_game_gtav",
                )
            ],

            [
                InlineKeyboardButton(
                    "✨ Genshin Impact",
                    callback_data="bot3_game_genshinimpact",
                )
            ],

            [
                InlineKeyboardButton(
                    "👑 Clash Royale",
                    callback_data="bot3_game_clashroyale",
                )
            ],

            [
                InlineKeyboardButton(
                    "🦸 Overwatch",
                    callback_data="bot3_game_overwatch",
                )
            ],

            [
                InlineKeyboardButton(
                    "⚔️ Elden Ring",
                    callback_data="bot3_game_eldenring",
                )
            ],

            [
                InlineKeyboardButton(
                    "🤠 Red Dead",
                    callback_data="bot3_red_dead",
                )
            ],

            [
                InlineKeyboardButton(
                    "✨ Explore Games",
                    callback_data="bot3_explore",
                )
            ],

            [
                InlineKeyboardButton(
                    "🏠 Main Menu",
                    callback_data="back",
                )
            ],
        ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# نص القائمة
# =========================================================

def bot3_menu_text(language):

    if language == "ar":

        return (
            "🎮 *مركز الألعاب*\n\n"
            "اختر لعبة من القائمة بالأسفل 👇"
        )

    return (
        "🎮 *Gaming Center*\n\n"
        "Choose a game from the list below 👇"
    )


# =========================================================
# فتح القائمة
# =========================================================

async def open_bot3_menu(
    update,
    context,
):

    query = update.callback_query

    await query.answer()

    language = get_language(
        context
    )

    await query.edit_message_text(
        bot3_menu_text(language),
        parse_mode="Markdown",
        reply_markup=bot3_menu_markup(
            language
        ),
    )


# =========================================================
# معلومات اللعبة
# =========================================================

async def bot3_game_info(
    update,
    context,
):

    query = update.callback_query

    await query.answer()

    game_id = query.data.replace(
        "bot3_game_",
        "",
    )

    if game_id not in BOT3_GAMES:

        await query.edit_message_text(
            "❌ اللعبة غير موجودة."
        )

        return

    language = get_language(
        context
    )

    game = BOT3_GAMES[game_id]

    if language == "ar":

        text = (
            f"{game['emoji']} *{game['name']}*\n\n"
            f"📖 *الوصف:*\n"
            f"{game['description']}\n\n"
            f"🎯 *النوع:*\n"
            f"{game['genre']}"
        )

        back_text = "🔙 رجوع"

    else:

        text = (
            f"{game['emoji']} *{game['name']}*\n\n"
            f"📖 *Description:*\n"
            f"{game['description']}\n\n"
            f"🎯 *Genre:*\n"
            f"{game['genre']}"
        )

        back_text = "🔙 Back"

    keyboard = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                back_text,
                callback_data="bot3_menu",
            )
        ],

    ])

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


# =========================================================
# استكشاف الألعاب
# =========================================================

async def explore_games(
    update,
    context,
):

    query = update.callback_query

    await query.answer()

    language = get_language(
        context
    )

    game_id = random.choice(
        list(BOT3_GAMES.keys())
    )

    context.user_data[
        "bot3_discovered_game"
    ] = game_id

    game = BOT3_GAMES[game_id]

    if language == "ar":

        text = (
            "✨ *اكتشف لعبة*\n\n"
            f"{game['emoji']} *{game['name']}*\n\n"
            f"🎯 النوع: {game['genre']}\n\n"
            f"📖 {game['description']}\n\n"
            "يمكن تكون لعبتك القادمة! 🎮"
        )

        another = "🔄 لعبة ثانية"
        back = "🔙 رجوع"

    else:

        text = (
            "✨ *Discover a Game*\n\n"
            f"{game['emoji']} *{game['name']}*\n\n"
            f"🎯 Genre: {game['genre']}\n\n"
            f"📖 {game['description']}\n\n"
            "Maybe this could be your next game! 🎮"
        )

        another = "🔄 Another Game"
        back = "🔙 Back"

    keyboard = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                another,
                callback_data="bot3_explore",
            )
        ],

        [
            InlineKeyboardButton(
                back,
                callback_data="bot3_menu",
            )
        ],

    ])

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


# =========================================================
# Red Dead
# =========================================================

async def bot3_red_dead(
    update,
    context,
):

    query = update.callback_query

    await query.answer()

    language = get_language(
        context
    )

    if language == "ar":

        text = (
            "🤠 *Red Dead*\n\n"
            "اختر اللعبة:"
        )

        back = "🔙 رجوع"

    else:

        text = (
            "🤠 *Red Dead*\n\n"
            "Choose a game:"
        )

        back = "🔙 Back"

    keyboard = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "🤠 Red Dead Redemption",
                callback_data="bot3_game_reddeadredemption",
            )
        ],

        [
            InlineKeyboardButton(
                "🤠 Red Dead Redemption 2",
                callback_data="bot3_game_reddeadredemption2",
            )
        ],

        [
            InlineKeyboardButton(
                back,
                callback_data="bot3_menu",
            )
        ],

    ])

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


# =========================================================
# تسجيل Handlers
# =========================================================

def register_bot3_handlers(app):

    # فتح Bot 3
    app.add_handler(
        CallbackQueryHandler(
            open_bot3_menu,
            pattern=r"^bot3_menu$",
        )
    )

    # الألعاب
    app.add_handler(
        CallbackQueryHandler(
            bot3_game_info,
            pattern=(
                r"^bot3_game_"
                r"(minecraft|roblox|fortnite|"
                r"valorant|rocketleague|"
                r"brawlstars|gtav|genshinimpact|"
                r"clashroyale|overwatch|eldenring|"
                r"reddeadredemption|reddeadredemption2)$"
            ),
        )
    )

    # اكتشاف
    app.add_handler(
        CallbackQueryHandler(
            explore_games,
            pattern=r"^bot3_explore$",
        )
    )

    # Red Dead
    app.add_handler(
        CallbackQueryHandler(
            bot3_red_dead,
            pattern=r"^bot3_red_dead$",
        )
    )


# =========================================================
# اختبار
# =========================================================

if __name__ == "__main__":

    print("=================================")
    print("✅ telegram_bot3.py جاهز")
    print(f"🎮 الألعاب: {len(BOT3_GAMES)}")
    print("✨ استكشاف الألعاب: جاهز")
    print("🤠 Red Dead: جاهز")
    print("=================================")