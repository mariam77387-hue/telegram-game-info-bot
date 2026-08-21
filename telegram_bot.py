import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

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
REQUESTS_FILE = Path(os.getenv("GAME_REQUESTS_FILE", "game_requests.json"))


# =========================
# Game information
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
        "aliases": ["gta 5", "grand theft auto v", "grand theft auto 5"],
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
}


GAME_ALIASES = {
    "gta v": "gtav",
    "gta 5": "gtav",
    "grand theft auto v": "gtav",
    "grand theft auto 5": "gtav",
}


def normalize_game_name(value: str) -> str:
    normalized = " ".join(value.strip().casefold().split())
    return normalized.replace("’", "'")


def find_game_id(game_name: str) -> str | None:
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


def get_language(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("language", "ar")


def menu_text(language: str) -> str:
    if language == "ar":
        return "🎮 اختر اللعبة التي تريد معرفة معلومات عنها:"

    return "🎮 Choose a game to get information about:"


def get_game_buttons(language: str) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                f"{game['emoji']} {game['name']}",
                callback_data=game_id,
            )
        ]
        for game_id, game in games.items()
    ]

    if language == "ar":
        keyboard.extend(
            [
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


def back_markup(language: str) -> InlineKeyboardMarkup:
    label = "🔙 رجوع" if language == "ar" else "🔙 Back"

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


def game_info_text(game_id: str, language: str) -> str:
    game = games[game_id]
    info = game[language]

    if language == "ar":
        return (
            f"{game['emoji']} *{game['name']}*\n\n"
            f"📖 *الوصف:*\n{info['description']}\n\n"
            f"👨‍💻 *المطور:*\n{info['developer']}\n\n"
            f"📅 *تاريخ الإصدار:*\n{info['release']}\n\n"
            f"🎯 *النوع:*\n{info['genre']}\n\n"
            f"💻 *المنصات:*\n{info['platforms']}"
        )

    return (
        f"{game['emoji']} *{game['name']}*\n\n"
        f"📖 *Description:*\n{info['description']}\n\n"
        f"👨‍💻 *Developer:*\n{info['developer']}\n\n"
        f"📅 *Release Date:*\n{info['release']}\n\n"
        f"🎯 *Genre:*\n{info['genre']}\n\n"
        f"💻 *Platforms:*\n{info['platforms']}"
    )


# =========================
# Game requests
# =========================

def load_requests() -> list[dict]:
    try:
        with REQUESTS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (
        FileNotFoundError,
        json.JSONDecodeError,
        OSError,
    ):
        return []


def save_requests(requests: list[dict]) -> None:
    REQUESTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=REQUESTS_FILE.parent,
            prefix=f".{REQUESTS_FILE.name}.",
            delete=False,
        ) as file:

            json.dump(
                requests,
                file,
                ensure_ascii=False,
                indent=2,
            )

            file.write("\n")
            temporary_path = Path(file.name)

        temporary_path.replace(REQUESTS_FILE)

    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()


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
                "✅ هذه اللعبة متوفرة بالفعل في البوت.",
            )

        return (
            False,
            "✅ This game is already available in the bot.",
        )

    requests = load_requests()

    normalized = normalize_game_name(game_name)

    user = update.effective_user

    # كل طلب من المستخدم يسجل كطلب مستقل
    requests.append(
        {
            "game_name": game_name,
            "normalized_name": normalized,
            "user_id": user.id if user else None,
            "username": user.username if user else None,
            "language": language,
            "requested_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }
    )

    save_requests(requests)

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

    admin_id = os.getenv("ADMIN_ID")

    if not admin_id or str(user.id) != str(admin_id).strip():
        await update.message.reply_text(
            "❌ You are not authorized to use this command."
        )
        return

    requests = load_requests()

    if not requests:
        await update.message.reply_text(
            "📋 لا توجد طلبات ألعاب حتى الآن."
        )
        return

    grouped = {}

    for item in requests:
        normalized_name = item.get(
            "normalized_name",
            "",
        )

        game_name = item.get(
            "game_name",
            "Unknown",
        )

        if not normalized_name:
            normalized_name = normalize_game_name(
                game_name
            )

        if normalized_name not in grouped:
            grouped[normalized_name] = {
                "name": game_name,
                "count": 0,
            }

        grouped[normalized_name]["count"] += 1

    sorted_requests = sorted(
        grouped.values(),
        key=lambda item: item["count"],
        reverse=True,
    )

    lines = [
        "📋 طلبات الألعاب",
        "",
    ]

    total = 0

    for index, item in enumerate(
        sorted_requests,
        start=1,
    ):
        count = item["count"]
        total += count

        if count == 1:
            request_word = "طلب"
        elif count == 2:
            request_word = "طلبان"
        else:
            request_word = "طلبات"

        lines.append(
            f"{index}. 🎮 {item['name']} — "
            f"{count} {request_word}"
        )

    lines.extend(
        [
            "",
            f"📊 إجمالي الطلبات: {total}",
        ]
    )

    # Telegram message limit protection
    message = "\n".join(lines)

    if len(message) <= 4000:
        await update.message.reply_text(message)
        return

    # إرسال النتائج على أكثر من رسالة إذا كانت كثيرة
    current = "📋 طلبات الألعاب\n\n"

    for line in lines[2:]:
        if len(current) + len(line) + 1 > 3900:
            await update.message.reply_text(current)
            current = ""

        current += line + "\n"

    if current.strip():
        await update.message.reply_text(current)


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
            reply_markup=get_game_buttons(language),
        )

    else:
        await update.message.reply_text(
            menu_text(language),
            reply_markup=get_game_buttons(language),
        )


