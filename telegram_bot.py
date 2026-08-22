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


# =========================
# Game information
# =========================

games = {
    "minecraft": {
        "name": "Minecraft",
        "emoji": "⛏️",
        "rating": "9.3/10",
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
        "rating": "غير متوفر",
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
        "rating": "7.8/10",
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
        "rating": "8.0/10",
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
        "rating": "8.5/10",
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
        "rating": "7.2/10",
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
        "aliases": [
            "gta 5",
            "grand theft auto v",
            "grand theft auto 5",
        ],
        "rating": "9.7/10",
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
        "rating": "8.1/10",
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
        "rating": "8.5/10",
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
        "rating": "9.1/10",
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
        "rating": "9.6/10",
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
        "rating": "9.5/10",
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
        "rating": "9.7/10",
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

    "red dead redemption": "reddeadredemption",
    "red dead redemption 2": "reddeadredemption2",

    "elden ring": "eldenring",
    "overwatch": "overwatch",
}


def normalize_game_name(value: str) -> str:
    normalized = " ".join(
        value.strip().casefold().split()
    )
    return normalized.replace("’", "'")


def find_game_id(game_name: str) -> str | None:

    normalized = normalize_game_name(game_name)

    if normalized in GAME_ALIASES:

        game_id = GAME_ALIASES[normalized]

        if game_id == "red_dead":
            return "red_dead"

        if game_id in games:
            return game_id

        return None

    for game_id, game in games.items():

        names = [
            game["name"],
            game_id,
            *game.get("aliases", []),
        ]

        if normalized in {
            normalize_game_name(name)
            for name in names
        }:
            return game_id

    return None


def get_language(
    context: ContextTypes.DEFAULT_TYPE,
) -> str:
    return context.user_data.get(
        "language",
        "ar",
    )


def menu_text(language: str) -> str:

    if language == "ar":
        return (
            "🎮 اختر اللعبة التي تريد معرفة "
            "معلومات عنها:"
        )

    return (
        "🎮 Choose a game to get "
        "information about:"
    )


# =========================
# Main game buttons
# =========================

def get_game_buttons(
    language: str,
) -> InlineKeyboardMarkup:

    keyboard = [
        [
            InlineKeyboardButton(
                f"{game['emoji']} {game['name']}",
                callback_data=game_id,
            )
        ]
        for game_id, game in games.items()
        if game_id not in {
            "reddeadredemption",
            "reddeadredemption2",
        }
    ]

    keyboard.append(
        [
            InlineKeyboardButton(
                "🤠 Red Dead",
                callback_data="red_dead",
            )
        ]
    )

    if language == "ar":

        keyboard.extend(
            [
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
                        "➕ طلب لعبة",
                        callback_data="request_game",
                    )
                ],
            ]
        )

    else:

        keyboard.extend(
            [
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
                        "➕ Request a Game",
                        callback_data="request_game",
                    )
                ],
            ]
        )

    return InlineKeyboardMarkup(keyboard)


def back_markup(
    language: str,
) -> InlineKeyboardMarkup:

    label = (
        "🔙 رجوع"
        if language == "ar"
        else "🔙 Back"
    )

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    label,
                    callback_data="back",
                )
            ]
        ]
    )


# =========================
# Game information
# =========================

def game_info_text(
    game_id: str,
    language: str,
) -> str:

    game = games[game_id]
    info = game[language]

    if language == "ar":

        return (
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
            f"{info['platforms']}\n\n"
            f"⭐ *تقييم النقاد:*\n"
            f"{game['rating']}"
        )

    return (
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
        f"{info['platforms']}\n\n"
        f"⭐ *Critics Score:*\n"
        f"{game['rating']}"
    )


# =========================
# Discover a random game
# =========================

def get_discoverable_games():

    return [
        game_id
        for game_id in games
        if game_id not in {
            "reddeadredemption",
            "reddeadredemption2",
        }
    ]


def choose_random_game(
    context: ContextTypes.DEFAULT_TYPE,
) -> str:

    available_games = get_discoverable_games()

    previous_game = context.user_data.get(
        "discovered_game"
    )

    if (
        previous_game in available_games
        and len(available_games) > 1
    ):

        available_games = [
            game_id
            for game_id in available_games
            if game_id != previous_game
        ]

    game_id = random.choice(
        available_games
    )

    context.user_data[
        "discovered_game"
    ] = game_id

    return game_id


