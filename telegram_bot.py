import os
import random
from datetime import datetime, timezone

import psycopg
from psycopg.rows import dict_row

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
DATABASE_URL = os.getenv("DATABASE_URL")


# =========================================================
# الألعاب
# =========================================================

games = {
    "minecraft": {
        "name": "Minecraft",
        "emoji": "⛏️",
        "rating": "93/100",
        "ar": {
            "description": "لعبة بناء ومغامرات وبقاء في عالم مفتوح.",
            "developer": "Mojang Studios",
            "release": "18 نوفمبر 2011",
            "genre": "بقاء، مغامرات، بناء",
            "platforms": "PC، PlayStation، Xbox، Nintendo Switch، الجوال",
        },
        "en": {
            "description": "A sandbox game focused on building, survival and adventure.",
            "developer": "Mojang Studios",
            "release": "November 18, 2011",
            "genre": "Survival, Adventure, Sandbox",
            "platforms": "PC, PlayStation, Xbox, Nintendo Switch, Mobile",
        },
    },

    "roblox": {
        "name": "Roblox",
        "emoji": "🎮",
        "rating": "غير محدد",
        "ar": {
            "description": "منصة ألعاب تتيح للمستخدمين لعب وصناعة تجارب مختلفة.",
            "developer": "Roblox Corporation",
            "release": "1 سبتمبر 2006",
            "genre": "منصة ألعاب، اجتماعية",
            "platforms": "PC، Xbox، PlayStation، الجوال",
        },
        "en": {
            "description": "An online platform where users can play and create different experiences.",
            "developer": "Roblox Corporation",
            "release": "September 1, 2006",
            "genre": "Gaming Platform, Social",
            "platforms": "PC, Xbox, PlayStation, Mobile",
        },
    },

    "fortnite": {
        "name": "Fortnite",
        "emoji": "🚌",
        "rating": "83/100",
        "ar": {
            "description": "لعبة أونلاين تجمع بين القتال والبناء والاستكشاف.",
            "developer": "Epic Games",
            "release": "25 يوليو 2017",
            "genre": "باتل رويال، أكشن، بناء",
            "platforms": "PC، PlayStation، Xbox، Nintendo Switch، الجوال",
        },
        "en": {
            "description": "An online game combining combat, building and exploration.",
            "developer": "Epic Games",
            "release": "July 25, 2017",
            "genre": "Battle Royale, Action, Building",
            "platforms": "PC, PlayStation, Xbox, Nintendo Switch, Mobile",
        },
    },

    "valorant": {
        "name": "Valorant",
        "emoji": "🎯",
        "rating": "80/100",
        "ar": {
            "description": "لعبة تصويب تكتيكية تنافسية تعتمد على الشخصيات والقدرات.",
            "developer": "Riot Games",
            "release": "2 يونيو 2020",
            "genre": "تصويب تكتيكي، تنافسية",
            "platforms": "PC، PlayStation، Xbox",
        },
        "en": {
            "description": "A competitive tactical shooter featuring unique agents and abilities.",
            "developer": "Riot Games",
            "release": "June 2, 2020",
            "genre": "Tactical Shooter, Competitive",
            "platforms": "PC, PlayStation, Xbox",
        },
    },

    "rocketleague": {
        "name": "Rocket League",
        "emoji": "🏎️",
        "rating": "86/100",
        "ar": {
            "description": "لعبة رياضية تجمع بين كرة القدم والسيارات السريعة.",
            "developer": "Psyonix",
            "release": "7 يوليو 2015",
            "genre": "رياضة، سيارات، تنافسية",
            "platforms": "PC، PlayStation، Xbox، Nintendo Switch",
        },
        "en": {
            "description": "A competitive sports game combining soccer with rocket-powered cars.",
            "developer": "Psyonix",
            "release": "July 7, 2015",
            "genre": "Sports, Racing, Competitive",
            "platforms": "PC, PlayStation, Xbox, Nintendo Switch",
        },
    },

    "brawlstars": {
        "name": "Brawl Stars",
        "emoji": "⭐",
        "rating": "82/100",
        "ar": {
            "description": "لعبة أكشن متعددة اللاعبين تضم شخصيات وأنماط لعب مختلفة.",
            "developer": "Supercell",
            "release": "12 ديسمبر 2018",
            "genre": "أكشن، متعددة اللاعبين",
            "platforms": "Android، iOS",
        },
        "en": {
            "description": "A multiplayer action game featuring different characters and game modes.",
            "developer": "Supercell",
            "release": "December 12, 2018",
            "genre": "Action, Multiplayer",
            "platforms": "Android, iOS",
        },
    },

    "gtav": {
        "name": "GTA V",
        "emoji": "🚗",
        "rating": "97/100",
        "aliases": [
            "gta 5",
            "grand theft auto v",
            "grand theft auto 5",
        ],
        "ar": {
            "description": "لعبة أكشن ومغامرات في عالم مفتوح تدور أحداثها في مدينة لوس سانتوس.",
            "developer": "Rockstar Games",
            "release": "17 سبتمبر 2013",
            "genre": "أكشن، مغامرات، عالم مفتوح",
            "platforms": "PC، PlayStation، Xbox",
        },
        "en": {
            "description": "An open-world action-adventure game set in the city of Los Santos.",
            "developer": "Rockstar Games",
            "release": "September 17, 2013",
            "genre": "Action, Adventure, Open World",
            "platforms": "PC, PlayStation, Xbox",
        },
    },

    "genshinimpact": {
        "name": "Genshin Impact",
        "emoji": "✨",
        "rating": "84/100",
        "ar": {
            "description": "لعبة تقمص أدوار وأكشن بعالم مفتوح مليء بالاستكشاف والشخصيات.",
            "developer": "HoYoverse",
            "release": "28 سبتمبر 2020",
            "genre": "أكشن، تقمص أدوار، عالم مفتوح",
            "platforms": "PC، PlayStation، Android، iOS",
        },
        "en": {
            "description": "An open-world action RPG centered on exploration and a diverse cast of characters.",
            "developer": "HoYoverse",
            "release": "September 28, 2020",
            "genre": "Action RPG, Open World",
            "platforms": "PC, PlayStation, Android, iOS",
        },
    },

    "clashroyale": {
        "name": "Clash Royale",
        "emoji": "👑",
        "rating": "80/100",
        "ar": {
            "description": "لعبة استراتيجية في الوقت الحقيقي تجمع بين البطاقات والمعارك متعددة اللاعبين.",
            "developer": "Supercell",
            "release": "2 مارس 2016",
            "genre": "استراتيجية، بطاقات، تنافسية",
            "platforms": "Android، iOS",
        },
        "en": {
            "description": "A real-time strategy game combining collectible cards with multiplayer battles.",
            "developer": "Supercell",
            "release": "March 2, 2016",
            "genre": "Strategy, Card, Competitive",
            "platforms": "Android, iOS",
        },
    },

    "overwatch": {
        "name": "Overwatch",
        "emoji": "🦸",
        "rating": "91/100",
        "ar": {
            "description": "لعبة تصويب جماعية تنافسية تعتمد على شخصيات وقدرات مختلفة.",
            "developer": "Blizzard Entertainment",
            "release": "24 مايو 2016",
            "genre": "تصويب، أكشن، جماعية",
            "platforms": "PC، PlayStation، Xbox، Nintendo Switch",
        },
        "en": {
            "description": "A competitive team-based shooter featuring heroes with unique abilities.",
            "developer": "Blizzard Entertainment",
            "release": "May 24, 2016",
            "genre": "Shooter, Action, Multiplayer",
            "platforms": "PC, PlayStation, Xbox, Nintendo Switch",
        },
    },

    "eldenring": {
        "name": "Elden Ring",
        "emoji": "⚔️",
        "rating": "96/100",
        "ar": {
            "description": "لعبة أكشن وتقمص أدوار بعالم مفتوح مليء بالاستكشاف والمواجهات.",
            "developer": "FromSoftware",
            "release": "25 فبراير 2022",
            "genre": "أكشن، تقمص أدوار، عالم مفتوح",
            "platforms": "PC، PlayStation، Xbox",
        },
        "en": {
            "description": "An open-world action RPG focused on exploration, combat and discovery.",
            "developer": "FromSoftware",
            "release": "February 25, 2022",
            "genre": "Action RPG, Open World",
            "platforms": "PC, PlayStation, Xbox",
        },
    },

    "reddeadredemption": {
        "name": "Red Dead Redemption",
        "emoji": "🤠",
        "rating": "95/100",
        "series": "red_dead",
        "ar": {
            "description": "لعبة أكشن ومغامرات في عالم مفتوح تدور أحداثها في الغرب الأمريكي.",
            "developer": "Rockstar San Diego",
            "release": "18 مايو 2010",
            "genre": "أكشن، مغامرات، عالم مفتوح",
            "platforms": "PlayStation، Xbox، Nintendo Switch، PC",
        },
        "en": {
            "description": "An open-world action-adventure game set in the American frontier.",
            "developer": "Rockstar San Diego",
            "release": "May 18, 2010",
            "genre": "Action, Adventure, Open World",
            "platforms": "PlayStation, Xbox, Nintendo Switch, PC",
        },
    },

    "reddeadredemption2": {
        "name": "Red Dead Redemption 2",
        "emoji": "🤠",
        "rating": "97/100",
        "series": "red_dead",
        "ar": {
            "description": "مغامرة ملحمية في الغرب الأمريكي تتبع قصة عصابة Van der Linde.",
            "developer": "Rockstar Studios",
            "release": "26 أكتوبر 2018",
            "genre": "أكشن، مغامرات، عالم مفتوح",
            "platforms": "PC، PlayStation، Xbox",
        },
        "en": {
            "description": "An epic open-world adventure following the Van der Linde gang.",
            "developer": "Rockstar Studios",
            "release": "October 26, 2018",
            "genre": "Action, Adventure, Open World",
            "platforms": "PC, PlayStation, Xbox",
        },
    },
}