# =========================
# Start and language
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

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

    context.user_data["language"] = (
        query.data.replace(
            "language_",
            "",
        )
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
        reply_markup=back_markup(language),
    )


async def show_searched_game(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    game_id = context.user_data.get(
        "searched_game_id"
    )

    if game_id not in games:
        await send_menu(
            update,
            context,
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
        reply_markup=back_markup(language),
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
            "🔎 اكتب اسم اللعبة التي تريد البحث عنها:"
            if language == "ar"
            else "🔎 Enter the name of the game you want to search for:"
        )

    return (
        "🎮 اكتب اسم اللعبة التي تريد إضافتها:"
        if language == "ar"
        else "🎮 Enter the name of the game you want to request:"
    )


async def begin_search(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    language = get_language(context)

    context.user_data["input_mode"] = "search"

    await query.edit_message_text(
        prompt_text(
            language,
            "search",
        ),
        reply_markup=back_markup(language),
    )


async def begin_request(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    language = get_language(context)

    context.user_data["input_mode"] = "request"

    await query.edit_message_text(
        prompt_text(
            language,
            "request",
        ),
        reply_markup=back_markup(language),
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
        reply_markup=back_markup(language),
    )


async def handle_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    mode = context.user_data.get(
        "input_mode"
    )

    if (
        mode not in {"search", "request"}
        or not update.message
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
            reply_markup=back_markup(language),
        )

        context.user_data["input_mode"] = mode
        return

    if mode == "search":

        game_id = find_game_id(game_name)

        if game_id:

            context.user_data[
                "searched_game_id"
            ] = game_id

            await update.message.reply_text(
                game_info_text(
                    game_id,
                    language,
                ),
                parse_mode="Markdown",
                reply_markup=back_markup(language),
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
        reply_markup=back_markup(language),
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
            "❌ BOT_TOKEN غير موجود في Secrets"
        )
        return

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
            choose_language,
            pattern=r"^language_(ar|en)$",
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            show_game,
            pattern=(
                r"^(minecraft|roblox|fortnite|"
                r"valorant|rocketleague|"
                r"brawlstars|gtav|genshinimpact|"
                r"clashroyale)$"
            ),
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            show_searched_game,
            pattern=r"^searched_game$",
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

    print("🤖 البوت يعمل الآن...")

    app.run_polling()


if __name__ == "__main__":
    main()