def discover_text(
    game_id: str,
    language: str,
) -> str:

    game = games[game_id]
    info = game[language]

    if language == "ar":

        return (
            "🎲 *اختيار عشوائي لك!*\n\n"
            f"{game['emoji']} *{game['name']}*\n\n"
            f"🎯 *النوع:* {info['genre']}\n"
            f"💻 *المنصات:* {info['platforms']}\n"
            f"⭐ *تقييم النقاد:* {game['rating']}\n\n"
            "✨ يمكن تكون لعبتك القادمة!"
        )

    return (
        "🎲 *Random pick for you!*\n\n"
        f"{game['emoji']} *{game['name']}*\n\n"
        f"🎯 *Genre:* {info['genre']}\n"
        f"💻 *Platforms:* {info['platforms']}\n"
        f"⭐ *Critics Score:* {game['rating']}\n\n"
        "✨ Maybe this could be your next game!"
    )


def discover_markup(
    language: str,
) -> InlineKeyboardMarkup:

    if language == "ar":

        new_game = "🔄 لعبة ثانية"
        info = "📖 معلومات اللعبة"
        back = "🔙 رجوع"

    else:

        new_game = "🔄 Another Game"
        info = "📖 Game Information"
        back = "🔙 Back"

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    new_game,
                    callback_data="discover_game",
                )
            ],
            [
                InlineKeyboardButton(
                    info,
                    callback_data="discover_info",
                )
            ],
            [
                InlineKeyboardButton(
                    back,
                    callback_data="back",
                )
            ],
        ]
    )


async def discover_game(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    language = get_language(context)

    game_id = choose_random_game(
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
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    language = get_language(context)

    game_id = context.user_data.get(
        "discovered_game"
    )

    if (
        not game_id
        or game_id not in games
    ):
        game_id = choose_random_game(
            context
        )

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


# =========================
# Red Dead series
# =========================

def red_dead_markup(
    language: str,
) -> InlineKeyboardMarkup:

    back = (
        "🔙 رجوع"
        if language == "ar"
        else "🔙 Back"
    )

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🤠 Red Dead Redemption",
                    callback_data=(
                        "reddeadredemption"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    "🤠 Red Dead Redemption 2",
                    callback_data=(
                        "reddeadredemption2"
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    back,
                    callback_data="back",
                )
            ],
        ]
    )


async def red_dead_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    language = get_language(context)

    if language == "ar":

        text = (
            "🤠 *Red Dead*\n\n"
            "أي لعبة تقصد؟"
        )

    else:

        text = (
            "🤠 *Red Dead*\n\n"
            "Which game do you mean?"
        )

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=red_dead_markup(
            language
        ),
    )


# =========================
# PostgreSQL
# =========================

def get_db_connection():

    if not DATABASE_URL:

        raise RuntimeError(
            "DATABASE_URL غير موجود "
            "في Render Environment"
        )

    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row,
    )


