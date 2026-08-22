# telegram_bot2.py

import os
import random

import psycopg
from psycopg.rows import dict_row

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler


DATABASE_URL = os.getenv("DATABASE_URL")


# =========================================================
# PostgreSQL
# =========================================================

def get_db_connection():

    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL غير موجود في Environment Variables"
        )

    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row,
    )


def init_quiz_database():

    with get_db_connection() as conn:

        with conn.cursor() as cur:

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
        "✅ Quiz database initialized.",
        flush=True,
    )


# =========================================================
# أسئلة تحدي الألعاب
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
            "نيويورك",
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
        "question_ar": "أي لعبة تدور أحداثها في الغرب الأمريكي؟",
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
        "question_ar": "أي لعبة تعتبر منصة لصناعة ولعب تجارب مختلفة؟",
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

    {
        "question_ar": "من مطور Fortnite؟",
        "question_en": "Who developed Fortnite?",
        "answers_ar": [
            "Epic Games",
            "Riot Games",
            "Mojang Studios",
            "Supercell",
        ],
        "answers_en": [
            "Epic Games",
            "Riot Games",
            "Mojang Studios",
            "Supercell",
        ],
        "correct": 0,
    },

    {
        "question_ar": "أي لعبة طورتها Supercell؟",
        "question_en": "Which game was developed by Supercell?",
        "answers_ar": [
            "Clash Royale",
            "Valorant",
            "GTA V",
            "Elden Ring",
        ],
        "answers_en": [
            "Clash Royale",
            "Valorant",
            "GTA V",
            "Elden Ring",
        ],
        "correct": 0,
    },

    {
        "question_ar": "من مطور Red Dead Redemption 2؟",
        "question_en": "Who developed Red Dead Redemption 2?",
        "answers_ar": [
            "Rockstar Studios",
            "Epic Games",
            "Blizzard",
            "Riot Games",
        ],
        "answers_en": [
            "Rockstar Studios",
            "Epic Games",
            "Blizzard",
            "Riot Games",
        ],
        "correct": 0,
    },

    {
        "question_ar": "أي لعبة تحتوي على شخصيات Agents بقدرات مختلفة؟",
        "question_en": "Which game features Agents with different abilities?",
        "answers_ar": [
            "Valorant",
            "Minecraft",
            "Rocket League",
            "Clash Royale",
        ],
        "answers_en": [
            "Valorant",
            "Minecraft",
            "Rocket League",
            "Clash Royale",
        ],
        "correct": 0,
    },

    {
        "question_ar": "من مطور Genshin Impact؟",
        "question_en": "Who developed Genshin Impact?",
        "answers_ar": [
            "HoYoverse",
            "Supercell",
            "Rockstar Games",
            "Mojang Studios",
        ],
        "answers_en": [
            "HoYoverse",
            "Supercell",
            "Rockstar Games",
            "Mojang Studios",
        ],
        "correct": 0,
    },

    {
        "question_ar": "أي لعبة تشتهر بالبناء والبقاء في عالم مفتوح؟",
        "question_en": "Which game is famous for building and survival in an open world?",
        "answers_ar": [
            "Minecraft",
            "Valorant",
            "Overwatch",
            "Brawl Stars",
        ],
        "answers_en": [
            "Minecraft",
            "Valorant",
            "Overwatch",
            "Brawl Stars",
        ],
        "correct": 0,
    },
]


# =========================================================
# اللغة
# =========================================================

def get_language(context):

    return context.user_data.get(
        "language",
        "ar",
    )


# =========================================================
# اختيار سؤال جديد
# =========================================================

def get_quiz_question(context):

    previous = context.user_data.get(
        "quiz_question"
    )

    choices = list(
        range(len(quiz_questions))
    )

    if (
        previous is not None
        and len(choices) > 1
        and previous in choices
    ):
        choices.remove(previous)

    index = random.choice(
        choices
    )

    context.user_data[
        "quiz_question"
    ] = index

    return quiz_questions[index]


# =========================================================
# تجهيز الإجابات بشكل عشوائي
# =========================================================

