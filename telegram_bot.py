import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")


# =========================
# معلومات الألعاب
# =========================

games = {

    "minecraft": {
        "name": "Minecraft",
        "emoji": "⛏️",
        "ar": {
            "description": "لعبة بناء ومغامرات وبقاء في عالم مفتوح.",
            "developer": "Mojang Studios",
            "release": "18 نوفمبر 2011",
            "genre": "بقاء، مغامرات، بناء",
            "platforms": "PC، PlayStation، Xbox، Nintendo Switch، الجوال"
        },
        "en": {
            "description": "A sandbox game focused on building, survival and adventure.",
            "developer": "Mojang Studios",
            "release": "November 18, 2011",
            "genre": "Survival, Adventure, Sandbox",
            "platforms": "PC, PlayStation, Xbox, Nintendo Switch, Mobile"
        }
    },


    "roblox": {
        "name": "Roblox",
        "emoji": "🎮",
        "ar": {
            "description": "منصة ألعاب تتيح للمستخدمين لعب وصناعة تجارب مختلفة.",
            "developer": "Roblox Corporation",
            "release": "1 سبتمبر 2006",
            "genre": "منصة ألعاب، اجتماعية",
            "platforms": "PC، Xbox، PlayStation، الجوال"
        },
        "en": {
            "description": "An online platform where users can play and create different experiences.",
            "developer": "Roblox Corporation",
            "release": "September 1, 2006",
            "genre": "Gaming Platform, Social",
            "platforms": "PC, Xbox, PlayStation, Mobile"
        }
    },


    "fortnite": {
        "name": "Fortnite",
        "emoji": "🚌",
        "ar": {
            "description": "لعبة أونلاين تجمع بين القتال والبناء والاستكشاف.",
            "developer": "Epic Games",
            "release": "25 يوليو 2017",
            "genre": "باتل رويال، أكشن، بناء",
            "platforms": "PC، PlayStation، Xbox، Nintendo Switch، الجوال"
        },
        "en": {
            "description": "An online game combining combat, building and exploration.",
            "developer": "Epic Games",
            "release": "July 25, 2017",
            "genre": "Battle Royale, Action, Building",
            "platforms": "PC, PlayStation, Xbox, Nintendo Switch, Mobile"
        }
    },


    "valorant": {
        "name": "Valorant",
        "emoji": "🎯",
        "ar": {
            "description": "لعبة تصويب تكتيكية تنافسية تعتمد على الشخصيات والقدرات.",
            "developer": "Riot Games",
            "release": "2 يونيو 2020",
            "genre": "تصويب تكتيكي، تنافسية",
            "platforms": "PC، PlayStation، Xbox"
        },
        "en": {
            "description": "A competitive tactical shooter featuring unique agents and abilities.",
            "developer": "Riot Games",
            "release": "June 2, 2020",
            "genre": "Tactical Shooter, Competitive",
            "platforms": "PC, PlayStation, Xbox"
        }
    },


    "rocketleague": {
        "name": "Rocket League",
        "emoji": "🏎️",
        "ar": {
            "description": "لعبة رياضية تجمع بين كرة القدم والسيارات السريعة.",
            "developer": "Psyonix",
            "release": "7 يوليو 2015",
            "genre": "رياضة، سيارات، تنافسية",
            "platforms": "PC، PlayStation، Xbox، Nintendo Switch"
        },
        "en": {
            "description": "A competitive sports game combining soccer with rocket-powered cars.",
            "developer": "Psyonix",
            "release": "July 7, 2015",
            "genre": "Sports, Racing, Competitive",
            "platforms": "PC, PlayStation, Xbox, Nintendo Switch"
        }
    },


    "brawlstars": {
        "name": "Brawl Stars",
        "emoji": "⭐",
        "ar": {
            "description": "لعبة أكشن متعددة اللاعبين تضم شخصيات وأنماط لعب مختلفة.",
            "developer": "Supercell",
            "release": "12 ديسمبر 2018",
            "genre": "أكشن، متعددة اللاعبين",
            "platforms": "Android، iOS"
        },
        "en": {
            "description": "A multiplayer action game featuring different characters and game modes.",
            "developer": "Supercell",
            "release": "December 12, 2018",
            "genre": "Action, Multiplayer",
            "platforms": "Android, iOS"
        }
    }

}