GAME_ALIASES = {
    "gta v": "gtav",
    "gta 5": "gtav",
    "grand theft auto v": "gtav",
    "grand theft auto 5": "gtav",
    "rdr": "red_dead",
    "red dead": "red_dead",
    "red dead redemption": "red_dead",
    "red dead redemption 2": "reddeadredemption2",
    "elden ring": "eldenring",
    "overwatch": "overwatch",
}


# =========================================================
# أسئلة التحدي
# =========================================================

quiz_questions = [
    {
        "question_ar": "من هو مطور Minecraft؟",
        "question_en": "Who developed Minecraft?",
        "answers_ar": [
            "Mojang Studios",
            "Rockstar Games",
            "Epic Games",
            "Supercell",
        ],
        "answers_en": [
            "Mojang Studios",
            "Rockstar Games",
            "Epic Games",
            "Supercell",
        ],
        "correct": 0,
    },
    {
        "question_ar": "في أي مدينة تدور أحداث GTA V بشكل أساسي؟",
        "question_en": "Which city is GTA V mainly set in?",
        "answers_ar": [
            "لوس سانتوس",
            "نيو يورك",
            "واشنطن",
            "لاس فيغاس",
        ],
        "answers_en": [
            "Los Santos",
            "New York",
            "Washington",
            "Las Vegas",
        ],
        "correct": 0,
    },
    {
        "question_ar": "من مطور Elden Ring؟",
        "question_en": "Who developed Elden Ring?",
        "answers_ar": [
            "FromSoftware",
            "Blizzard",
            "Riot Games",
            "Psyonix",
        ],
        "answers_en": [
            "FromSoftware",
            "Blizzard",
            "Riot Games",
            "Psyonix",
        ],
        "correct": 0,
    },
    {
        "question_ar": "أي لعبة تجمع بين كرة القدم والسيارات؟",
        "question_en": "Which game combines soccer and cars?",
        "answers_ar": [
            "Rocket League",
            "Valorant",
            "Overwatch",
            "Minecraft",
        ],
        "answers_en": [
            "Rocket League",
            "Valorant",
            "Overwatch",
            "Minecraft",
        ],
        "correct": 0,
    },
    {
        "question_ar": "من مطور Valorant؟",
        "question_en": "Who developed Valorant?",
        "answers_ar": [
            "Riot Games",
            "Supercell",
            "Epic Games",
            "Mojang Studios",
        ],
        "answers_en": [
            "Riot Games",
            "Supercell",
            "Epic Games",
            "Mojang Studios",
        ],
        "correct": 0,
    },
    {
        "question_ar": "أي لعبة تدور في الغرب الأمريكي؟",
        "question_en": "Which game is set in the American frontier?",
        "answers_ar": [
            "Red Dead Redemption",
            "GTA V",
            "Roblox",
            "Fortnite",
        ],
        "answers_en": [
            "Red Dead Redemption",
            "GTA V",
            "Roblox",
            "Fortnite",
        ],
        "correct": 0,
    },
    {
        "question_ar": "من مطور Brawl Stars؟",
        "question_en": "Who developed Brawl Stars?",
        "answers_ar": [
            "Supercell",
            "Rockstar Games",
            "Blizzard",
            "HoYoverse",
        ],
        "answers_en": [
            "Supercell",
            "Rockstar Games",
            "Blizzard",
            "HoYoverse",
        ],
        "correct": 0,
    },
    {
        "question_ar": "أي لعبة هي منصة لصناعة ولعب تجارب مختلفة؟",
        "question_en": "Which game is a platform for creating and playing experiences?",
        "answers_ar": [
            "Roblox",
            "Elden Ring",
            "Valorant",
            "Rocket League",
        ],
        "answers_en": [
            "Roblox",
            "Elden Ring",
            "Valorant",
            "Rocket League",
        ],
        "correct": 0,
    },
    {
        "question_ar": "من مطور Overwatch؟",
        "question_en": "Who developed Overwatch?",
        "answers_ar": [
            "Blizzard Entertainment",
            "Riot Games",
            "FromSoftware",
            "Psyonix",
        ],
        "answers_en": [
            "Blizzard Entertainment",
            "Riot Games",
            "FromSoftware",
            "Psyonix",
        ],
        "correct": 0,
    },
    {
        "question_ar": "أي لعبة صدرت في عام 2022؟",
        "question_en": "Which game was released in 2022?",
        "answers_ar": [
            "Elden Ring",
            "GTA V",
            "Minecraft",
            "Overwatch",
        ],
        "answers_en": [
            "Elden Ring",
            "GTA V",
            "Minecraft",
            "Overwatch",
        ],
        "correct": 0,
    },
]