def prepare_quiz_answers(
    context,
    question,
    language,
):

    answers = (
        question["answers_ar"]
        if language == "ar"
        else question["answers_en"]
    )

    # الإجابة الصحيحة الأصلية
    correct_index = question["correct"]

    correct_answer = answers[
        correct_index
    ]

    # نسوي قائمة جديدة مع رقم الإجابة الأصلية
    answer_items = []

    for index, answer in enumerate(
        answers
    ):
        answer_items.append(
            {
                "answer": answer,
                "original_index": index,
            }
        )

    # نخلط الإجابات
    random.shuffle(
        answer_items
    )

    # نعرف مكان الإجابة الصحيحة بعد الخلط
    shuffled_correct_index = 0

    for index, item in enumerate(
        answer_items
    ):

        if item["original_index"] == correct_index:

            shuffled_correct_index = index

            break

    # نخزن ترتيب الإجابات لهذا السؤال
    context.user_data[
        "quiz_answers"
    ] = answer_items

    context.user_data[
        "quiz_correct"
    ] = shuffled_correct_index

    return answer_items


# =========================================================
# شكل أزرار الإجابات
# =========================================================

def quiz_markup(
    context,
    language,
):

    answer_items = context.user_data.get(
        "quiz_answers",
        [],
    )

    keyboard = []

    for index, item in enumerate(
        answer_items
    ):

        answer = item["answer"]

        keyboard.append([
            InlineKeyboardButton(
                f"{chr(65 + index)}) {answer}",
                callback_data=f"quiz_answer_{index}",
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            "🔙 رجوع"
            if language == "ar"
            else "🔙 Back",
            callback_data="back",
        )
    ])

    return InlineKeyboardMarkup(
        keyboard
    )


# =========================================================
# نص السؤال
# =========================================================

def quiz_question_text(
    question,
    language,
):

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


# =========================================================
# بدء التحدي
# =========================================================

async def quiz_start(
    update,
    context,
):

    query = update.callback_query

    await query.answer()

    language = get_language(
        context
    )

    question = get_quiz_question(
        context
    )

    # مهم:
    # كل مرة نبدأ سؤال جديد نخلط الإجابات
    prepare_quiz_answers(
        context,
        question,
        language,
    )

    await query.edit_message_text(
        quiz_question_text(
            question,
            language,
        ),
        parse_mode="Markdown",
        reply_markup=quiz_markup(
            context,
            language,
        ),
    )


# =========================================================
# الحصول على نقاط اللاعب
# =========================================================

def get_quiz_score(
    user_id,
):

    with get_db_connection() as conn:

        with conn.cursor() as cur:

            cur.execute("""
                SELECT *
                FROM quiz_scores
                WHERE user_id = %s
            """, (
                user_id,
            ))

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
                VALUES
                (%s, 0, 0, 0, 0, 0)
                RETURNING *
            """, (
                user_id,
            ))

            row = cur.fetchone()

        conn.commit()

    return row


# =========================================================
# تحديث النقاط
# =========================================================

def update_quiz_score(
    user,
    correct,
):

    with get_db_connection() as conn:

        with conn.cursor() as cur:

            cur.execute("""
                SELECT
                    xp,
                    correct_answers,
                    wrong_answers,
                    best_streak,
                    current_streak
                FROM quiz_scores
                WHERE user_id = %s
                FOR UPDATE
            """, (
                user.id,
            ))

            current = cur.fetchone()

            if not current:

                old_xp = 0
                old_correct = 0
                old_wrong = 0
                old_best = 0
                old_streak = 0

            else:

                old_xp = current["xp"]
                old_correct = current[
                    "correct_answers"
                ]
                old_wrong = current[
                    "wrong_answers"
                ]
                old_best = current[
                    "best_streak"
                ]
                old_streak = current[
                    "current_streak"
                ]

            if correct:

                new_xp = old_xp + 10
                new_correct = old_correct + 1
                new_wrong = old_wrong

                new_streak = old_streak + 1

                new_best = max(
                    old_best,
                    new_streak,
                )

            else:

                new_xp = old_xp
                new_correct = old_correct
                new_wrong = old_wrong + 1

                new_streak = 0
                new_best = old_best

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
                VALUES
                (
                    %s, %s, %s, %s,
                    %s, %s, %s, %s
                )

                ON CONFLICT (user_id)
                DO UPDATE SET
                    username = EXCLUDED.username,
                    first_name = EXCLUDED.first_name,
                    xp = EXCLUDED.xp,
                    correct_answers = EXCLUDED.correct_answers,
                    wrong_answers = EXCLUDED.wrong_answers,
                    best_streak = EXCLUDED.best_streak,
                    current_streak = EXCLUDED.current_streak
            """, (
                user.id,
                user.username,
                user.first_name,
                new_xp,
                new_correct,
                new_wrong,
                new_best,
                new_streak,
            ))

        conn.commit()

    return {
        "xp": new_xp,
        "correct_answers": new_correct,
        "wrong_answers": new_wrong,
        "best_streak": new_best,
        "current_streak": new_streak,
    }