# =========================
# قائمة الألعاب
# =========================

def get_game_buttons():

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "⛏️ Minecraft",
                callback_data="minecraft"
            )
        ],

        [
            InlineKeyboardButton(
                "🎮 Roblox",
                callback_data="roblox"
            )
        ],

        [
            InlineKeyboardButton(
                "🚌 Fortnite",
                callback_data="fortnite"
            )
        ],

        [
            InlineKeyboardButton(
                "🎯 Valorant",
                callback_data="valorant"
            )
        ],

        [
            InlineKeyboardButton(
                "🏎️ Rocket League",
                callback_data="rocketleague"
            )
        ],

        [
            InlineKeyboardButton(
                "⭐ Brawl Stars",
                callback_data="brawlstars"
            )
        ]

    ])


# =========================
# البداية
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "🇸🇦 العربية",
                callback_data="language_ar"
            ),

            InlineKeyboardButton(
                "🇺🇸 English",
                callback_data="language_en"
            )
        ]

    ])

    await update.message.reply_text(

        "👋 أهلاً بك في بوت معلومات الألعاب!\n\n"
        "اختر اللغة / Choose your language:",

        reply_markup=keyboard

    )


# =========================
# اختيار اللغة
# =========================

async def choose_language(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    language = query.data.replace(
        "language_",
        ""
    )

    context.user_data["language"] = language

    if language == "ar":

        text = (
            "🎮 اختر اللعبة التي تريد معرفة معلومات عنها:"
        )

    else:

        text = (
            "🎮 Choose a game to get information about:"
        )

    await query.edit_message_text(

        text,

        reply_markup=get_game_buttons()

    )


# =========================
# عرض معلومات اللعبة
# =========================

async def show_game(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    game_id = query.data

    if game_id not in games:

        await query.edit_message_text(
            "❌ اللعبة غير موجودة."
        )

        return

    game = games[game_id]

    language = context.user_data.get(
        "language",
        "ar"
    )

    info = game[language]


    if language == "ar":

        text = (

            f"{game['emoji']} *{game['name']}*\n\n"

            f"📖 *الوصف:*\n"
            f"{info['description']}\n\n"

            f"👨‍💻 *المطور:*\n"
            f"{info['developer']}\n\n"

            f"📅 *تاريخ الإصدار:*\n"
            f"{info['release']}\n\n"

            f"🎯 *النوع:*\n"
            f"{info['genre']}\n\n"

            f"💻 *المنصات:*\n"
            f"{info['platforms']}"

        )

        back_text = "🔙 رجوع"


    else:

        text = (

            f"{game['emoji']} *{game['name']}*\n\n"

            f"📖 *Description:*\n"
            f"{info['description']}\n\n"

            f"👨‍💻 *Developer:*\n"
            f"{info['developer']}\n\n"

            f"📅 *Release Date:*\n"
            f"{info['release']}\n\n"

            f"🎯 *Genre:*\n"
            f"{info['genre']}\n\n"

            f"💻 *Platforms:*\n"
            f"{info['platforms']}"

        )

        back_text = "🔙 Back"


    keyboard = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                back_text,
                callback_data="back"
            )
        ]

    ])


    await query.edit_message_text(

        text,

        parse_mode="Markdown",

        reply_markup=keyboard

    )


# =========================
# الرجوع
# =========================

async def back(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    language = context.user_data.get(
        "language",
        "ar"
    )

    if language == "ar":

        text = (
            "🎮 اختر اللعبة التي تريد معرفة معلومات عنها:"
        )

    else:

        text = (
            "🎮 Choose a game to get information about:"
        )

    await query.edit_message_text(

        text,

        reply_markup=get_game_buttons()

    )


# =========================
# تشغيل البوت
# =========================

def main():

    if not TOKEN:

        print(
            "❌ TELEGRAM_BOT_TOKEN غير موجود في Secrets"
        )

        return


    app = Application.builder().token(
        TOKEN
    ).build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            choose_language,
            pattern=r"^language_(ar|en)$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            show_game,
            pattern=r"^(minecraft|roblox|fortnite|valorant|rocketleague|brawlstars)$"
        )
    )


    app.add_handler(
        CallbackQueryHandler(
            back,
            pattern=r"^back$"
        )
    )


    print("🤖 البوت يعمل الآن...")


    app.run_polling()


if __name__ == "__main__":
    main()