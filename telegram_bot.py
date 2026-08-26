# telegram_bot.py

import os
import random
import requests
import html
from datetime import datetime, timezone

import psycopg
from psycopg.rows import dict_row

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================================================
# استيراد ميزات telegram_bot2.py
# =========================================================

from telegram_bot2 import (
    init_quiz_database,
    register_quiz_handlers,
)

# =========================================================
# استيراد القائمة الجديدة من telegram_bot3.py
# =========================================================

from telegram_bot3 import (
    main_menu_text as bot3_menu_text,
    new_main_menu as bot3_main_menu,
    register_bot3_handlers,
)


# =========================================================
# الإعدادات
# =========================================================

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


"bloodborne": {
    "name": "Bloodborne",
    "emoji": "🩸",
    "rating": "92/100",

    "ar": {
        "description": "لعبة أكشن وتقمص أدوار بطابع مظلم، تدور أحداثها في مدينة يارنام المليئة بالأسرار والوحوش.",
        "developer": "FromSoftware",
        "release": "24 مارس 2015",
        "genre": "أكشن، تقمص أدوار، رعب",
        "platforms": "PlayStation 4",
    },

    "en": {
        "description": "An action RPG with a dark atmosphere, set in the mysterious city of Yharnam.",
        "developer": "FromSoftware",
        "release": "March 24, 2015",
        "genre": "Action RPG, Horror",
        "platforms": "PlayStation 4",
    },
},


    "reddeadredemption": {
        "name": "Red Dead Redemption",
        "emoji": "🤠",
        "rating": "95/100",

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

def search_game_external(game_name):
    """
    البحث عن لعبة غير موجودة في games
    باستخدام RAWG API.

    تبحث عن أقرب نتيجة ثم تجلب معلوماتها الكاملة.
    """

    api_key = os.getenv("RAWG_API_KEY")

    if not api_key:

        print(
            "⚠️ RAWG_API_KEY غير موجود",
            flush=True,
        )

        return None

    try:

        # =====================================================
        # البحث عن اللعبة
        # =====================================================

        response = requests.get(
            "https://api.rawg.io/api/games",
            params={
                "key": api_key,
                "search": game_name,
                "page_size": 10,
                "search_precise": "true",
            },
            timeout=10,
        )

        if response.status_code != 200:

            print(
                f"❌ RAWG search error: "
                f"{response.status_code}",
                flush=True,
            )

            return None

        data = response.json()

        results = data.get(
            "results",
            [],
        )

        if not results:

            print(
                f"⚠️ لم يتم العثور على لعبة: {game_name}",
                flush=True,
            )

            return None

        # =====================================================
        # اختيار أقرب نتيجة
        # =====================================================

        normalized_query = (
            game_name
            .strip()
            .lower()
        )

        selected_result = None

        # تطابق الاسم بشكل مباشر
        for result in results:

            result_name = (
                result.get("name")
                or ""
            ).strip().lower()

            if result_name == normalized_query:

                selected_result = result

                break

        # إذا لم نجد تطابقًا مباشرًا
        # نستخدم أول نتيجة مناسبة
        if not selected_result:

            selected_result = results[0]

        rawg_id = selected_result.get(
            "id"
        )

        if not rawg_id:

            return None

        # =====================================================
        # جلب التفاصيل الكاملة
        # =====================================================

        details_response = requests.get(
            f"https://api.rawg.io/api/games/{rawg_id}",
            params={
                "key": api_key,
            },
            timeout=10,
        )

        if details_response.status_code != 200:

            print(
                f"❌ RAWG details error: "
                f"{details_response.status_code}",
                flush=True,
            )

            return None

        game = details_response.json()

        # =====================================================
        # الاسم
        # =====================================================

        name = (
            game.get("name")
            or game_name
        )

        # =====================================================
        # الوصف
        # =====================================================

        description = (
            game.get("description_raw")
            or "غير متوفر"
        )

        description = html.unescape(
            description
        )

        # تنظيف المسافات الزائدة
        description = " ".join(
            description.split()
        )

        # =====================================================
        # المطور
        # =====================================================

        developer_list = game.get(
            "developers",
            [],
        )

        developers = [

            item.get("name")

            for item in developer_list

            if item.get("name")

        ]

        developer = (

            "، ".join(developers)

            if developers

            else "غير محدد"

        )

        # =====================================================
        # الناشر
        # =====================================================

        publisher_list = game.get(
            "publishers",
            [],
        )

        publishers = [

            item.get("name")

            for item in publisher_list

            if item.get("name")

        ]

        publisher = (

            "، ".join(publishers)

            if publishers

            else "غير محدد"

        )

        # =====================================================
        # النوع
        # =====================================================

        genres_list = game.get(
            "genres",
            [],
        )

        genres = [

            item.get("name")

            for item in genres_list

            if item.get("name")

        ]

        genre = (

            "، ".join(genres)

            if genres

            else "غير محدد"

        )

        # =====================================================
        # المنصات
        # =====================================================

        platforms_list = game.get(
            "platforms",
            [],
        )

        platforms = []

        for item in platforms_list:

            platform = item.get(
                "platform",
                {}
            )

            platform_name = platform.get(
                "name"
            )

            if platform_name:

                platforms.append(
                    platform_name
                )

        platforms_text = (

            "، ".join(platforms)

            if platforms

            else "غير محدد"

        )

        # =====================================================
        # تاريخ الإصدار
        # =====================================================

        release = (
            game.get("released")
            or "غير محدد"
        )

        # =====================================================
        # تقييم Metacritic
        # =====================================================

        metacritic = game.get(
            "metacritic"
        )

        if metacritic is not None:

            rating = (
                f"{metacritic}/100"
            )

        else:

            rating = "غير محدد"

        # =====================================================
        # تقييم RAWG
        # =====================================================

        rawg_rating = game.get(
            "rating"
        )

        ratings_count = game.get(
            "ratings_count"
        )

        # =====================================================
        # عدد التقييمات
        # =====================================================

        if ratings_count is not None:

            ratings_count_text = str(
                ratings_count
            )

        else:

            ratings_count_text = "غير محدد"

        # =====================================================
        # رابط اللعبة في RAWG
        # =====================================================

        rawg_url = game.get(
            "website"
        ) or game.get(
            "slug"
        )

        # =====================================================
        # الصورة
        # =====================================================

        background_image = game.get(
            "background_image"
        )

        # =====================================================
        # النتيجة النهائية
        # =====================================================

        return {

            "name": name,

            "description": description,

            "developer": developer,

            "publisher": publisher,

            "release": release,

            "genre": genre,

            "platforms": platforms_text,

            "rating": rating,

            "rawg_rating": (
                str(rawg_rating)
                if rawg_rating is not None
                else "غير محدد"
            ),

            "ratings_count": (
                ratings_count_text
            ),

            "rawg_url": rawg_url,

            "image": background_image,

        }

    except requests.RequestException as error:

        print(
            f"❌ RAWG connection error: "
            f"{error}",
            flush=True,
        )

        return None

    except Exception as error:

        print(
            f"❌ External search error: "
            f"{error}",
            flush=True,
        )

        return None


def external_game_info_text(
    game,
    language,
):
    """
    تجهيز معلومات اللعبة الخارجية
    بالعربي أو الإنجليزي.
    """

    if language == "ar":

        return (
            "🎮 *معلومات اللعبة*\n\n"
            f"🎮 *{game['name']}*\n\n"
            f"📝 *الوصف:*\n"
            f"{game['description']}\n\n"
            f"👨‍💻 *المطور:* "
            f"{game['developer']}\n"
            f"📅 *الإصدار:* "
            f"{game['release']}\n"
            f"🎭 *النوع:* "
            f"{game['genre']}\n"
            f"🖥️ *المنصات:* "
            f"{game['platforms']}\n"
            f"⭐ *التقييم:* "
            f"{game['rating']}\n\n"
            "🌐 تم العثور على اللعبة من مصدر خارجي."
        )

    return (
        "🎮 *Game Information*\n\n"
        f"🎮 *{game['name']}*\n\n"
        f"📝 *Description:*\n"
        f"{game['description']}\n\n"
        f"👨‍💻 *Developer:* "
        f"{game['developer']}\n"
        f"📅 *Release:* "
        f"{game['release']}\n"
        f"🎭 *Genre:* "
        f"{game['genre']}\n"
        f"🖥️ *Platforms:* "
        f"{game['platforms']}\n"
        f"⭐ *Rating:* "
        f"{game['rating']}\n\n"
        "🌐 Found using an external game database."
    )


# =========================================================
# Aliases
# =========================================================

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
# أدوات عامة
# =========================================================

def normalize_game_name(
    value: str,
):

    normalized = " ".join(
        value.strip().casefold().split()
    )

    return normalized.replace(
        "’",
        "'",
    )


def find_game_id(
    game_name: str,
):

    normalized = normalize_game_name(
        game_name
    )

    if normalized in GAME_ALIASES:

        return GAME_ALIASES[
            normalized
        ]

    for game_id, game in games.items():

        names = [
            game["name"],
            game_id,
            *game.get(
                "aliases",
                []
            ),
        ]

        normalized_names = {
            normalize_game_name(
                name
            )
            for name in names
        }

        if normalized in normalized_names:

            return game_id

    return None


def get_language(
    context,
):

    return context.user_data.get(
        "language",
        "ar",
    )


# =========================================================
# القائمة
# =========================================================

def menu_text(
    language,
):

    if language == "ar":

        return (
            "🎮 اختر اللعبة التي تريد "
            "معرفة معلومات عنها:"
        )

    return (
        "🎮 Choose a game to get "
        "information about:"
    )


def back_markup(
    language,
):

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


def get_game_buttons(
    language,
):

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

    game = games[
        game_id
    ]

    info = game[
        language
    ]

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
        f"⭐ *Critic Rating:*\n"
        f"{game['rating']}"
    )