# =========================================================
# أدوات عامة
# =========================================================

def normalize_game_name(value: str) -> str:
    normalized = " ".join(value.strip().casefold().split())
    return normalized.replace("’", "'")


def find_game_id(game_name: str):
    normalized = normalize_game_name(game_name)

    if normalized in GAME_ALIASES:
        return GAME_ALIASES[normalized]

    for game_id, game in games.items():
        names = [game["name"], game_id, *game.get("aliases", [])]

        if normalized in {
            normalize_game_name(name)
            for name in names
        }:
            return game_id

    return None


def get_language(context):
    return context.user_data.get("language", "ar")


def menu_text(language):
    if language == "ar":
        return "🎮 اختر اللعبة التي تريد معرفة معلومات عنها:"
    return "🎮 Choose a game to get information about:"


def back_markup(language):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔙 رجوع" if language == "ar" else "🔙 Back",
                callback_data="back",
            )
        ]
    ])


# =========================================================
# قائمة الألعاب
# =========================================================

def get_game_buttons(language):

    keyboard = []

    for game_id, game in games.items():

        if game_id in {
            "reddeadredemption",
            "reddeadredemption2",
        }:
            continue

        keyboard.append([
            InlineKeyboardButton(
                f"{game['emoji']} {game['name']}",
                callback_data=game_id,
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            "🤠 Red Dead",
            callback_data="red_dead",
        )
    ])

    if language == "ar":
        keyboard.extend([
            [
                InlineKeyboardButton(
                    "🎲 اكتشف لعبة",
                    callback_data="discover_game",
                )
            ],
            [
                InlineKeyboardButton(
                    "🧠 تحدي الألعاب",
                    callback_data="quiz_start",
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
                    "➕ طلب لعبة",
                    callback_data="request_game",
                )
            ],
        ])

    else:
        keyboard.extend([
            [
                InlineKeyboardButton(
                    "🎲 Discover a Game",
                    callback_data="discover_game",
                )
            ],
            [
                InlineKeyboardButton(
                    "🧠 Game Challenge",
                    callback_data="quiz_start",
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
                    "➕ Request a Game",
                    callback_data="request_game",
                )
            ],
        ])

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# معلومات اللعبة
# =========================================================

