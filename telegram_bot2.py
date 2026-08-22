telegram_bot2.py

import json
import os

=========================

Settings

=========================

PLAYERS_FILE = “players.json”

XP_PER_LEVEL = 100

=========================

File handling

=========================

def load_players():
“”“تحميل بيانات اللاعبين من players.json”””

if not os.path.exists(PLAYERS_FILE):
    return {}
try:
    with open(
        PLAYERS_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)
except (json.JSONDecodeError, OSError):
    return {}

def save_players(players):
“”“حفظ بيانات اللاعبين”””

with open(
    PLAYERS_FILE,
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        players,
        file,
        ensure_ascii=False,
        indent=2,
    )

=========================

Player

=========================

def get_player(user_id):
“”“إنشاء اللاعب إذا لم يكن موجودًا”””

players = load_players()
user_id = str(user_id)
if user_id not in players:
    players[user_id] = {
        "xp": 0,
        "level": 1,
        "streak": 0,
        "quizzes": 0,
        "challenges": 0,
    }
    save_players(players)
return players[user_id]

=========================

Level system

=========================

def calculate_level(xp):
“”“حساب مستوى اللاعب من XP”””

return (xp // XP_PER_LEVEL) + 1

def xp_to_next_level(xp):
“”“كم XP يحتاج اللاعب للمستوى التالي”””

level = calculate_level(xp)
next_level_xp = level * XP_PER_LEVEL
return next_level_xp - xp

=========================

Add XP

=========================

def add_xp(
user_id,
amount,
source=None,
):
“””
إضافة XP للاعب.

يرجع:
{
    "xp": XP الحالي,
    "level": المستوى,
    "leveled_up": هل ارتفع المستوى؟
}
"""
players = load_players()
user_id = str(user_id)
if user_id not in players:
    players[user_id] = {
        "xp": 0,
        "level": 1,
        "streak": 0,
        "quizzes": 0,
        "challenges": 0,
    }
player = players[user_id]
old_level = calculate_level(
    player["xp"]
)
player["xp"] += max(0, int(amount))
new_level = calculate_level(
    player["xp"]
)
player["level"] = new_level
if source == "quiz":
    player["quizzes"] += 1
elif source == "challenge":
    player["challenges"] += 1
save_players(players)
return {
    "xp": player["xp"],
    "level": new_level,
    "leveled_up": new_level > old_level,
}

=========================

Streak

=========================

def increase_streak(user_id):
“”“زيادة سلسلة الإجابات الصحيحة”””

players = load_players()
user_id = str(user_id)
if user_id not in players:
    get_player(user_id)
    players = load_players()
players[user_id]["streak"] += 1
save_players(players)
return players[user_id]["streak"]

def reset_streak(user_id):
“”“تصفير السلسلة”””

players = load_players()
user_id = str(user_id)
if user_id in players:
    players[user_id]["streak"] = 0
    save_players(players)

=========================

Player stats

=========================

def get_stats(user_id):
“”“إرجاع إحصائيات اللاعب”””

player = get_player(user_id)
return {
    "xp": player["xp"],
    "level": player["level"],
    "streak": player["streak"],
    "quizzes": player["quizzes"],
    "challenges": player["challenges"],
    "xp_to_next": xp_to_next_level(
        player["xp"]
    ),
}

=========================

Profile text

=========================

def profile_text(user_id):
“”“إنشاء نص ملف اللاعب”””

stats = get_stats(user_id)
return (
    "🎮 ملفك في البوت\n\n"
    f"🏆 المستوى: {stats['level']}\n"
    f"⭐ XP: {stats['xp']}\n"
    f"📈 XP للمستوى التالي: "
    f"{stats['xp_to_next']}\n"
    f"🔥 السلسلة: {stats['streak']}\n"
    f"🧠 الاختبارات: {stats['quizzes']}\n"
    f"🎯 التحديات: {stats['challenges']}"
)
