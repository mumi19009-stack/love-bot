# -*- coding: utf-8 -*-
import telebot
from telebot import types
import random
import json
import os
from datetime import datetime, timedelta

TOKEN = '8772865540:AAEZCynp6Xp1ikQFwvRu9VNZlygzpGq5O7g'
bot = telebot.TeleBot(TOKEN)

USER_PASSWORD = '232314421849e2'
ADMIN_PASSWORD = '2tw38293eh4'

START_DATE = datetime(2026, 5, 1, 0, 0, 0)

DATA_FILE = 'bot_data.json'
LOG_FILE = 'bot_logs.json'
PHOTOS_DIR = 'photos'
USERS_FILE = 'users.json'
DIARY_FILE = 'diary.json'
PLAYLIST_FILE = 'playlist.json'
MOVIES_FILE = 'movies.json'
GOALS_FILE = 'goals.json'
EVENTS_FILE = 'events.json'

if not os.path.exists(PHOTOS_DIR):
    os.makedirs(PHOTOS_DIR)

def load_json(file, default):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default

def save_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_json(DATA_FILE, {'photos': [], 'romantic_messages': [
    '❤️ Я тебя безумно люблю! Ты моя вселенная! ❤️',
    '💕 Я скучаю по тебе каждую секунду! 💕',
    '💋 Твои губы - моя слабость! 💋',
    '🌹 Ты самая красивая девушка на свете! 🌹',
    '💗 Моё сердце бьется только для тебя! 💗',
    '🌟 Ты сияешь ярче всех звезд! 🌟',
    '💖 Ты моя половинка, моя душа! 💖',
    '🌸 С тобой я счастлив каждую минуту! 🌸',
    '✨ Ты мое вдохновение и моя мечта! ✨',
    '💝 Ты лучшее, что случилось в моей жизни! 💝',
    '🌺 Ты как прекрасный цветок в моем сердце! 🌺',
    '💞 Наши сердца бьются в унисон! 💞',
    '🌟 Ты мой ангел-хранитель! 🌟',
    '💗 Я хочу просыпаться с тобой каждое утро! 💗',
    '❤️ Ты сделала мою жизнь ярче! ❤️',
    '💕 Мои мысли всегда о тебе! 💕',
    '🌹 Ты моя единственная и неповторимая! 🌹',
    '💖 Каждый день с тобой - это праздник! 💖',
    '🌸 Ты мое солнце и моя радость! 🌸',
    '💗 Я готов на все ради твоей улыбки! 💗',
    '🌟 Ты самая невероятная женщина! 🌟',
    '❤️ Моя любовь к тебе бесконечна! ❤️',
    '💕 Ты - мое счастье и мой покой! 💕',
    '💋 Я хочу целовать тебя вечно! 💋',
    '🌺 Ты как прекрасный сон! 🌺',
    '💖 Ты моя муза и вдохновение! 💖',
    '🌟 С тобой я на вершине мира! 🌟',
    '💗 Ты лучшее, что со мной случалось! 💗',
    '❤️ Я люблю тебя больше всех сокровищ! ❤️',
    '💕 Твои глаза сводят меня с ума! 💕',
    '🌹 Ты моя нежность и забота! 🌹',
    '💖 С каждым днем я люблю тебя сильнее! 💖',
    '🌸 Ты моя весна и лето! 🌸',
    '💗 Ты - моя судьба навечно! 💗',
    '🌟 Ты освещаешь мой путь любовью! 🌟',
    '❤️ Без тебя этот мир пуст! ❤️',
    '💕 Ты моя принцесса и королева! 💕',
    '💋 Я хочу быть с тобой всегда! 💋',
    '🌹 Ты мой самый красивый цветок! 🌹',
    '💖 Ты моя вечная любовь! 💖',
    '🌸 Ты моя радость каждый день! 🌸',
    '💗 Ты моя путеводная звезда! 💗',
    '🌟 С тобой я стал лучше! 🌟',
    '❤️ Ты моя самая большая ценность! ❤️',
    '💕 Ты моя нежность и ласка! 💕',
    '💋 Твои объятия - мой рай! 💋',
    '🌹 Ты моя единственная любовь! 🌹',
    '💖 Я люблю тебя до бесконечности! 💖',
    '🌸 Ты моя улыбка и смех! 🌸',
    '💗 Ты моя жизнь и дыхание! 💗'
]})