def game_info_text(game_id, language):

    game = games[game_id]
    info = game[language]

    if language == "ar":
        return (
            f"{game['emoji']} *{game['name']}*\n\n"
            f"📖 *الوصف:*\n{info['description']}\n\n"
            f"👨‍💻 *المطور:*\n{info['developer']}\n\n"
            f"📅 *تاريخ الإصدار:*\n{info['release']}\n\n"
            f"🎯 *النوع:*\n{info['genre']}\n\n"
            f"💻 *المنصات:*\n{info['platforms']}\n\n"
            f"⭐ *تقييم النقاد:*\n{game['rating']}"
        )

    return (
        f"{game['emoji']} *{game['name']}*\n\n"
        f"📖 *Description:*\n{info['description']}\n\n"
        f"👨‍💻 *Developer:*\n{info['developer']}\n\n"
        f"📅 *Release Date:*\n{info['release']}\n\n"
        f"🎯 *Genre:*\n{info['genre']}\n\n"
        f"💻 *Platforms:*\n{info['platforms']}\n\n"
        f"⭐ *Critic Rating:*\n{game['rating']}"
    )


# =========================================================
# اكتشف لعبة
# =========================================================

def choose_random_game(context):

    available = [
        game_id
        for game_id in games
        if game_id not in {
            "reddeadredemption",
            "reddeadredemption2",
        }
    ]

    previous = context.user_data.get("discovered_game")

    if previous in available and len(available) > 1:
        available.remove(previous)

    game_id = random.choice(available)
    context.user_data["discovered_game"] = game_id

    return game_id


def discover_text(game_id, language):

    game = games[game_id]
    info = game[language]

    if language == "ar":
        return (
            "🎲 *اختيار عشوائي لك!*\n\n"
            f"{game['emoji']} *{game['name']}*\n\n"
            f"🎯 *النوع:* {info['genre']}\n"
            f"💻 *المنصات:* {info['platforms']}\n"
            f"⭐ *التقييم:* {game['rating']}\n\n"
            "✨ يمكن تكون لعبتك القادمة!"
        )

    return (
        "🎲 *Random pick for you!*\n\n"
        f"{game['emoji']} *{game['name']}*\n\n"
        f"🎯 *Genre:* {info['genre']}\n"
        f"💻 *Platforms:* {info['platforms']}\n"
        f"⭐ *Rating:* {game['rating']}\n\n"
        "✨ Maybe this could be your next game!"
    )


def discover_markup(language):

    if language == "ar":
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔄 لعبة ثانية",
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
                "🔄 Another Game",
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


async def discover_game(update, context):

    query = update.callback_query
    await query.answer()

    language = get_language(context)
    game_id = choose_random_game(context)

    await query.edit_message_text(
        discover_text(game_id, language),
        parse_mode="Markdown",
        reply_markup=discover_markup(language),
    )


async def discover_info(update, context):

    query = update.callback_query
    await query.answer()

    language = get_language(context)

    game_id = context.user_data.get("discovered_game")

    if not game_id:
        game_id = choose_random_game(context)

    await query.edit_message_text(
        game_info_text(game_id, language),
        parse_mode="Markdown",
        reply_markup=back_markup(language),
    )


# =========================================================
# Red Dead
# =========================================================

def red_dead_markup(language):

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🤠 Red Dead Redemption",
                callback_data="reddeadredemption",
            )
        ],
        [
            InlineKeyboardButton(
                "🤠 Red Dead Redemption 2",
                callback_data="reddeadredemption2",
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 رجوع" if language == "ar" else "🔙 Back",
                callback_data="back",
            )
        ],
    ])


async def red_dead_menu(update, context):

    query = update.callback_query
    await query.answer()

    language = get_language(context)

    text = (
        "🤠 *Red Dead*\n\nأي لعبة تقصد؟"
        if language == "ar"
        else
        "🤠 *Red Dead*\n\nWhich game do you mean?"
    )

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=red_dead_markup(language),
    )


# =========================================================
# PostgreSQL
# =========================================================

def get_db_connection():

    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL غير موجود في Render Environment"
        )

    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row,
    )


