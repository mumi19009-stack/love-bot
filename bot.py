# -*- coding: utf-8 -*-
import telebot
from telebot import types
import random
import json
import os
from datetime import datetime, timedelta

TOKEN = '8772865540:AAHlIKEaIauGSHn3ttTt4VH4xWb8KU_Miqc'
bot = telebot.TeleBot(TOKEN)

try:
    bot.remove_webhook()
except:
    pass

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
ANSWERS_FILE = 'answers.json'  # Ответы на вопросы дня

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

logs = load_json(LOG_FILE, {'attempts': [], 'successful': [], 'clicks': [], 'answers': []})
users = load_json(USERS_FILE, {})
diary = load_json(DIARY_FILE, [])
playlist = load_json(PLAYLIST_FILE, [])
movies = load_json(MOVIES_FILE, [])
goals = load_json(GOALS_FILE, [])
events = load_json(EVENTS_FILE, [{'name': 'Начало отношений ❤️', 'date': '01.05.2026'}])
answers = load_json(ANSWERS_FILE, [])

verified_users = {}
is_admin = {}
user_balance = {}  # Баланс пользователей
admin_temp = {}

# Загружаем пользователей и балансы
def load_saved_data():
    for user_id, user_data in users.items():
        if user_data.get('verified', False):
            verified_users[user_id] = True
        if user_data.get('is_admin', False):
            is_admin[user_id] = True
        user_balance[user_id] = user_data.get('balance', 0)

load_saved_data()

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
    '💝 Что ты хочешь пожелать мне сегодня?',
    '🌺 Что делает тебя счастливой в наших отношениях?',
    '💞 Какой комплимент ты хочешь услышать от меня?',
    '🌟 Что ты ценишь во мне больше всего?',
    '💗 Какое твое любимое время с тобой?',
    '❤️ Что ты хочешь сделать вместе сегодня?'
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

# ========== МЕНЮ ==========

def get_admin_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('📊 Статистика', callback_data='admin_stats'),
        types.InlineKeyboardButton('📝 Логи', callback_data='admin_logs'),
        types.InlineKeyboardButton('📤 Загрузить фото', callback_data='admin_upload'),
        types.InlineKeyboardButton('❌ Удалить все фото', callback_data='admin_delete_photos'),
        types.InlineKeyboardButton('➕ Добавить слово', callback_data='admin_add_word'),
        types.InlineKeyboardButton('📢 Рассылка', callback_data='admin_mailing'),
        types.InlineKeyboardButton('💎 Выдать баллы', callback_data='admin_give_balance'),
        types.InlineKeyboardButton('👥 Управление пользователями', callback_data='admin_users'),
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
        types.InlineKeyboardButton('🎲 Игры', callback_data='games'),
        types.InlineKeyboardButton('💎 Мой баланс', callback_data='my_balance')
    )
    
    if str(user_id) in is_admin and is_admin[str(user_id)]:
        markup.add(types.InlineKeyboardButton('👑 Админ-панель', callback_data='admin_panel'))
    
    return markup

def unverified_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('🔑 Верификация', callback_data='verify'))
    return markup