# =========================================================
# اكتشف لعبة
# =========================================================

def choose_random_game(
    context,
):

    available = [

        game_id

        for game_id in games

        if game_id not in {
            "reddeadredemption",
            "reddeadredemption2",
        }

    ]

    previous = context.user_data.get(
        "discovered_game"
    )

    if (
        previous in available
        and len(available) > 1
    ):

        available.remove(
            previous
        )

    game_id = random.choice(
        available
    )

    context.user_data[
        "discovered_game"
    ] = game_id

    return game_id


def discover_text(
    game_id,
    language,
):

    game = games[
        game_id
    ]

    info = game[
        language
    ]

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


def discover_markup(
    language,
):

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


async def discover_game(
    update,
    context,
):

    query = update.callback_query

    await query.answer()

    language = get_language(
        context
    )

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
    update,
    context,
):

    query = update.callback_query

    await query.answer()

    language = get_language(
        context
    )

    game_id = context.user_data.get(
        "discovered_game"
    )

    if not game_id:

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


# =========================================================
# Red Dead
# =========================================================

def red_dead_markup(
    language,
):

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
                "🔙 رجوع"
                if language == "ar"
                else "🔙 Back",
                callback_data="back",
            )
        ],

    ])


async def red_dead_menu(
    update,
    context,
):

    query = update.callback_query

    await query.answer()

    language = get_language(
        context
    )

    text = (

        "🤠 *Red Dead*\n\nأي لعبة تقصد?"

        if language == "ar"

        else

        "🤠 *Red Dead*\n\nWhich game do you mean?"

    )

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=red_dead_markup(
            language
        ),
    )