def init_database():

    with get_db_connection() as conn:

        with conn.cursor() as cur:

            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    language TEXT NOT NULL DEFAULT 'ar',
                    first_seen_at TIMESTAMPTZ NOT NULL,
                    last_seen_at TIMESTAMPTZ NOT NULL
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS game_requests (
                    id BIGSERIAL PRIMARY KEY,
                    game_name TEXT NOT NULL,
                    normalized_name TEXT NOT NULL,
                    user_id BIGINT,
                    username TEXT,
                    language TEXT NOT NULL DEFAULT 'ar',
                    requested_at TIMESTAMPTZ NOT NULL
                )
            """)

            # جدول نقاط تحدي الألعاب
            cur.execute("""
                CREATE TABLE IF NOT EXISTS quiz_scores (
                    user_id BIGINT PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    xp INTEGER NOT NULL DEFAULT 0,
                    correct_answers INTEGER NOT NULL DEFAULT 0,
                    wrong_answers INTEGER NOT NULL DEFAULT 0,
                    best_streak INTEGER NOT NULL DEFAULT 0,
                    current_streak INTEGER NOT NULL DEFAULT 0
                )
            """)

        conn.commit()

    print(
        "✅ PostgreSQL database initialized.",
        flush=True,
    )


# =========================================================
# تسجيل المستخدم
# =========================================================

def register_user(update, language="ar"):

    user = update.effective_user

    if not user:
        return

    now = datetime.now(timezone.utc)

    try:

        with get_db_connection() as conn:

            with conn.cursor() as cur:

                cur.execute("""
                    INSERT INTO users
                    (
                        user_id,
                        username,
                        first_name,
                        language,
                        first_seen_at,
                        last_seen_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)

                    ON CONFLICT (user_id)
                    DO UPDATE SET
                        username = EXCLUDED.username,
                        first_name = EXCLUDED.first_name,
                        last_seen_at = EXCLUDED.last_seen_at
                """, (
                    user.id,
                    user.username,
                    user.first_name,
                    language,
                    now,
                    now,
                ))

            conn.commit()

    except Exception as error:

        print(
            f"❌ Database error while registering user: {error}",
            flush=True,
        )


def update_user_language(update, language):

    user = update.effective_user

    if not user:
        return

    try:

        with get_db_connection() as conn:

            with conn.cursor() as cur:

                cur.execute("""
                    UPDATE users
                    SET
                        language = %s,
                        last_seen_at = %s
                    WHERE user_id = %s
                """, (
                    language,
                    datetime.now(timezone.utc),
                    user.id,
                ))

            conn.commit()

    except Exception as error:

        print(
            f"❌ Database error while updating language: {error}",
            flush=True,
        )


# =========================================================
# نظام تحدي الألعاب
# =========================================================

def get_quiz_question(context):

    previous = context.user_data.get("quiz_question")

    choices = list(range(len(quiz_questions)))

    if previous is not None and len(choices) > 1:
        choices.remove(previous)

    index = random.choice(choices)

    context.user_data["quiz_question"] = index

    return quiz_questions[index]


def quiz_markup(question, language):

    answers = (
        question["answers_ar"]
        if language == "ar"
        else question["answers_en"]
    )

    buttons = []

    for index, answer in enumerate(answers):

        buttons.append([
            InlineKeyboardButton(
                f"{chr(65 + index)}) {answer}",
                callback_data=f"quiz_answer_{index}",
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            "🔙 رجوع" if language == "ar" else "🔙 Back",
            callback_data="back",
        )
    ])

    return InlineKeyboardMarkup(buttons)


def quiz_question_text(question, language):

    if language == "ar":
        return (
            "🧠 *تحدي الألعاب*\n\n"
            "🎯 جاوب على السؤال:\n\n"
            f"❓ {question['question_ar']}\n\n"
            "⭐ الإجابة الصحيحة = +10 XP"
        )

    return (
        "🧠 *Game Challenge*\n\n"
        "🎯 Answer the question:\n\n"
        f"❓ {question['question_en']}\n\n"
        "⭐ Correct answer = +10 XP"
    )


async def quiz_start(update, context):

    query = update.callback_query
    await query.answer()

    language = get_language(context)

    question = get_quiz_question(context)

    await query.edit_message_text(
        quiz_question_text(question, language),
        parse_mode="Markdown",
        reply_markup=quiz_markup(
            question,
            language,
        ),
    )


def get_quiz_score(user_id):

    with get_db_connection() as conn:

        with conn.cursor() as cur:

            cur.execute("""
                SELECT *
                FROM quiz_scores
                WHERE user_id = %s
            """, (user_id,))

            row = cur.fetchone()

            if row:
                return row

            cur.execute("""
                INSERT INTO quiz_scores
                (
                    user_id,
                    xp,
                    correct_answers,
                    wrong_answers,
                    best_streak,
                    current_streak
                )
                VALUES (%s, 0, 0, 0, 0, 0)
                RETURNING *
            """, (user_id,))

            row = cur.fetchone()

        conn.commit()

    return row


def update_quiz_score(
    user,
    correct,
):

    with get_db_connection() as conn:

        with conn.cursor() as cur:

            cur.execute("""
                INSERT INTO quiz_scores
                (
                    user_id,
                    username,
                    first_name,
                    xp,
                    correct_answers,
                    wrong_answers,
                    best_streak,
                    current_streak
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

                ON CONFLICT (user_id)
                DO UPDATE SET
                    username = EXCLUDED.username,
                    first_name = EXCLUDED.first_name,
                    xp = quiz_scores.xp + EXCLUDED.xp,
                    correct_answers =
                        quiz_scores.correct_answers
                        + EXCLUDED.correct_answers,
                    wrong_answers =
                        quiz_scores.wrong_answers
                        + EXCLUDED.wrong_answers,
                    current_streak =
                        EXCLUDED.current_streak,
                    best_streak =
                        GREATEST(
                            quiz_scores.best_streak,
                            EXCLUDED.best_streak
                        )
            """, (
                user.id,
                user.username,
                user.first_name,
                10 if correct else 0,
                1 if correct else 0,
                0 if correct else 1,
                1 if correct else 0,
                1 if correct else 0,
            ))

        conn.commit()


async def quiz_answer(update, context):

    query = update.callback_query
    await query.answer()

    user = update.effective_user

    if not user:
        return

    language = get_language(context)

    question_index = context.user_data.get(
        "quiz_question"
    )

    if question_index is None:
        await quiz_start(update, context)
        return

    question = quiz_questions[question_index]

    selected = int(
        query.data.replace(
            "quiz_answer_",
            "",
        )
    )

    correct_index = question["correct"]

    if selected == correct_index:

        # نحافظ على الـstreak في user_data
        streak = context.user_data.get(
            "quiz_streak",
            0,
        ) + 1

        context.user_data["quiz_streak"] = streak

        update_quiz_score(
            user,
            True,
        )

        score = get_quiz_score(user.id)

        if language == "ar":

            message = (
                "🎉 *إجابة صحيحة!*\n\n"
                "⭐ +10 XP\n"
                f"🔥 السلسلة الحالية: {streak}\n\n"
                f"🏆 مجموع XP: {score['xp']}"
            )

        else:

            message = (
                "🎉 *Correct answer!*\n\n"
                "⭐ +10 XP\n"
                f"🔥 Current streak: {streak}\n\n"
                f"🏆 Total XP: {score['xp']}"
            )

    else:

        context.user_data["quiz_streak"] = 0

        update_quiz_score(
            user,
            False,
        )

        score = get_quiz_score(user.id)

        correct_answer = (
            question["answers_ar"][correct_index]
            if language == "ar"
            else
            question["answers_en"][correct_index]
        )

        if language == "ar":

            message = (
                "❌ *إجابة خاطئة!*\n\n"
                f"✅ الإجابة الصحيحة: {correct_answer}\n\n"
                "🔥 السلسلة رجعت إلى 0\n"
                f"🏆 مجموع XP: {score['xp']}"
            )

        else:

            message = (
                "❌ *Wrong answer!*\n\n"
                f"✅ Correct answer: {correct_answer}\n\n"
                "🔥 Streak reset to 0\n"
                f"🏆 Total XP: {score['xp']}"
            )

    buttons = []

    buttons.append([
        InlineKeyboardButton(
            "🧠 سؤال آخر"
            if language == "ar"
            else "🧠 Another Question",
            callback_data="quiz_start",
        )
    ])

    buttons.append([
        InlineKeyboardButton(
            "🏆 إحصائياتي"
            if language == "ar"
            else "🏆 My Stats",
            callback_data="quiz_stats",
        )
    ])

    buttons.append([
        InlineKeyboardButton(
            "🔙 رجوع"
            if language == "ar"
            else "🔙 Back",
            callback_data="back",
        )
    ])

    await query.edit_message_text(
        message,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def quiz_stats(update, context):

    query = update.callback_query
    await query.answer()

    user = update.effective_user

    if not user:
        return

    language = get_language(context)

    score = get_quiz_score(user.id)

    xp = score["xp"]
    correct = score["correct_answers"]
    wrong = score["wrong_answers"]
    best = score["best_streak"]

    level = (xp // 50) + 1

    if language == "ar":

        text = (
            "🏆 *إحصائيات تحدي الألعاب*\n\n"
            f"⭐ XP: {xp}\n"
            f"📈 المستوى: {level}\n"
            f"✅ إجابات صحيحة: {correct}\n"
            f"❌ إجابات خاطئة: {wrong}\n"
            f"🔥 أفضل سلسلة: {best}"
        )

    else:

        text = (
            "🏆 *Game Challenge Stats*\n\n"
            f"⭐ XP: {xp}\n"
            f"📈 Level: {level}\n"
            f"✅ Correct answers: {correct}\n"
            f"❌ Wrong answers: {wrong}\n"
            f"🔥 Best streak: {best}"
        )

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🧠 سؤال آخر"
                    if language == "ar"
                    else "🧠 Another Question",
                    callback_data="quiz_start",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 رجوع"
                    if language == "ar"
                    else "🔙 Back",
                    callback_data="back",
                )
            ],
        ]),
    )


# =========================================================
# إحصائيات الأدمن
# =========================================================

async def stats_command(update, context):

    user = update.effective_user

    if not user or not update.message:
        return

    if (
        not ADMIN_ID
        or str(user.id) != str(ADMIN_ID).strip()
    ):
        await update.message.reply_text(
            "❌ You are not authorized to use this command."
        )
        return

    try:

        with get_db_connection() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    "SELECT COUNT(*) AS total FROM users"
                )
                total = int(cur.fetchone()["total"])

                cur.execute("""
                    SELECT COUNT(*) AS today
                    FROM users
                    WHERE
                        (
                            first_seen_at
                            AT TIME ZONE 'Asia/Riyadh'
                        )::date
                        =
                        (
                            NOW()
                            AT TIME ZONE 'Asia/Riyadh'
                        )::date
                """)

                today = int(cur.fetchone()["today"])

                cur.execute("""
                    SELECT COUNT(*) AS last_7_days
                    FROM users
                    WHERE first_seen_at >=
                        NOW() - INTERVAL '7 days'
                """)

                last_7_days = int(
                    cur.fetchone()["last_7_days"]
                )

                cur.execute("""
                    SELECT
                        user_id,
                        username,
                        first_name,
                        first_seen_at
                    FROM users
                    ORDER BY first_seen_at DESC
                    LIMIT 1
                """)

                latest = cur.fetchone()

    except Exception as error:

        print(
            f"❌ Database error while loading stats: {error}",
            flush=True,
        )

        await update.message.reply_text(
            "❌ حدث خطأ أثناء قراءة الإحصائيات."
        )

        return

    if latest:

        latest_name = (
            latest["first_name"]
            or "بدون اسم"
        )

        if latest["username"]:
            latest_name += (
                f" (@{latest['username']})"
            )

    else:
        latest_name = "لا يوجد"

    message = (
        "📊 إحصائيات البوت\n\n"
        f"👥 إجمالي المستخدمين: {total}\n"
        f"🆕 الجدد اليوم: {today}\n"
        f"📈 الجدد خلال 7 أيام: {last_7_days}\n\n"
        f"👤 آخر مستخدم جديد:\n{latest_name}"
    )

    await update.message.reply_text(message)


# =========================================================
# طلبات الألعاب
# =========================================================

def register_game_request(
    game_name,
    update,
    language,
):

    game_name = " ".join(
        game_name.strip().split()
    )

    if find_game_id(game_name):

        if language == "ar":
            return (
                False,
                "✅ هذه اللعبة متوفرة بالفعل في البوت.",
            )

        return (
            False,
            "✅ This game is already available in the bot.",
        )

    user = update.effective_user

    normalized = normalize_game_name(
        game_name
    )

    with get_db_connection() as conn:

        with conn.cursor() as cur:

            cur.execute("""
                INSERT INTO game_requests
                (
                    game_name,
                    normalized_name,
                    user_id,
                    username,
                    language,
                    requested_at
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                game_name,
                normalized,
                user.id if user else None,
                user.username if user else None,
                language,
                datetime.now(timezone.utc),
            ))

        conn.commit()

    if language == "ar":

        return (
            True,
            f'✅ تم استلام طلبك بإضافة "{game_name}".\n'
            "شكرًا على اقتراحك! ❤️",
        )

    return (
        True,
        f'✅ Your request for "{game_name}" has been received.\n'
        "Thank you for your suggestion! ❤️",
    )