# ========== ОСНОВНЫЕ ФУНКЦИИ ==========

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or message.from_user.first_name or 'Unknown'
    
    if user_id not in users:
        users[user_id] = {
            'username': username,
            'first_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'verified': False,
            'is_admin': False,
            'balance': 0,
            'banned': False
        }
        save_json(USERS_FILE, users)
    
    # Проверка бана
    if users[user_id].get('banned', False):
        bot.send_message(message.chat.id, "❌ Вы забанены!")
        return
    
    logs['attempts'].append({
        'user_id': user_id,
        'username': username,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    save_json(LOG_FILE, logs)
    
    if user_id in verified_users and verified_users[user_id]:
        bot.send_message(
            message.chat.id,
            f"❤️ С возвращением, {username}! ❤️\n\n💎 Баланс: {user_balance.get(user_id, 0)} баллов",
            reply_markup=main_menu(user_id)
        )
    else:
        bot.send_message(
            message.chat.id,
            f"❤️ Привет, {username}! ❤️\n\n🔑 Пройди верификацию один раз, и я запомню тебя!",
            reply_markup=unverified_menu()
        )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = str(call.from_user.id)
    username = call.from_user.username or call.from_user.first_name or 'Unknown'
    
    # Проверка бана
    if user_id in users and users[user_id].get('banned', False):
        bot.send_message(call.message.chat.id, "❌ Вы забанены!")
        bot.answer_callback_query(call.id)
        return
    
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
    
    # ===== ГЛАВНОЕ МЕНЮ =====
    if call.data == 'random':
        msg = random.choice(data['romantic_messages'])
        bot.send_message(call.message.chat.id, f"💗 {msg}")
        # +1 балл за использование
        user_balance[user_id] = user_balance.get(user_id, 0) + 1
        users[user_id]['balance'] = user_balance[user_id]
        save_json(USERS_FILE, users)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'my_balance':
        balance = user_balance.get(user_id, 0)
        bot.send_message(call.message.chat.id, f"💎 Твой баланс: {balance} баллов\n\n✨ За каждое нажатие 'Любовь' +1 балл!")
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
        show_question_day(call.message, user_id)
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
    
    # ===== ИГРЫ =====
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
    
    # ===== ДОБАВЛЕНИЕ =====
    elif call.data == 'add_song':
        bot.send_message(call.message.chat.id, "🎵 Введите название песни и исполнителя:")
        bot.register_next_step_handler(call.message, process_add_song)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'add_movie':
        bot.send_message(call.message.chat.id, "🎬 Введите название фильма:")
        bot.register_next_step_handler(call.message, process_add_movie)
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
    
    # ===== ОТВЕТ НА ВОПРОС =====
    elif call.data == 'answer_question':
        bot.send_message(call.message.chat.id, "✍️ Напиши свой ответ:")
        bot.register_next_step_handler(call.message, process_answer_question)
        bot.answer_callback_query(call.id)
    
    elif call.data == 'view_answers':
        show_answers(call.message)
        bot.answer_callback_query(call.id)
    
    # ===== АДМИНКА =====
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
    
    # ===== ДОБАВЛЕНИЕ СЛОВА В RANDOM =====
    elif call.data == 'admin_add_word':
        if user_id in is_admin and is_admin[user_id]:
            bot.send_message(call.message.chat.id, "✍️ Введите новое романтическое сообщение для Random:")
            bot.register_next_step_handler(call.message, process_add_word)
        else:
            bot.send_message(call.message.chat.id, "❌ Доступ запрещен!")
        bot.answer_callback_query(call.id)
    
    # ===== РАССЫЛКА =====
    elif call.data == 'admin_mailing':
        if user_id in is_admin and is_admin[user_id]:
            bot.send_message(call.message.chat.id, "📢 Введите сообщение для РАССЫЛКИ всем пользователям:")
            bot.register_next_step_handler(call.message, process_mailing)
        else:
            bot.send_message(call.message.chat.id, "❌ Доступ запрещен!")
        bot.answer_callback_query(call.id)
    
    # ===== ВЫДАЧА БАЛЛОВ =====
    elif call.data == 'admin_give_balance':
        if user_id in is_admin and is_admin[user_id]:
            bot.send_message(call.message.chat.id, "💎 Введите ID пользователя и количество баллов через пробел (например: 123456789 10):")
            bot.register_next_step_handler(call.message, process_give_balance)
        else:
            bot.send_message(call.message.chat.id, "❌ Доступ запрещен!")
        bot.answer_callback_query(call.id)
    
    # ===== УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ =====
    elif call.data == 'admin_users':
        if user_id in is_admin and is_admin[user_id]:
            show_user_management(call.message)
        else:
            bot.send_message(call.message.chat.id, "❌ Доступ запрещен!")
        bot.answer_callback_query(call.id)
    
    elif call.data.startswith('ban_user_'):
        if user_id in is_admin and is_admin[user_id]:
            target_id = call.data.replace('ban_user_', '')
            if target_id in users:
                users[target_id]['banned'] = True
                save_json(USERS_FILE, users)
                bot.send_message(call.message.chat.id, f"✅ Пользователь {target_id} ЗАБАНЕН!")
                if target_id in verified_users:
                    verified_users.pop(target_id, None)
                show_user_management(call.message)
            else:
                bot.send_message(call.message.chat.id, "❌ Пользователь не найден!")
        else:
            bot.send_message(call.message.chat.id, "❌ Доступ запрещен!")
        bot.answer_callback_query(call.id)
    
    elif call.data.startswith('unban_user_'):
        if user_id in is_admin and is_admin[user_id]:
            target_id = call.data.replace('unban_user_', '')
            if target_id in users:
                users[target_id]['banned'] = False
                save_json(USERS_FILE, users)
                bot.send_message(call.message.chat.id, f"✅ Пользователь {target_id} РАЗБАНЕН!")
                show_user_management(call.message)
            else:
                bot.send_message(call.message.chat.id, "❌ Пользователь не найден!")
        else:
            bot.send_message(call.message.chat.id, "❌ Доступ запрещен!")
        bot.answer_callback_query(call.id)
    
    elif call.data.startswith('make_admin_'):
        if user_id in is_admin and is_admin[user_id]:
            target_id = call.data.replace('make_admin_', '')
            if target_id in users:
                users[target_id]['is_admin'] = True
                is_admin[target_id] = True
                save_json(USERS_FILE, users)
                bot.send_message(call.message.chat.id, f"✅ Пользователь {target_id} стал АДМИНОМ!")
                show_user_management(call.message)
            else:
                bot.send_message(call.message.chat.id, "❌ Пользователь не найден!")
        else:
            bot.send_message(call.message.chat.id, "❌ Доступ запрещен!")
        bot.answer_callback_query(call.id)
    
    elif call.data.startswith('remove_admin_'):
        if user_id in is_admin and is_admin[user_id]:
            target_id = call.data.replace('remove_admin_', '')
            if target_id in users:
                users[target_id]['is_admin'] = False
                is_admin.pop(target_id, None)
                save_json(USERS_FILE, users)
                bot.send_message(call.message.chat.id, f"✅ У пользователя {target_id} сняты права админа!")
                show_user_management(call.message)
            else:
                bot.send_message(call.message.chat.id, "❌ Пользователь не найден!")
        else:
            bot.send_message(call.message.chat.id, "❌ Доступ запрещен!")
        bot.answer_callback_query(call.id)
    
    # ===== НАЗАД =====
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

# ========== ПРОВЕРКА ПАРОЛЯ ==========

def check_password(message):
    user_id = str(message.from_user.id)
    password = message.text
    username = message.from_user.username or message.from_user.first_name or 'Unknown'
    
    if password == USER_PASSWORD:
        verified_users[user_id] = True
        is_admin[user_id] = False
        
        if user_id in users:
            users[user_id]['verified'] = True
            users[user_id]['is_admin'] = False
            save_json(USERS_FILE, users)
        
        logs['successful'].append({
            'user_id': user_id,
            'username': username,
            'role': 'user',
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        save_json(LOG_FILE, logs)
        bot.send_message(
            message.chat.id,
            "✅ Верификация пройдена! Теперь я запомнил тебя навсегда! 🌟\n\n💎 За каждое нажатие 'Любовь' ты получаешь +1 балл!",
            reply_markup=main_menu(user_id)
        )
    elif password == ADMIN_PASSWORD:
        verified_users[user_id] = True
        is_admin[user_id] = True
        
        if user_id in users:
            users[user_id]['verified'] = True
            users[user_id]['is_admin'] = True
            save_json(USERS_FILE, users)
        
        logs['successful'].append({
            'user_id': user_id,
            'username': username,
            'role': 'admin',
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        save_json(LOG_FILE, logs)
        bot.send_message(
            message.chat.id,
            "👑 Ты вошел как АДМИНИСТРАТОР! Теперь я запомнил тебя! 👑\n\n"
            "📊 Тебе доступны:\n"
            "- Рассылка пользователям\n"
            "- Выдача баллов\n"
            "- Управление пользователями\n"
            "- Добавление слов в Random\n"
            "- Просмотр всех логов\n"
            "- Ответы на вопросы дня",
            reply_markup=main_menu(user_id)
        )
    else:
        bot.send_message(message.chat.id, "❌ Неверный пароль! Попробуйте снова.")
        bot.send_message(message.chat.id, "🔑 Введите пароль:")
        bot.register_next_step_handler(message, check_password)

# ========== ВСЕ ФУНКЦИИ ПОКАЗА ==========

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

def show_question_day(message, user_id):
    day = datetime.now().day
    question = daily_questions[day % len(daily_questions)]
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('✍️ Ответить', callback_data='answer_question'),
        types.InlineKeyboardButton('👀 Посмотреть ответы', callback_data='view_answers'),
        types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_menu')
    )
    
    text = f"""❓ ВОПРОС ДНЯ ❓

{question}

💕 Ответь честно, это важно для меня! 💕
📝 Твои ответы увидят все!"""
    
    bot.send_message(message.chat.id, text, reply_markup=markup)

def show_answers(message):
    if not answers:
        bot.send_message(message.chat.id, "📭 Ответов пока нет!")
        return
    
    text = "📝 ОТВЕТЫ НА ВОПРОСЫ ДНЯ 📝\n\n"
    for answer in answers[-10:]:  # Последние 10
        text += f"👤 {answer['username']}\n"
        text += f"❓ {answer['question']}\n"
        text += f"💬 {answer['answer']}\n"
        text += f"🕐 {answer['time']}\n\n"
    
    if len(text) > 4000:
        text = text[:4000] + "..."
    
    bot.send_message(message.chat.id, text)

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

# ========== АДМИН-ПАНЕЛЬ ==========

def show_admin_panel(message):
    bot.send_message(
        message.chat.id,
        "👑 Админ-панель\n\n"
        "📢 Рассылка - отправить сообщение всем\n"
        "💎 Выдать баллы - начисление баллов\n"
        "👥 Управление - бан/разбан/права\n"
        "➕ Добавить слово - в Random\n"
        "📊 Статистика - полная информация\n"
        "📝 Логи - все действия",
        reply_markup=get_admin_menu()
    )

def show_stats(message):
    stats = f"📊 СТАТИСТИКА:\n\n"
    stats += f"👥 Всего пользователей: {len(users)}\n"
    stats += f"✅ Верифицировано: {len(verified_users)}\n"
    stats += f"👑 Администраторов: {sum(1 for v in is_admin.values() if v)}\n"
    stats += f"🚫 Забанено: {sum(1 for u in users.values() if u.get('banned', False))}\n"
    stats += f"🖱 Всего нажатий: {len(logs['clicks'])}\n"
    stats += f"📸 Фото в базе: {len(data['photos'])}\n"
    stats += f"💬 Слов в Random: {len(data['romantic_messages'])}\n"
    stats += f"🎵 Плейлист: {len(playlist)}\n"
    stats += f"🎬 Фильмов: {len(movies)}\n"
    stats += f"📝 Записей в дневнике: {len(diary)}\n"
    stats += f"🌅 Целей: {len(goals)}\n"
    stats += f"🗓️ Событий: {len(events)}\n"
    stats += f"📝 Ответов на вопросы: {len(answers)}"
    
    bot.send_message(message.chat.id, stats)

def show_logs(message):
    if not logs['clicks']:
        bot.send_message(message.chat.id, "📝 Логов нет.")
        return
    
    # Последние 20 действий
    recent_logs = logs['clicks'][-20:]
    text = "📝 ПОСЛЕДНИЕ 20 ДЕЙСТВИЙ:\n\n"
    for log in recent_logs:
        text += f"👤 {log.get('username', 'Unknown')}\n"
        text += f"   ⚡ {log.get('action', 'Unknown')}\n"
        text += f"   🕐 {log.get('time', 'Unknown')}\n\n"
    
    if len(text) > 4000:
        text = text[:4000] + "..."
    
    # Добавляем информацию о попытках входа
    if logs['attempts']:
        text += "\n👥 ПОСЛЕДНИЕ ПОПЫТКИ ВХОДА:\n"
        for attempt in logs['attempts'][-5:]:
            text += f"👤 {attempt.get('username', 'Unknown')} - {attempt.get('time', '')}\n"
    
    bot.send_message(message.chat.id, text)

def show_user_management(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Показываем последних 10 пользователей
    user_list = list(users.items())[-10:]
    for uid, u_data in user_list:
        username = u_data.get('username', 'Unknown')
        status = ""
        if u_data.get('banned', False):
            status = "🚫"
        elif u_data.get('is_admin', False):
            status = "👑"
        elif u_data.get('verified', False):
            status = "✅"
        
        markup.add(types.InlineKeyboardButton(
            f"{status} {username}", 
            callback_data=f'show_user_{uid}'
        ))
    
    markup.add(types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_admin'))
    
    bot.send_message(
        message.chat.id,
        "👥 Управление пользователями:\n\n"
        "✅ - верифицирован\n"
        "👑 - админ\n"
        "🚫 - забанен\n\n"
        "Выберите пользователя для управления:",
        reply_markup=markup
    )

# Обработчик выбора пользователя
@bot.callback_query_handler(func=lambda call: call.data.startswith('show_user_'))
def show_user_actions(call):
    user_id = str(call.from_user.id)
    if user_id not in is_admin or not is_admin[user_id]:
        bot.send_message(call.message.chat.id, "❌ Доступ запрещен!")
        bot.answer_callback_query(call.id)
        return
    
    target_id = call.data.replace('show_user_', '')
    if target_id not in users:
        bot.send_message(call.message.chat.id, "❌ Пользователь не найден!")
        bot.answer_callback_query(call.id)
        return
    
    u_data = users[target_id]
    username = u_data.get('username', 'Unknown')
    is_banned = u_data.get('banned', False)
    is_admin_user = u_data.get('is_admin', False)
    balance = u_data.get('balance', 0)
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    if is_banned:
        markup.add(types.InlineKeyboardButton('✅ Разбанить', callback_data=f'unban_user_{target_id}'))
    else:
        markup.add(types.InlineKeyboardButton('🚫 Забанить', callback_data=f'ban_user_{target_id}'))
    
    if is_admin_user:
        markup.add(types.InlineKeyboardButton('👑 Снять админа', callback_data=f'remove_admin_{target_id}'))
    else:
        markup.add(types.InlineKeyboardButton('👑 Сделать админом', callback_data=f'make_admin_{target_id}'))
    
    markup.add(types.InlineKeyboardButton('🔙 Назад', callback_data='admin_users'))
    
    text = f"👤 ПОЛЬЗОВАТЕЛЬ:\n\n"
    text += f"ID: {target_id}\n"
    text += f"Имя: {username}\n"
    text += f"Статус: {'🚫 Забанен' if is_banned else '✅ Активен'}\n"
    text += f"Права: {'👑 Админ' if is_admin_user else '👤 Пользователь'}\n"
    text += f"💎 Баланс: {balance} баллов\n"
    text += f"📅 Зарегистрирован: {u_data.get('first_seen', 'Unknown')}\n"
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
    bot.answer_callback_query(call.id)

# ========== ПРОЦЕССЫ ДОБАВЛЕНИЯ ==========

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

# ========== ОТВЕТЫ НА ВОПРОСЫ ==========

def process_answer_question(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or message.from_user.first_name or 'Unknown'
    
    day = datetime.now().day
    question = daily_questions[day % len(daily_questions)]
    
    answers.append({
        'user_id': user_id,
        'username': username,
        'question': question,
        'answer': message.text,
        'time': datetime.now().strftime('%d.%m.%Y %H:%M')
    })
    save_json(ANSWERS_FILE, answers)
    
    logs['answers'].append({
        'user_id': user_id,
        'username': username,
        'question': question,
        'answer': message.text,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    save_json(LOG_FILE, logs)
    
    bot.send_message(message.chat.id, "✅ Твой ответ сохранен! 💕")
    
    # Показываем вопрос снова
    show_question_day(message, user_id)

# ========== АДМИН-ФУНКЦИИ ==========

def process_add_word(message):
    user_id = str(message.from_user.id)
    if user_id not in is_admin or not is_admin[user_id]:
        return
    
    data['romantic_messages'].append(message.text)
    save_json(DATA_FILE, data)
    bot.send_message(message.chat.id, f"✅ Слово добавлено! Всего: {len(data['romantic_messages'])}")

def process_mailing(message):
    user_id = str(message.from_user.id)
    if user_id not in is_admin or not is_admin[user_id]:
        return
    
    text = message.text
    success = 0
    fail = 0
    
    bot.send_message(message.chat.id, "🔄 Начинаю рассылку...")
    
    for uid in users:
        if users[uid].get('banned', False):
            continue
        try:
            bot.send_message(uid, f"📢 РАССЫЛКА ОТ АДМИНА:\n\n{text}")
            success += 1
        except:
            fail += 1
    
    bot.send_message(
        message.chat.id,
        f"✅ Рассылка завершена!\n"
        f"📨 Отправлено: {success}\n"
        f"❌ Не доставлено: {fail}"
    )

def process_give_balance(message):
    user_id = str(message.from_user.id)
    if user_id not in is_admin or not is_admin[user_id]:
        return
    
    try:
        parts = message.text.split()
        target_id = parts[0]
        amount = int(parts[1])
        
        if target_id not in users:
            bot.send_message(message.chat.id, "❌ Пользователь не найден!")
            return
        
        user_balance[target_id] = user_balance.get(target_id, 0) + amount
        users[target_id]['balance'] = user_balance[target_id]
        save_json(USERS_FILE, users)
        
        bot.send_message(
            message.chat.id,
            f"✅ Пользователю {target_id} начислено {amount} баллов!\n"
            f"💎 Текущий баланс: {user_balance[target_id]}"
        )
        
        try:
            bot.send_message(
                target_id,
                f"💎 Тебе начислено {amount} баллов!\n"
                f"✨ Твой баланс: {user_balance[target_id]}"
            )
        except:
            pass
    
    except:
        bot.send_message(message.chat.id, "❌ Ошибка! Введите: ID_пользователя Количество (например: 123456789 10)")

# ========== СОХРАНЕНИЕ ФОТО ==========

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

# ========== ОБРАБОТЧИК RANDOM MOVIE ==========

@bot.callback_query_handler(func=lambda call: call.data == 'random_movie')
def random_movie(call):
    if not movies:
        bot.send_message(call.message.chat.id, "❌ Нет фильмов!")
        return
    movie = random.choice(movies)
    bot.send_message(call.message.chat.id, f"🎲 СЛУЧАЙНЫЙ ФИЛЬМ:\n\n{movie}")
    bot.answer_callback_query(call.id)

# ========== ОТМЕНА ==========

@bot.message_handler(commands=['cancel'])
def cancel_command(message):
    user_id = str(message.from_user.id)
    if user_id in is_admin and is_admin[user_id]:
        admin_temp.pop(user_id, None)
        bot.send_message(message.chat.id, "❌ Отменено.")
        show_admin_panel(message)

# ========== ЗАПУСК ==========

if __name__ == '__main__':
    print("❤️ LOVE BOT ЗАПУЩЕН! ❤️")
    print(f"🔑 Пароль для пользователей: {USER_PASSWORD}")
    print(f"👑 Пароль для админа: {ADMIN_PASSWORD}")
    print("🔥 БОТ РАБОТАЕТ 24/7!")
    print(f"👥 Пользователей в базе: {len(users)}")
    print(f"💎 Балансов загружено: {len(user_balance)}")
    bot.polling(none_stop=True)