logs = load_json(LOG_FILE, {'attempts': [], 'successful': [], 'clicks': []})
users = load_json(USERS_FILE, {})
diary = load_json(DIARY_FILE, [])
playlist = load_json(PLAYLIST_FILE, [])
movies = load_json(MOVIES_FILE, [])
goals = load_json(GOALS_FILE, [])
events = load_json(EVENTS_FILE, [{'name': 'Начало отношений ❤️', 'date': '01.05.2026'}])

verified_users = {}
is_admin = {}
admin_temp = {}

daily_questions = [
    '❤️ Какой момент с нами был самым счастливым?',
    '💕 Что ты чувствуешь ко мне в эту минуту?',
    '💋 За что ты меня любишь больше всего?',
    '🌹 Что я могу сделать, чтобы ты улыбнулась?',
    '💗 Какое наше совместное воспоминание самое теплое?',
    '🌟 Что ты хочешь сказать мне сегодня?',
    '💖 Какая черта во мне тебе нравится больше всего?',
    '🌸 Что ты чувствуешь, когда я рядом?',
    '✨ Какое место ты хочешь посетить со мной?',
    '💝 Что ты хочешь пожелать мне сегодня?'
]

truth_questions = [
    'Какой самый романтичный поступок я совершал?',
    'Что тебе нравится во мне больше всего?',
    'О чем ты думаешь, когда смотришь на меня?',
    'Какая наша самая смешная история?',
    'Что ты чувствовал в нашу первую встречу?',
    'Какое место ты хочешь посетить со мной?',
    'Что я делаю, когда ты счастлива?',
    'Какая твоя самая заветная мечта с тобой?',
    'Что тебя бесит во мне? (честно!)',
    'Когда ты понял, что любишь меня?'
]

dare_actions = [
    'Поцелуй меня в губы (если рядом) 💋',
    'Скажи мне комплимент на 5 разных языках',
    'Обними меня на 30 секунд',
    'Спой мне свою любимую песню',
    'Расскажи стих о любви',
    'Покрути меня и поцелуй',
    'Сделай мне массаж плеч',
    'Потанцуй со мной медленный танец',
    'Шепни мне на ухо что-то приятное',
    'Закрой глаза и представь нашу совместную жизнь'
]

def get_admin_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('📊 Статистика', callback_data='admin_stats'),
        types.InlineKeyboardButton('📝 Логи', callback_data='admin_logs'),
        types.InlineKeyboardButton('📤 Загрузить фото', callback_data='admin_upload'),
        types.InlineKeyboardButton('❌ Удалить все фото', callback_data='admin_delete_photos'),
        types.InlineKeyboardButton('➕ Добавить сообщение', callback_data='admin_add_message'),
        types.InlineKeyboardButton('💬 Написать пользователю', callback_data='admin_send_message'),
        types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu')
    )
    return markup

def main_menu(user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('❤️ Любовь', callback_data='random'),
        types.InlineKeyboardButton('📸 Наши фото', callback_data='photos'),
        types.InlineKeyboardButton('📅 Наша дата', callback_data='our_date'),
        types.InlineKeyboardButton('❓ Вопрос дня', callback_data='question_day'),
        types.InlineKeyboardButton('🎵 Плейлист', callback_data='playlist'),
        types.InlineKeyboardButton('🎬 Кино', callback_data='movies'),
        types.InlineKeyboardButton('📝 Дневник', callback_data='diary'),
        types.InlineKeyboardButton('🗓️ События', callback_data='events'),
        types.InlineKeyboardButton('🌅 Наши цели', callback_data='goals'),
        types.InlineKeyboardButton('🎲 Игры', callback_data='games')
    )
    
    if str(user_id) in is_admin and is_admin[str(user_id)]:
        markup.add(types.InlineKeyboardButton('👑 Админ-панель', callback_data='admin_panel'))
    
    return markup