async def requests_command(update, context):

    user = update.effective_user

    if not user:
        return

    if (
        not ADMIN_ID
        or str(user.id) != str(ADMIN_ID).strip()
    ):
        await update.message.reply_text(
            "❌ You are not authorized to use this command."
        )
        return

    try:

        with get_db_connection() as conn:

            with conn.cursor() as cur:

                cur.execute("""
                    SELECT
                        normalized_name,
                        MIN(game_name) AS game_name,
                        COUNT(*) AS request_count
                    FROM game_requests
                    GROUP BY normalized_name
                    ORDER BY
                        request_count DESC,
                        game_name ASC
                """)

                rows = cur.fetchall()

    except Exception as error:

        print(
            f"❌ Database error while loading requests: {error}",
            flush=True,
        )

        await update.message.reply_text(
            "❌ حدث خطأ أثناء قراءة طلبات الألعاب."
        )

        return

    if not rows:

        await update.message.reply_text(
            "📋 لا توجد طلبات ألعاب حتى الآن."
        )

        return

    lines = [
        "📋 طلبات الألعاب",
        "",
    ]

    total = 0

    for index, item in enumerate(
        rows,
        start=1,
    ):

        count = int(
            item["request_count"]
        )

        total += count

        if count == 1:
            request_word = "طلب"
        elif count == 2:
            request_word = "طلبان"
        else:
            request_word = "طلبات"

        lines.append(
            f"{index}. 🎮 {item['game_name']} — "
            f"{count} {request_word}"
        )

    lines.extend([
        "",
        f"📊 إجمالي الطلبات: {total}",
    ])

    message = "\n".join(lines)

    await update.message.reply_text(
        message[:4000]
    )