def init_database():

    with get_db_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    language TEXT NOT NULL DEFAULT 'ar',
                    first_seen_at TIMESTAMPTZ NOT NULL,
                    last_seen_at TIMESTAMPTZ NOT NULL
                )
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS game_requests (
                    id BIGSERIAL PRIMARY KEY,
                    game_name TEXT NOT NULL,
                    normalized_name TEXT NOT NULL,
                    user_id BIGINT,
                    username TEXT,
                    language TEXT NOT NULL DEFAULT 'ar',
                    requested_at TIMESTAMPTZ NOT NULL
                )
                """
            )

        conn.commit()

    print(
        "✅ PostgreSQL database initialized.",
        flush=True,
    )


# =========================
# User registration
# =========================

def register_user(
    update: Update,
    language: str = "ar",
):

    user = update.effective_user

    if not user:
        return

    now = datetime.now(
        timezone.utc
    )

    try:

        with get_db_connection() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    """
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
                    """,
                    (
                        user.id,
                        user.username,
                        user.first_name,
                        language,
                        now,
                        now,
                    ),
                )

            conn.commit()

    except Exception as error:

        print(
            "❌ Database error while "
            f"registering user: {error}",
            flush=True,
        )


def update_user_language(
    update: Update,
    language: str,
):

    user = update.effective_user

    if not user:
        return

    try:

        with get_db_connection() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    """
                    UPDATE users
                    SET
                        language = %s,
                        last_seen_at = %s
                    WHERE user_id = %s
                    """,
                    (
                        language,
                        datetime.now(
                            timezone.utc
                        ),
                        user.id,
                    ),
                )

            conn.commit()

    except Exception as error:

        print(
            "❌ Database error while "
            f"updating user language: {error}",
            flush=True,
        )


# =========================
# Admin statistics
# =========================

async def stats_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    user = update.effective_user

    if not user or not update.message:
        return

    if (
        not ADMIN_ID
        or str(user.id)
        != str(ADMIN_ID).strip()
    ):

        await update.message.reply_text(
            "❌ You are not authorized "
            "to use this command."
        )

        return

    try:

        with get_db_connection() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    """
                    SELECT COUNT(*) AS total
                    FROM users
                    """
                )

                total = int(
                    cur.fetchone()["total"]
                )

                cur.execute(
                    """
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
                    """
                )

                today = int(
                    cur.fetchone()["today"]
                )

                cur.execute(
                    """
                    SELECT COUNT(*) AS last_7_days
                    FROM users
                    WHERE first_seen_at >=
                        NOW() - INTERVAL '7 days'
                    """
                )

                last_7_days = int(
                    cur.fetchone()["last_7_days"]
                )

                cur.execute(
                    """
                    SELECT
                        user_id,
                        username,
                        first_name,
                        first_seen_at
                    FROM users
                    ORDER BY first_seen_at DESC
                    LIMIT 1
                    """
                )

                latest = cur.fetchone()

    except Exception as error:

        print(
            "❌ Database error while "
            f"loading stats: {error}",
            flush=True,
        )

        await update.message.reply_text(
            "❌ حدث خطأ أثناء قراءة "
            "الإحصائيات."
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
        f"📈 الجدد خلال 7 أيام: "
        f"{last_7_days}\n\n"
        f"👤 آخر مستخدم جديد:\n"
        f"{latest_name}"
    )

    await update.message.reply_text(
        message
    )


# =========================
# Game requests
# =========================

def register_game_request(
    game_name: str,
    update: Update,
    language: str,
) -> tuple[bool, str]:

    game_name = " ".join(
        game_name.strip().split()
    )

    if find_game_id(game_name):

        if language == "ar":

            return (
                False,
                "✅ هذه اللعبة متوفرة بالفعل "
                "في البوت.",
            )

        return (
            False,
            "✅ This game is already "
            "available in the bot.",
        )

    user = update.effective_user

    normalized = normalize_game_name(
        game_name
    )

    with get_db_connection() as conn:

        with conn.cursor() as cur:

            cur.execute(
                """
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
                """,
                (
                    game_name,
                    normalized,
                    user.id if user else None,
                    user.username if user else None,
                    language,
                    datetime.now(
                        timezone.utc
                    ),
                ),
            )

        conn.commit()

    if language == "ar":

        return (
            True,
            f'✅ تم استلام طلبك بإضافة '
            f'"{game_name}".\n'
            "شكرًا على اقتراحك! ❤️",
        )

    return (
        True,
        f'✅ Your request for '
        f'"{game_name}" has been received.\n'
        "Thank you for your suggestion! ❤️",
    )


# =========================
# Admin requests command
# =========================

async def requests_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    user = update.effective_user

    if not user:
        return

    if (
        not ADMIN_ID
        or str(user.id)
        != str(ADMIN_ID).strip()
    ):

        await update.message.reply_text(
            "❌ You are not authorized "
            "to use this command."
        )

        return

    try:

        with get_db_connection() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    """
                    SELECT
                        normalized_name,
                        MIN(game_name) AS game_name,
                        COUNT(*) AS request_count
                    FROM game_requests
                    GROUP BY normalized_name
                    ORDER BY
                        request_count DESC,
                        game_name ASC
                    """
                )

                rows = cur.fetchall()

    except Exception as error:

        print(
            "❌ Database error while "
            f"loading requests: {error}",
            flush=True,
        )

        await update.message.reply_text(
            "❌ حدث خطأ أثناء قراءة "
            "طلبات الألعاب."
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
            f"{index}. 🎮 "
            f"{item['game_name']} — "
            f"{count} {request_word}"
        )

    lines.extend(
        [
            "",
            f"📊 إجمالي الطلبات: {total}",
        ]
    )

    message = "\n".join(lines)

    if len(message) <= 4000:

        await update.message.reply_text(
            message
        )

        return

    current = "📋 طلبات الألعاب\n\n"

    for line in lines[2:]:

        if (
            len(current)
            + len(line)
            + 1
            > 3900
        ):

            await update.message.reply_text(
                current
            )

            current = ""

        current += line + "\n"

    if current.strip():

        await update.message.reply_text(
            current
        )


# =========================
# Menu
# =========================

async def send_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

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


# =========================
# Start and language
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    register_user(update)

    context.user_data.clear()

    keyboard = InlineKeyboardMarkup(
        [
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
        ]
    )

    await update.message.reply_text(
        "👋 أهلاً بك في بوت معلومات الألعاب!\n\n"
        "اختر اللغة / Choose your language:",
        reply_markup=keyboard,
    )


async def choose_language(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    language = query.data.replace(
        "language_",
        "",
    )

    context.user_data[
        "language"
    ] = language

    update_user_language(
        update,
        language,
    )

    await send_menu(
        update,
        context,
    )


# =========================
# Game display
# =========================

async def show_game(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    game_id = query.data

    if game_id not in games:

        await query.edit_message_text(
            "❌ اللعبة غير موجودة."
        )

        return

    language = get_language(context)

    context.user_data.pop(
        "input_mode",
        None,
    )

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


# =========================
# Search and request flows
# =========================

def prompt_text(
    language: str,
    mode: str,
) -> str:

    if mode == "search":

        return (
            "🔎 اكتب اسم اللعبة التي تريد "
            "البحث عنها:"
            if language == "ar"
            else
            "🔎 Enter the name of the game "
            "you want to search for:"
        )

    return (
        "🎮 اكتب اسم اللعبة التي تريد "
        "إضافتها:"
        if language == "ar"
        else
        "🎮 Enter the name of the game "
        "you want to request:"
    )


async def begin_search(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    language = get_language(context)

    context.user_data[
        "input_mode"
    ] = "search"

    await query.edit_message_text(
        prompt_text(
            language,
            "search",
        ),
        reply_markup=back_markup(
            language
        ),
    )


async def begin_request(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    language = get_language(context)

    context.user_data[
        "input_mode"
    ] = "request"

    await query.edit_message_text(
        prompt_text(
            language,
            "request",
        ),
        reply_markup=back_markup(
            language
        ),
    )


async def request_searched_game(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

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

    context.user_data.pop(
        "input_mode",
        None,
    )

    await query.edit_message_text(
        message,
        reply_markup=back_markup(
            language
        ),
    )


async def handle_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

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

    game_name = (
        update.message.text.strip()
    )

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
                (
                    "🤠 *Red Dead*\n\n"
                    "أي لعبة تقصد؟"
                    if language == "ar"
                    else
                    "🤠 *Red Dead*\n\n"
                    "Which game do you mean?"
                ),
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

        if language == "ar":

            text = (
                f'❌ اللعبة "{game_name}" '
                "غير موجودة حاليًا."
            )

            button = (
                f"➕ طلب إضافة {game_name}"
            )

        else:

            text = (
                f'❌ "{game_name}" '
                "isn't available yet."
            )

            button = (
                f"➕ Request {game_name}"
            )

        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            button[:60],
                            callback_data=(
                                "request_searched_game"
                            ),
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
                ]
            ),
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


# =========================
# Back
# =========================

async def back(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    await send_menu(
        update,
        context,
    )


# =========================
# Application setup
# =========================

def main():

    if not TOKEN:

        print(
            "❌ BOT_TOKEN غير موجود في Secrets",
            flush=True,
        )

        return

    if not DATABASE_URL:

        print(
            "❌ DATABASE_URL غير موجود "
            "في Render Environment",
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

    # Language
    app.add_handler(
        CallbackQueryHandler(
            choose_language,
            pattern=r"^language_(ar|en)$",
        )
    )

    # Discover
    app.add_handler(
        CallbackQueryHandler(
            discover_game,
            pattern=r"^discover_game$",
        )
    )

    # Discover information
    app.add_handler(
        CallbackQueryHandler(
            discover_info,
            pattern=r"^discover_info$",
        )
    )

    # Red Dead series
    app.add_handler(
        CallbackQueryHandler(
            red_dead_menu,
            pattern=r"^red_dead$",
        )
    )

    # Games
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

    # Search
    app.add_handler(
        CallbackQueryHandler(
            begin_search,
            pattern=r"^search_game$",
        )
    )

    # Request
    app.add_handler(
        CallbackQueryHandler(
            begin_request,
            pattern=r"^request_game$",
        )
    )

    # Request searched game
    app.add_handler(
        CallbackQueryHandler(
            request_searched_game,
            pattern=r"^request_searched_game$",
        )
    )

    # Back
    app.add_handler(
        CallbackQueryHandler(
            back,
            pattern=r"^back$",
        )
    )

    # Text input
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