# =========================================================
# PostgreSQL
# =========================================================


def get_db_connection():

    if not DATABASE_URL:

        raise RuntimeError(
            "DATABASE_URL غير موجود"
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
                    requested_at TIMESTAMPTZ NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending'
                )
            """)

            # إضافة الحالة للجدول القديم إذا كان موجودًا
            cur.execute("""
                ALTER TABLE game_requests
                ADD COLUMN IF NOT EXISTS status
                TEXT NOT NULL DEFAULT 'pending'
            """)

        conn.commit()

    print(
        "✅ Main database initialized.",
        flush=True,
    )


# =========================================================
# تسجيل المستخدم
# =========================================================

def register_user(
    update,
    language="ar",
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
                    VALUES
                    (
                        %s, %s, %s,
                        %s, %s, %s
                    )

                    ON CONFLICT (user_id)
                    DO UPDATE SET
                        username =
                            EXCLUDED.username,
                        first_name =
                            EXCLUDED.first_name,
                        last_seen_at =
                            EXCLUDED.last_seen_at
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
            f"❌ Database error: {error}",
            flush=True,
        )


def update_user_language(
    update,
    language,
):

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
                    datetime.now(
                        timezone.utc
                    ),
                    user.id,
                ))

            conn.commit()

    except Exception as error:

        print(
            f"❌ Database error: {error}",
            flush=True,
        )


# =========================================================
# إحصائيات الأدمن
# =========================================================

async def stats_command(
    update,
    context,
):

    user = update.effective_user

    if (
        not user
        or not update.message
    ):
        return

    if (
        not ADMIN_ID
        or str(user.id)
        != str(ADMIN_ID).strip()
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

                total = int(
                    cur.fetchone()[
                        "total"
                    ]
                )

                cur.execute("""
                    SELECT COUNT(*) AS today
                    FROM users
                    WHERE
                        (
                            first_seen_at
                            AT TIME ZONE
                            'Asia/Riyadh'
                        )::date
                        =
                        (
                            NOW()
                            AT TIME ZONE
                            'Asia/Riyadh'
                        )::date
                """)

                today = int(
                    cur.fetchone()[
                        "today"
                    ]
                )

                cur.execute("""
                    SELECT COUNT(*) AS last_7_days
                    FROM users
                    WHERE first_seen_at >=
                        NOW() - INTERVAL '7 days'
                """)

                last_7_days = int(
                    cur.fetchone()[
                        "last_7_days"
                    ]
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
            f"❌ Database error: {error}",
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
        f"👤 آخر مستخدم جديد:\n"
        f"{latest_name}"
    )

    await update.message.reply_text(
        message
    )


# =========================================================
# طلبات الألعاب
# =========================================================

async def requests_command(
    update,
    context,
):

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
                        id,
                        game_name,
                        username,
                        user_id,
                        status
                    FROM game_requests
                    ORDER BY requested_at DESC
                """)

                rows = cur.fetchall()

    except Exception as error:

        print(
            f"❌ Database error: {error}",
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

    keyboard = []

    for index, item in enumerate(rows, start=1):

        request_id = item["id"]
        game_name = item["game_name"]
        username = item["username"]
        status = item["status"]

        if username:
            display_name = f"@{username}"
        else:
            display_name = f"ID: {item['user_id']}"

        if status == "approved":

            status_text = "🟢 تمت الإضافة"

        else:

            status_text = "🟡 قيد المراجعة"

        lines.extend([
            f"{index}. 🎮 {game_name}",
            f"   👤 {display_name}",
            f"   {status_text}",
            "",
        ])

        if status != "approved":

            keyboard.append([
                InlineKeyboardButton(
                    f"✅ تمت إضافة {game_name}"[:60],
                    callback_data=f"approve_request:{request_id}",
                )
            ])

    lines.append(
        f"📊 إجمالي الطلبات: {len(rows)}"
    )

    await update.message.reply_text(
        "\n".join(lines)[:4000],
        reply_markup=InlineKeyboardMarkup(keyboard)
        if keyboard
        else None,
    )


async def approve_request(
    update,
    context,
):

    query = update.callback_query

    print(
        f"🔘 APPROVE BUTTON PRESSED: {query.data}",
        flush=True,
    )

    user = update.effective_user

    if not user:
        await query.answer(
            "❌ المستخدم غير موجود.",
            show_alert=True,
        )
        return

    if (
        not ADMIN_ID
        or str(user.id) != str(ADMIN_ID).strip()
    ):

        await query.answer(
            "❌ غير مصرح لك.",
            show_alert=True,
        )
        return

    try:

        request_id = int(
            query.data.split(":", 1)[1]
        )

    except (ValueError, IndexError):

        await query.answer(
            "❌ رقم الطلب غير صالح.",
            show_alert=True,
        )
        return

    try:

        with get_db_connection() as conn:

            with conn.cursor() as cur:

                cur.execute("""
                    UPDATE game_requests
                    SET status = 'approved'
                    WHERE id = %s
                    RETURNING id, game_name
                """, (
                    request_id,
                ))

                row = cur.fetchone()

            conn.commit()

        if not row:

            await query.answer(
                "❌ الطلب غير موجود في قاعدة البيانات.",
                show_alert=True,
            )
            return

        game_name = row["game_name"]

        await query.answer(
            "✅ تمت الإضافة!",
        )

        await query.edit_message_text(
            f"🎮 *{game_name}*\n\n"
            "🟢 تمت الإضافة",
            parse_mode="Markdown",
        )

        print(
            f"✅ Request {request_id} approved: {game_name}",
            flush=True,
        )

    except Exception as error:

        print(
            f"❌ Approve request error: {error}",
            flush=True,
        )

        await query.answer(
            "❌ حدث خطأ أثناء تحديث الطلب.",
            show_alert=True,
        )
    
    
# =========================================================
# القائمة
# =========================================================

async def send_menu(
    update,
    context,
):

    language = get_language(
        context
    )

    context.user_data.pop(
        "input_mode",
        None,
    )

    context.user_data.pop(
        "pending_game_request",
        None,
    )

    # استخدام القائمة الجديدة من telegram_bot3.py
    if update.callback_query:

        await update.callback_query.edit_message_text(
            bot3_menu_text(
                language
            ),
            parse_mode="Markdown",
            reply_markup=bot3_main_menu(
                language
            ),
        )

    else:

        await update.message.reply_text(
            bot3_menu_text(
                language
            ),
            parse_mode="Markdown",
            reply_markup=bot3_main_menu(
                language
            ),
        )


# =========================================================
# Start
# =========================================================

async def start(
    update,
    context,
):

    register_user(
        update
    )

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


async def choose_language(
    update,
    context,
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


# =========================================================
# عرض اللعبة
# =========================================================

async def show_game(
    update,
    context,
):

    query = update.callback_query

    await query.answer()

    game_id = query.data

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
        reply_markup=back_markup(
            language
        ),
    )


# =========================================================
# البحث والطلبات
# =========================================================

def prompt_text(
    language,
    mode,
):

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


async def begin_search(
    update,
    context,
):

    query = update.callback_query

    await query.answer()

    language = get_language(
        context
    )

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
    update,
    context,
):

    query = update.callback_query

    await query.answer()

    language = get_language(
        context
    )

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
    update,
    context,
):

    query = update.callback_query

    await query.answer()

    language = get_language(
        context
    )

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