# =========================================================
# القائمة
# =========================================================

async def send_menu(update, context):

    language = get_language(context)

    context.user_data.pop(
        "input_mode",
        None,
    )

    context.user_data.pop(
        "pending_game_request",
        None,
    )

    if update.callback_query:

        await update.callback_query.edit_message_text(
            menu_text(language),
            reply_markup=get_game_buttons(
                language
            ),
        )

    else:

        await update.message.reply_text(
            menu_text(language),
            reply_markup=get_game_buttons(
                language
            ),
        )


# =========================================================
# Start
# =========================================================

async def start(update, context):

    register_user(update)

    context.user_data.clear()

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🇸🇦 العربية",
                callback_data="language_ar",
            ),
            InlineKeyboardButton(
                "🇺🇸 English",
                callback_data="language_en",
            ),
        ]
    ])

    await update.message.reply_text(
        "👋 أهلاً بك في بوت معلومات الألعاب!\n\n"
        "اختر اللغة / Choose your language:",
        reply_markup=keyboard,
    )


async def choose_language(update, context):

    query = update.callback_query
    await query.answer()

    language = query.data.replace(
        "language_",
        "",
    )

    context.user_data["language"] = language

    update_user_language(
        update,
        language,
    )

    await send_menu(
        update,
        context,
    )


# =========================================================
# عرض لعبة
# =========================================================

async def show_game(update, context):

    query = update.callback_query
    await query.answer()

    game_id = query.data

    if game_id not in games:

        await query.edit_message_text(
            "❌ اللعبة غير موجودة."
        )

        return

    language = get_language(context)

    await query.edit_message_text(
        game_info_text(
            game_id,
            language,
        ),
        parse_mode="Markdown",
        reply_markup=back_markup(
            language
        ),
    )


# =========================================================
# البحث والطلبات
# =========================================================

def prompt_text(language, mode):

    if mode == "search":

        return (
            "🔎 اكتب اسم اللعبة التي تريد البحث عنها:"
            if language == "ar"
            else
            "🔎 Enter the name of the game you want to search for:"
        )

    return (
        "🎮 اكتب اسم اللعبة التي تريد إضافتها:"
        if language == "ar"
        else
        "🎮 Enter the name of the game you want to request:"
    )