def unverified_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('🔑 Верификация', callback_data='verify'))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or message.from_user.first_name or 'Unknown'
    
    if user_id not in users:
        users[user_id] = {
            'username': username,
            'first_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        save_json(USERS_FILE, users)
    
    logs['attempts'].append({
        'user_id': user_id,
        'username': username,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    save_json(LOG_FILE, logs)
    
    if user_id in verified_users and verified_users[user_id]:
        bot.send_message(
            message.chat.id,
            f"❤️ С возвращением, {username}! ❤️",
            reply_markup=main_menu(user_id)
        )
    else:
        bot.send_message(
            message.chat.id,
            f"❤️ Привет, {username}! ❤️\n\n🔑 Пройди верификацию:",
            reply_markup=unverified_menu()
        )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = str(call.from_user.id)
    username = call.from_user.username or call.from_user.first_name or 'Unknown'
    
    logs['clicks'].append({
        'user_id': user_id,
        'username': username,
        'action': call.data,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    save_json(LOG_FILE, logs)
    
    if call.data == 'verify':
        bot.send_message(call.message.chat.id, "🔑 Введите пароль:")
        bot.register_next_step_handler(call.message, check_password)
        bot.answer_callback_query(call.id)
        return
    
    if user_id not in verified_users or not verified_users[user_id]:
        bot.send_message(call.message.chat.id, "❌ Пройдите верификацию!")
        bot.answer_callback_query(call.id)
        return
    
    if call.data == 'random':
        msg = random.choice(data['romantic_messages'])
        bot.send_message(call.message.chat.id, f"{msg}")
        bot.answer_callback_query(call.id)
    
    elif call.data == 'photos':
        show_photos_menu(call.message, user_id)
        bot.answer_callback_query(call.id)
    
    elif call.data.startswith('photo_'):
        photo_index = int(call.data.split('_')[1])
        if 0 <= photo_index < len(data['photos']):
            photo_path = data['photos'][photo_index]
            with open(photo_path, 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo)
        else:
            bot.send_message(call.message.chat.id, "❌ Фото не найдено!")
        bot.answer_callback_query(call.id)
    
    elif call.data == 'our_date':
        show_our_date(call.message)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'question_day':
        show_question_day(call.message)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'playlist':
        show_playlist(call.message)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'movies':
        show_movies(call.message)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'diary':
        show_diary(call.message)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'events':
        show_events(call.message)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'goals':
        show_goals(call.message)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'games':
        show_games_menu(call.message)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'game_truth':
        show_truth_game(call.message)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'game_dare':
        show_dare_game(call.message)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'game_questions':
        show_questions_game(call.message)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'game_compliment':
        show_compliment_game(call.message)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'add_song':
        bot.send_message(call.message.chat.id, "🎵 Введите название песни и исполнителя:")
        bot.register_next_step_handler(call.message, process_add_song)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'add_movie':
        bot.send_message(call.message.chat.id, "🎬 Введите название фильма:")
        bot.register_next_step_handler(call.message, process_add_movie)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'random_movie':
        if not movies:
            bot.send_message(call.message.chat.id, "❌ Нет фильмов!")
        else:
            movie = random.choice(movies)
            bot.send_message(call.message.chat.id, f"🎲 СЛУЧАЙНЫЙ ФИЛЬМ:\n\n{movie}")
        bot.answer_callback_query(call.id)
    
    elif call.data == 'add_diary':
        bot.send_message(call.message.chat.id, "📝 Напиши свои чувства:\n\nВыбери настроение:\n1 - 😊 Счастлив\n2 - ❤️ Влюблен\n3 - 😢 Грустно\n4 - 😍 Очень счастлив\n5 - 🥰 Нежность\n6 - 💕 Романтика")
        bot.register_next_step_handler(call.message, process_add_diary)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'add_event':
        bot.send_message(call.message.chat.id, "📅 Введите дату (ДД.ММ.ГГГГ):")
        bot.register_next_step_handler(call.message, process_add_event_date)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'add_goal':
        bot.send_message(call.message.chat.id, "🌅 Введите цель:")
        bot.register_next_step_handler(call.message, process_add_goal)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'done_goal':
        if not goals:
            bot.send_message(call.message.chat.id, "❌ Нет целей!")
            bot.answer_callback_query(call.id)
            return
        
        text = "✅ Выберите выполненную цель (введите номер):\n\n"
        for i, goal in enumerate(goals, 1):
            status = "✅" if goal['done'] else "⬜"
            text += f"{i}. {status} {goal['text']}\n"
        
        bot.send_message(call.message.chat.id, text)
        bot.register_next_step_handler(call.message, process_done_goal)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'admin_panel':
        if user_id in is_admin and is_admin[user_id]:
            show_admin_panel(call.message)
        else:
            bot.send_message(call.message.chat.id, "❌ Доступ запрещен!")
        bot.answer_callback_query(call.id)
    
    elif call.data == 'admin_stats':
        if user_id in is_admin and is_admin[user_id]:
            show_stats(call.message)
        else:
            bot.send_message(call.message.chat.id, "❌ Доступ запрещен!")
        bot.answer_callback_query(call.id)
    
    elif call.data == 'admin_logs':
        if user_id in is_admin and is_admin[user_id]:
            show_logs(call.message)
        else:
            bot.send_message(call.message.chat.id, "❌ Доступ запрещен!")
        bot.answer_callback_query(call.id)
    
    elif call.data == 'admin_upload':
        if user_id in is_admin and is_admin[user_id]:
            bot.send_message(call.message.chat.id, "📤 Отправьте фото:")
            bot.register_next_step_handler(call.message, save_photo)
        else:
            bot.send_message(call.message.chat.id, "❌ Доступ запрещен!")
        bot.answer_callback_query(call.id)
    
    elif call.data == 'admin_delete_photos':
        if user_id in is_admin and is_admin[user_id]:
            for photo in data['photos']:
                if os.path.exists(photo):
                    os.remove(photo)
            data['photos'] = []
            save_json(DATA_FILE, data)
            bot.send_message(call.message.chat.id, "✅ Все фото удалены!")
        else:
            bot.send_message(call.message.chat.id, "❌ Доступ запрещен!")
        bot.answer_callback_query(call.id)
    
    elif call.data == 'admin_add_message':
        if user_id in is_admin and is_admin[user_id]:
            bot.send_message(call.message.chat.id, "✍️ Введите новое романтическое сообщение:")
            bot.register_next_step_handler(call.message, save_message)
        else:
            bot.send_message(call.message.chat.id, "❌ Доступ запрещен!")
        bot.answer_callback_query(call.id)
    
    elif call.data == 'admin_send_message':
        if user_id in is_admin and is_admin[user_id]:
            show_user_list_for_message(call.message)
        else:
            bot.send_message(call.message.chat.id, "❌ Доступ запрещен!")
        bot.answer_callback_query(call.id)
    
    elif call.data.startswith('send_to_'):
        if user_id in is_admin and is_admin[user_id]:
            target_user_id = call.data.replace('send_to_', '')
            admin_temp[user_id] = {'target_user': target_user_id}
            bot.send_message(
                call.message.chat.id,
                "✍️ Введите сообщение для пользователя:\n\nОтмена: /cancel"
            )
            bot.register_next_step_handler(call.message, send_message_to_user)
        else:
            bot.send_message(call.message.chat.id, "❌ Доступ запрещен!")
        bot.answer_callback_query(call.id)
    
    elif call.data == 'back_to_menu':
        bot.send_message(
            call.message.chat.id,
            "❤️ Главное меню:",
            reply_markup=main_menu(user_id)
        )
        bot.answer_callback_query(call.id)
    
    elif call.data == 'back_to_admin':
        bot.send_message(
            call.message.chat.id,
            "👑 Админ-панель:",
            reply_markup=get_admin_menu()
        )
        bot.answer_callback_query(call.id)
    
    elif call.data == 'no_photos':
        bot.answer_callback_query(call.id, "Фото пока нет!")

def check_password(message):
    user_id = str(message.from_user.id)
    password = message.text
    username = message.from_user.username or message.from_user.first_name or 'Unknown'
    
    if password == USER_PASSWORD:
        verified_users[user_id] = True
        is_admin[user_id] = False
        logs['successful'].append({
            'user_id': user_id,
            'username': username,
            'role': 'user',
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        save_json(LOG_FILE, logs)
        bot.send_message(
            message.chat.id,
            "✅ Верификация пройдена! 🌟",
            reply_markup=main_menu(user_id)
        )
    elif password == ADMIN_PASSWORD:
        verified_users[user_id] = True
        is_admin[user_id] = True
        logs['successful'].append({
            'user_id': user_id,
            'username': username,
            'role': 'admin',
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        save_json(LOG_FILE, logs)
        bot.send_message(
            message.chat.id,
            "👑 Ты вошел как АДМИНИСТРАТОР! 👑",
            reply_markup=main_menu(user_id)
        )
    else:
        bot.send_message(message.chat.id, "❌ Неверный пароль!")
        bot.send_message(message.chat.id, "🔑 Введите пароль:")
        bot.register_next_step_handler(message, check_password)

def show_our_date(message):
    now = datetime.now()
    diff = now - START_DATE
    
    years = diff.days // 365
    months = (diff.days % 365) // 30
    days = (diff.days % 365) % 30
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60
    seconds = diff.seconds % 60
    
    text = f"""❤️ МЫ ВМЕСТЕ УЖЕ ❤️

📅 {years} лет, {months} месяцев, {days} дней
⏰ {hours} часов, {minutes} минут, {seconds} секунд

💗 С 01.05.2026
💖 Каждая секунда с тобой - бесценна!
💕 Ты моя вечная любовь!"""
    
    bot.send_message(
        message.chat.id,
        text,
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu')
        )
    )

def show_question_day(message):
    day = datetime.now().day
    question = daily_questions[day % len(daily_questions)]
    
    text = f"""❓ ВОПРОС ДНЯ ❓

{question}

💕 Ответь честно, это важно для меня! 💕"""
    
    bot.send_message(
        message.chat.id,
        text,
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu')
        )
    )

def show_playlist(message):
    text = "🎵 НАШ ПЛЕЙЛИСТ 🎵\n\n"
    if not playlist:
        text += "📭 Пока нет песен\n\n➕ Добавь свою любимую песню!"
    else:
        for i, song in enumerate(playlist, 1):
            text += f"{i}. {song}\n"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton('➕ Добавить песню', callback_data='add_song'),
        types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu')
    )
    
    bot.send_message(message.chat.id, text, reply_markup=markup)

def show_movies(message):
    text = "🎬 ФИЛЬМЫ ДЛЯ ПРОСМОТРА 🎬\n\n"
    if not movies:
        text += "📭 Пока нет фильмов\n\n➕ Добавь фильм который хотим посмотреть!"
    else:
        for i, movie in enumerate(movies, 1):
            text += f"{i}. {movie}\n"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton('➕ Добавить фильм', callback_data='add_movie'),
        types.InlineKeyboardButton('🎲 Случайный фильм', callback_data='random_movie'),
        types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu')
    )
    
    bot.send_message(message.chat.id, text, reply_markup=markup)

def show_diary(message):
    text = "📝 НАШ ДНЕВНИК 📝\n\n"
    if not diary:
        text += "📭 Записей пока нет\n\n➕ Добавь запись о своих чувствах!"
    else:
        recent = diary[-5:]
        for entry in reversed(recent):
            text += f"📅 {entry['date']}\n"
            text += f"❤️ {entry['text']}\n"
            text += f"😊 Настроение: {entry['mood']}\n\n"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton('➕ Добавить запись', callback_data='add_diary'),
        types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu')
    )
    
    bot.send_message(message.chat.id, text, reply_markup=markup)

def show_events(message):
    text = "🗓️ ВАЖНЫЕ ДАТЫ 🗓️\n\n"
    for event in events:
        text += f"📅 {event['date']}\n"
        text += f"❤️ {event['name']}\n\n"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton('➕ Добавить событие', callback_data='add_event'),
        types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu')
    )
    
    bot.send_message(message.chat.id, text, reply_markup=markup)

def show_goals(message):
    text = "🌅 НАШИ ЦЕЛИ 🌅\n\n"
    if not goals:
        text += "📭 Целей пока нет\n\n➕ Добавьте общую цель!"
    else:
        for i, goal in enumerate(goals, 1):
            status = "✅" if goal['done'] else "⬜"
            text += f"{status} {i}. {goal['text']}\n"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton('➕ Добавить цель', callback_data='add_goal'),
        types.InlineKeyboardButton('✅ Отметить выполненную', callback_data='done_goal'),
        types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu')
    )
    
    bot.send_message(message.chat.id, text, reply_markup=markup)

def show_games_menu(message):
    text = """🎲 ИГРЫ ДЛЯ ДВОИХ 🎲

Выбери игру:

💕 Правда - честные ответы
💋 Действие - романтические задания
❓ 20 вопросов о любви
🌸 Комплимент дня"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('💕 Правда', callback_data='game_truth'),
        types.InlineKeyboardButton('💋 Действие', callback_data='game_dare'),
        types.InlineKeyboardButton('❓ 20 вопросов', callback_data='game_questions'),
        types.InlineKeyboardButton('🌸 Комплимент', callback_data='game_compliment'),
        types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu')
    )
    
    bot.send_message(message.chat.id, text, reply_markup=markup)

def show_truth_game(message):
    question = random.choice(truth_questions)
    text = f"""💕 ПРАВДА 💕

{question}

Ответь честно! ❤️"""
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton('🔀 Следующий вопрос', callback_data='game_truth'),
        types.InlineKeyboardButton('🔙 Назад в игры', callback_data='games')
    )
    
    bot.send_message(message.chat.id, text, reply_markup=markup)

def show_dare_game(message):
    action = random.choice(dare_actions)
    text = f"""💋 ДЕЙСТВИЕ 💋

{action}

Выполни! 😉"""
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton('🔀 Следующее действие', callback_data='game_dare'),
        types.InlineKeyboardButton('🔙 Назад в игры', callback_data='games')
    )
    
    bot.send_message(message.chat.id, text, reply_markup=markup)

def show_questions_game(message):
    questions = [
        '❓ Какое твое любимое место для свиданий?',
        '❓ Что ты чувствуешь, когда я рядом?',
        '❓ Какой твой любимый фильм о любви?',
        '❓ Что ты хочешь изменить в наших отношениях?',
        '❓ Какой твой самый счастливый момент с тобой?',
        '❓ Что ты больше всего ценишь во мне?',
        '❓ Какую песню ты посвящаешь мне?',
        '❓ Куда ты хочешь поехать со мной?',
        '❓ Что тебя делает счастливой?',
        '❓ Какой комплимент тебе приятнее всего?',
        '❓ Что ты хочешь пожелать мне сегодня?',
        '❓ Какая твоя самая заветная мечта?',
        '❓ Что я делаю лучше всего?',
        '❓ Когда ты понял(а) что любишь меня?',
        '❓ Что ты хочешь сказать мне прямо сейчас?',
        '❓ Какое твое любимое время суток со мной?',
        '❓ Что тебя бесит в наших отношениях?',
        '❓ Что делает наши отношения особенными?',
        '❓ О чем ты мечтаешь в отношениях?',
        '❓ Что ты хочешь сделать для меня сегодня?'
    ]
    
    question = random.choice(questions)
    text = f"""❓ ВОПРОС О ЛЮБВИ ❓

{question}

💕 Ответь честно! 💕"""
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton('🔀 Другой вопрос', callback_data='game_questions'),
        types.InlineKeyboardButton('🔙 Назад в игры', callback_data='games')
    )
    
    bot.send_message(message.chat.id, text, reply_markup=markup)

def show_compliment_game(message):
    compliments = [
        '🌸 Ты самая красивая!',
        '💕 Ты моя любовь навечно!',
        '💋 Твои глаза сводят меня с ума!',
        '🌹 Ты моя мечта и реальность!',
        '💗 Ты делаешь меня счастливым!',
        '🌟 Ты сияешь ярче солнца!',
        '💖 Ты моя муза и вдохновение!',
        '🌸 Ты как цветок в моем сердце!',
        '💕 С тобой я на вершине мира!',
        '💋 Твоя улыбка - мое счастье!',
        '🌹 Ты моя принцесса!',
        '💗 Я люблю тебя больше жизни!',
        '🌟 Ты моя вечная любовь!',
        '💖 Ты самая невероятная!'
    ]
    
    compliment = random.choice(compliments)
    text = f"""🌸 КОМПЛИМЕНТ ДНЯ 🌸

{compliment}

💕 Ты самая лучшая! 💕"""
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton('🔀 Еще комплимент', callback_data='game_compliment'),
        types.InlineKeyboardButton('🔙 Назад в игры', callback_data='games')
    )
    
    bot.send_message(message.chat.id, text, reply_markup=markup)

def show_photos_menu(message, user_id):
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = []
    for i in range(len(data['photos'])):
        buttons.append(types.InlineKeyboardButton(str(i+1), callback_data=f'photo_{i}'))
    
    if buttons:
        for i in range(0, len(buttons), 3):
            markup.add(*buttons[i:i+3])
    else:
        markup.add(types.InlineKeyboardButton('📭 Нет фото', callback_data='no_photos'))
    
    if user_id in is_admin and is_admin[user_id]:
        markup.add(types.InlineKeyboardButton('📤 Загрузить фото', callback_data='admin_upload'))
    
    markup.add(types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu'))
    
    bot.send_message(
        message.chat.id,
        f"📸 Наши фото ({len(data['photos'])} шт.):",
        reply_markup=markup
    )

def show_admin_panel(message):
    bot.send_message(
        message.chat.id,
        "👑 Админ-панель",
        reply_markup=get_admin_menu()
    )

def show_stats(message):
    stats = f"📊 СТАТИСТИКА:\n\n"
    stats += f"👥 Пользователей: {len(users)}\n"
    stats += f"✅ Входов: {len(logs['successful'])}\n"
    stats += f"🖱 Нажатий: {len(logs['clicks'])}\n"
    stats += f"📸 Фото: {len(data['photos'])}\n"
    stats += f"💬 Сообщений: {len(data['romantic_messages'])}\n"
    stats += f"🎵 Плейлист: {len(playlist)}\n"
    stats += f"🎬 Фильмов: {len(movies)}\n"
    stats += f"📝 Записей: {len(diary)}\n"
    stats += f"🌅 Целей: {len(goals)}\n"
    stats += f"🗓️ Событий: {len(events)}"
    
    bot.send_message(message.chat.id, stats)

def show_logs(message):
    if not logs['clicks']:
        bot.send_message(message.chat.id, "📝 Логов нет.")
        return
    
    recent_logs = logs['clicks'][-15:]
    text = "📝 ПОСЛЕДНИЕ 15 ДЕЙСТВИЙ:\n\n"
    for log in recent_logs:
        text += f"👤 {log.get('username', 'Unknown')}\n"
        text += f"   ⚡ {log.get('action', 'Unknown')}\n"
        text += f"   🕐 {log.get('time', 'Unknown')}\n\n"
    
    bot.send_message(message.chat.id, text[:4000])

def show_user_list_for_message(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    if not users:
        markup.add(types.InlineKeyboardButton('❌ Нет пользователей', callback_data='no_users'))
    else:
        for user_id, user_data in list(users.items())[-20:]:
            username = user_data.get('username', 'Unknown')
            markup.add(types.InlineKeyboardButton(
                f"👤 {username}", callback_data=f'send_to_{user_id}'
            ))
    
    markup.add(types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_admin'))
    
    bot.send_message(
        message.chat.id,
        "💬 Выберите пользователя:",
        reply_markup=markup
    )

def send_message_to_user(message):
    user_id = str(message.from_user.id)
    
    if message.text == '/cancel':
        bot.send_message(message.chat.id, "❌ Отменено.")
        show_admin_panel(message)
        return
    
    target_user_id = admin_temp.get(user_id, {}).get('target_user')
    if not target_user_id:
        bot.send_message(message.chat.id, "❌ Ошибка!")
        show_admin_panel(message)
        return
    
    try:
        bot.send_message(target_user_id, f"📨 Сообщение:\n\n{message.text}")
        bot.send_message(message.chat.id, "✅ Отправлено!")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {str(e)}")
    
    admin_temp.pop(user_id, None)
    show_admin_panel(message)

def save_photo(message):
    user_id = str(message.from_user.id)
    if user_id in is_admin and is_admin[user_id]:
        if message.photo:
            file_info = bot.get_file(message.photo[-1].file_id)
            file_path = os.path.join(PHOTOS_DIR, f'photo_{len(data["photos"])+1}.jpg')
            downloaded_file = bot.download_file(file_info.file_path)
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            data['photos'].append(file_path)
            save_json(DATA_FILE, data)
            bot.send_message(message.chat.id, f"✅ Сохранено! Всего: {len(data['photos'])}")
        else:
            bot.send_message(message.chat.id, "❌ Отправьте фото!")

def save_message(message):
    user_id = str(message.from_user.id)
    if user_id in is_admin and is_admin[user_id]:
        data['romantic_messages'].append(message.text)
        save_json(DATA_FILE, data)
        bot.send_message(message.chat.id, f"✅ Добавлено! Всего: {len(data['romantic_messages'])}")

def process_add_song(message):
    playlist.append(message.text)
    save_json(PLAYLIST_FILE, playlist)
    bot.send_message(message.chat.id, f"✅ Песня добавлена! Всего: {len(playlist)}")
    show_playlist(message)

def process_add_movie(message):
    movies.append(message.text)
    save_json(MOVIES_FILE, movies)
    bot.send_message(message.chat.id, f"✅ Фильм добавлен! Всего: {len(movies)}")
    show_movies(message)

def process_add_diary(message):
    mood_map = {
        '1': '😊 Счастлив',
        '2': '❤️ Влюблен',
        '3': '😢 Грустно',
        '4': '😍 Очень счастлив',
        '5': '🥰 Нежность',
        '6': '💕 Романтика'
    }
    
    mood = mood_map.get(message.text, '❤️ Влюблен')
    
    if message.text not in mood_map:
        diary.append({
            'date': datetime.now().strftime('%d.%m.%Y %H:%M'),
            'text': message.text,
            'mood': mood
        })
        save_json(DIARY_FILE, diary)
        bot.send_message(message.chat.id, "✅ Запись добавлена!")
        show_diary(message)
    else:
        bot.send_message(message.chat.id, "✍️ Теперь напиши свои чувства:")
        bot.register_next_step_handler(message, process_diary_text, mood)

def process_diary_text(message, mood):
    diary.append({
        'date': datetime.now().strftime('%d.%m.%Y %H:%M'),
        'text': message.text,
        'mood': mood
    })
    save_json(DIARY_FILE, diary)
    bot.send_message(message.chat.id, "✅ Запись добавлена!")
    show_diary(message)

def process_add_event_date(message):
    date = message.text
    bot.send_message(message.chat.id, "❤️ Введите название события:")
    bot.register_next_step_handler(message, process_add_event_name, date)

def process_add_event_name(message, date):
    events.append({'date': date, 'name': message.text})
    save_json(EVENTS_FILE, events)
    bot.send_message(message.chat.id, "✅ Событие добавлено!")
    show_events(message)

def process_add_goal(message):
    goals.append({'text': message.text, 'done': False})
    save_json(GOALS_FILE, goals)
    bot.send_message(message.chat.id, "✅ Цель добавлена!")
    show_goals(message)

def process_done_goal(message):
    try:
        num = int(message.text) - 1
        if 0 <= num < len(goals):
            goals[num]['done'] = True
            save_json(GOALS_FILE, goals)
            bot.send_message(message.chat.id, "✅ Цель отмечена как выполненная!")
        else:
            bot.send_message(message.chat.id, "❌ Неверный номер!")
    except:
        bot.send_message(message.chat.id, "❌ Введите номер!")
    
    show_goals(message)

@bot.message_handler(commands=['cancel'])
def cancel_command(message):
    user_id = str(message.from_user.id)
    if user_id in is_admin and is_admin[user_id]:
        admin_temp.pop(user_id, None)
        bot.send_message(message.chat.id, "❌ Отменено.")
        show_admin_panel(message)

if __name__ == '__main__':
    print("❤️ LOVE BOT ЗАПУЩЕН! ❤️")
    print(f"🔑 Пароль для пользователей: {USER_PASSWORD}")
    print(f"👑 Пароль для админа: {ADMIN_PASSWORD}")
    print("🔥 БОТ РАБОТАЕТ 24/7!")
    bot.polling(none_stop=True)