async def handle_text(
    update,
    context,
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

    game_name = update.message.text.strip()

    language = get_language(
        context
    )

    context.user_data.pop(
        "input_mode",
        None,
    )

    # =====================================================
    # إذا المستخدم لم يكتب اسم لعبة
    # =====================================================

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

    # =====================================================
    # البحث عن لعبة
    # =====================================================

    if mode == "search":

        # -------------------------------------------------
        # البحث داخل الألعاب الموجودة في البوت
        # -------------------------------------------------

        game_id = find_game_id(
            game_name
        )

        # -------------------------------------------------
        # Red Dead
        # -------------------------------------------------

        if game_id == "red_dead":

            await update.message.reply_text(
                (
                    "🤠 *Red Dead*\n\nأي لعبة تقصد؟"
                    if language == "ar"
                    else
                    "🤠 *Red Dead*\n\nWhich game do you mean?"
                ),
                parse_mode="Markdown",
                reply_markup=red_dead_markup(
                    language
                ),
            )

            return

        # -------------------------------------------------
        # اللعبة موجودة بالفعل في البوت
        # -------------------------------------------------

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

        # =================================================
        # اللعبة غير موجودة في البوت
        # نبحث عنها في قاعدة الألعاب الخارجية
        # =================================================

        external_game = search_game_external(
            game_name
        )

        # -------------------------------------------------
        # وجدنا اللعبة خارج البوت
        # -------------------------------------------------

        if external_game:

            context.user_data[
                "pending_game_request"
            ] = external_game["name"]

            text = external_game_info_text(
                external_game,
                language,
            )

            # إضافة تنبيه للمستخدم بأن اللعبة
            # ليست موجودة داخل البوت حالياً

            if language == "ar":

                text += (
                    "\n\n"
                    "ℹ️ هذه اللعبة غير مضافة إلى قائمة البوت حاليًا.\n"
                    "يمكنك طلب إضافتها من الزر بالأسفل."
                )

                request_button = (
                    f"➕ طلب إضافة {external_game['name']}"
                )

            else:

                text += (
                    "\n\n"
                    "ℹ️ This game is not currently in the bot's list.\n"
                    "You can request it using the button below."
                )

                request_button = (
                    f"➕ Request {external_game['name']}"
                )

            await update.message.reply_text(

                text,

                parse_mode="Markdown",

                reply_markup=InlineKeyboardMarkup([

                    [
                        InlineKeyboardButton(
                            request_button[:60],
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

        # =================================================
        # البحث الخارجي لم يجد اللعبة
        # نرجع لنظام طلب اللعبة القديم
        # =================================================

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

    # =====================================================
    # وضع طلب لعبة مباشرة
    # =====================================================

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

async def back(
    update,
    context,
):

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
            "❌ DATABASE_URL غير موجود",
            flush=True,
        )

        return

    init_database()

    init_quiz_database()

    app = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    app.add_handler(
        CommandHandler(
            "requests",
            requests_command,
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            approve_request,
            pattern=r"^approve_request:\d+$",
        )
    )

    app.add_handler(
        CommandHandler(
            "stats",
            stats_command,
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            choose_language,
            pattern=r"^language_(ar|en)$",
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            discover_game,
            pattern=r"^discover_game$",
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            discover_info,
            pattern=r"^discover_info$",
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            red_dead_menu,
            pattern=r"^red_dead$",
        )
    )

    register_quiz_handlers(
        app
    )

    register_bot3_handlers(
        app
    )

    app.add_handler(
        CallbackQueryHandler(
            show_game,
            pattern=(
                r"^(minecraft|roblox|fortnite|"
                r"valorant|rocketleague|"
                r"brawlstars|gtav|genshinimpact|"
                r"clashroyale|overwatch|eldenring|bloodborne|"
                r"reddeadredemption|"
                r"reddeadredemption2)$"
            ),
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            begin_search,
            pattern=r"^search_game$",
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            begin_request,
            pattern=r"^request_game$",
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            request_searched_game,
            pattern=r"^request_searched_game$",
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            back,
            pattern=r"^back$",
        )
    )

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