async def begin_search(update, context):

    query = update.callback_query
    await query.answer()

    language = get_language(context)

    context.user_data["input_mode"] = "search"

    await query.edit_message_text(
        prompt_text(
            language,
            "search",
        ),
        reply_markup=back_markup(
            language
        ),
    )


async def begin_request(update, context):

    query = update.callback_query
    await query.answer()

    language = get_language(context)

    context.user_data["input_mode"] = "request"

    await query.edit_message_text(
        prompt_text(
            language,
            "request",
        ),
        reply_markup=back_markup(
            language
        ),
    )


async def request_searched_game(update, context):

    query = update.callback_query
    await query.answer()

    language = get_language(context)

    game_name = context.user_data.pop(
        "pending_game_request",
        "",
    )

    if not game_name:

        await send_menu(
            update,
            context,
        )

        return

    _, message = register_game_request(
        game_name,
        update,
        language,
    )

    await query.edit_message_text(
        message,
        reply_markup=back_markup(
            language
        ),
    )


async def handle_text(update, context):

    mode = context.user_data.get(
        "input_mode"
    )

    if (
        mode not in {
            "search",
            "request",
        }
        or not update.message
        or not update.message.text
    ):
        return

    game_name = update.message.text.strip()
    language = get_language(context)

    context.user_data.pop(
        "input_mode",
        None,
    )

    if not game_name:

        await update.message.reply_text(
            prompt_text(
                language,
                mode,
            ),
            reply_markup=back_markup(
                language
            ),
        )

        context.user_data[
            "input_mode"
        ] = mode

        return

    if mode == "search":

        game_id = find_game_id(
            game_name
        )

        if game_id == "red_dead":

            await update.message.reply_text(
                "🤠 *Red Dead*\n\nأي لعبة تقصد؟"
                if language == "ar"
                else
                "🤠 *Red Dead*\n\nWhich game do you mean?",
                parse_mode="Markdown",
                reply_markup=red_dead_markup(
                    language
                ),
            )

            return

        if game_id:

            await update.message.reply_text(
                game_info_text(
                    game_id,
                    language,
                ),
                parse_mode="Markdown",
                reply_markup=back_markup(
                    language
                ),
            )

            return

        context.user_data[
            "pending_game_request"
        ] = game_name

        text = (
            f'❌ اللعبة "{game_name}" غير موجودة حاليًا.'
            if language == "ar"
            else
            f'❌ "{game_name}" isn\'t available yet.'
        )

        button = (
            f"➕ طلب إضافة {game_name}"
            if language == "ar"
            else
            f"➕ Request {game_name}"
        )

        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        button[:60],
                        callback_data="request_searched_game",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔙 رجوع"
                        if language == "ar"
                        else "🔙 Back",
                        callback_data="back",
                    )
                ],
            ]),
        )

        return

    _, message = register_game_request(
        game_name,
        update,
        language,
    )

    await update.message.reply_text(
        message,
        reply_markup=back_markup(
            language
        ),
    )


# =========================================================
# رجوع
# =========================================================

async def back(update, context):

    query = update.callback_query
    await query.answer()

    await send_menu(
        update,
        context,
    )


# =========================================================
# تشغيل البوت
# =========================================================

def main():

    if not TOKEN:

        print(
            "❌ BOT_TOKEN غير موجود في Secrets",
            flush=True,
        )

        return

    if not DATABASE_URL:

        print(
            "❌ DATABASE_URL غير موجود في Render Environment",
            flush=True,
        )

        return

    init_database()

    app = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    # /start
    app.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    # /requests
    app.add_handler(
        CommandHandler(
            "requests",
            requests_command,
        )
    )

    # /stats
    app.add_handler(
        CommandHandler(
            "stats",
            stats_command,
        )
    )

    # اللغة
    app.add_handler(
        CallbackQueryHandler(
            choose_language,
            pattern=r"^language_(ar|en)$",
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

    # Red Dead
    app.add_handler(
        CallbackQueryHandler(
            red_dead_menu,
            pattern=r"^red_dead$",
        )
    )

    # =====================================================
    # تحدي الألعاب
    # =====================================================

    app.add_handler(
        CallbackQueryHandler(
            quiz_start,
            pattern=r"^quiz_start$",
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            quiz_answer,
            pattern=r"^quiz_answer_[0-3]$",
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            quiz_stats,
            pattern=r"^quiz_stats$",
        )
    )

    # الألعاب
    app.add_handler(
        CallbackQueryHandler(
            show_game,
            pattern=(
                r"^(minecraft|roblox|fortnite|"
                r"valorant|rocketleague|"
                r"brawlstars|gtav|genshinimpact|"
                r"clashroyale|overwatch|eldenring|"
                r"reddeadredemption|"
                r"reddeadredemption2)$"
            ),
        )
    )

    # البحث
    app.add_handler(
        CallbackQueryHandler(
            begin_search,
            pattern=r"^search_game$",
        )
    )

    # طلب لعبة
    app.add_handler(
        CallbackQueryHandler(
            begin_request,
            pattern=r"^request_game$",
        )
    )

    # طلب اللعبة التي تم البحث عنها
    app.add_handler(
        CallbackQueryHandler(
            request_searched_game,
            pattern=r"^request_searched_game$",
        )
    )

    # رجوع
    app.add_handler(
        CallbackQueryHandler(
            back,
            pattern=r"^back$",
        )
    )

    # إدخال نص
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text,
        )
    )

    print(
        "🤖 البوت يعمل الآن...",
        flush=True,
    )

    app.run_polling()


if __name__ == "__main__":
    main()