# =========================================================
# الإجابة
# =========================================================

async def quiz_answer(
    update,
    context,
):

    query = update.callback_query

    await query.answer()

    user = update.effective_user

    if not user:
        return

    language = get_language(
        context
    )

    question_index = context.user_data.get(
        "quiz_question"
    )

    if question_index is None:

        await quiz_start(
            update,
            context,
        )

        return

    question = quiz_questions[
        question_index
    ]

    try:

        selected = int(
            query.data.replace(
                "quiz_answer_",
                "",
            )
        )

    except ValueError:

        return

    # الإجابة الصحيحة التي تم تحديدها
    # بعد خلط الخيارات
    correct_index = context.user_data.get(
        "quiz_correct"
    )

    if correct_index is None:

        await quiz_start(
            update,
            context,
        )

        return

    is_correct = (
        selected == correct_index
    )

    score = update_quiz_score(
        user,
        is_correct,
    )

    # الإجابة الصحيحة المعروضة
    answer_items = context.user_data.get(
        "quiz_answers",
        [],
    )

    if (
        correct_index >= 0
        and correct_index < len(answer_items)
    ):

        correct_answer = answer_items[
            correct_index
        ]["answer"]

    else:

        correct_answer = "غير معروفة"

    if is_correct:

        if language == "ar":

            message = (
                "🎉 *إجابة صحيحة!*\n\n"
                "⭐ +10 XP\n"
                f"🔥 السلسلة الحالية: "
                f"{score['current_streak']}\n\n"
                f"🏆 مجموع XP: "
                f"{score['xp']}"
            )

        else:

            message = (
                "🎉 *Correct answer!*\n\n"
                "⭐ +10 XP\n"
                f"🔥 Current streak: "
                f"{score['current_streak']}\n\n"
                f"🏆 Total XP: "
                f"{score['xp']}"
            )

    else:

        if language == "ar":

            message = (
                "❌ *إجابة خاطئة!*\n\n"
                f"✅ الإجابة الصحيحة: "
                f"{correct_answer}\n\n"
                "🔥 السلسلة رجعت إلى 0\n"
                f"🏆 مجموع XP: "
                f"{score['xp']}"
            )

        else:

            message = (
                "❌ *Wrong answer!*\n\n"
                f"✅ Correct answer: "
                f"{correct_answer}\n\n"
                "🔥 Streak reset to 0\n"
                f"🏆 Total XP: "
                f"{score['xp']}"
            )

    keyboard = [

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
                "🏆 إحصائياتي"
                if language == "ar"
                else "🏆 My Stats",
                callback_data="quiz_stats",
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

    await query.edit_message_text(
        message,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            keyboard
        ),
    )


# =========================================================
# إحصائيات اللاعب
# =========================================================

async def quiz_stats(
    update,
    context,
):

    query = update.callback_query

    await query.answer()

    user = update.effective_user

    if not user:
        return

    language = get_language(
        context
    )

    score = get_quiz_score(
        user.id
    )

    xp = score["xp"]

    correct = score[
        "correct_answers"
    ]

    wrong = score[
        "wrong_answers"
    ]

    best = score[
        "best_streak"
    ]

    current = score[
        "current_streak"
    ]

    level = (xp // 50) + 1

    xp_in_level = xp % 50

    if xp_in_level == 0:
        xp_remaining = 50
    else:
        xp_remaining = 50 - xp_in_level

    if language == "ar":

        text = (
            "🏆 *إحصائيات تحدي الألعاب*\n\n"
            f"⭐ XP: {xp}\n"
            f"📈 المستوى: {level}\n"
            f"🔥 السلسلة الحالية: {current}\n"
            f"🏅 أفضل سلسلة: {best}\n\n"
            f"✅ إجابات صحيحة: {correct}\n"
            f"❌ إجابات خاطئة: {wrong}\n\n"
            f"🎯 تحتاج {xp_remaining} XP "
            "للمستوى التالي."
        )

    else:

        text = (
            "🏆 *Game Challenge Stats*\n\n"
            f"⭐ XP: {xp}\n"
            f"📈 Level: {level}\n"
            f"🔥 Current streak: {current}\n"
            f"🏅 Best streak: {best}\n\n"
            f"✅ Correct answers: {correct}\n"
            f"❌ Wrong answers: {wrong}\n\n"
            f"🎯 You need {xp_remaining} XP "
            "for the next level."
        )

    keyboard = [

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

    ]

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            keyboard
        ),
    )


# =========================================================
# تسجيل Handlers
# =========================================================

def register_quiz_handlers(app):

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