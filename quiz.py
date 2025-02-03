from imports import *
import languages as lg

def language(update: Update, context: CallbackContext):
    if context.user_data['user_language'] == "RU":
        return lg.l_RU
    elif context.user_data['user_language'] == "FR":
        return lg.l_FR
    elif context.user_data['user_language'] == "AR":
        return lg.l_AR
    else:
        return lg.l_EN

def only_admin_check(func):
    def wrapped(update: Update, context: CallbackContext, *args, **kwargs):
        langue = language(update, context)
        user_id = update.message.from_user.id
        db = Database()
        status_blocked, admin_status, commentaire, only_admins = db.get_user_data(user_id)
        if status_blocked:
            update.message.reply_text(f"{langue['Status blocked']} {commentaire}", parse_mode='HTML')
            initialization(update, context)
            return
        if only_admins and admin_status == 0:
            logger.info(f"Доступ для пользователя {user_id} закрыт: режим технических работ")
            update.message.reply_text(f"{langue['Technical works']}", parse_mode='HTML')
            return
        return func(update, context, *args, **kwargs)

    return wrapped

def initialization(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    context.user_data['quiz_in_progress'] = False
    context.user_data['choose_in_progress'] = False
    context.user_data['add_admin'] = False
    context.user_data['change_admin_status'] = False

    if not context.user_data.get('initializated'):
        context.user_data['mode'] = "fr_to_ru"
        context.user_data['user_language'] = "RU"

    context.user_data['initializated'] = True
    context.user_data['change_admin_mode'] = False
    context.user_data['change_admin_status'] = False
    context.user_data['change_admin_status_stage'] = 0
    context.user_data['id_for_change'] = 0
    context.user_data['get_words'] = False
    context.user_data['first start'] = False


    if user_id not in user_data:
        user_data[user_id] = {}
    if 'words' not in user_data[user_id]:
        user_data[user_id]['words'] = {}
    print("Инициализировано")

    return

def get_keyboard():
    voc = Database()
    liste = voc.db_get_words("vocabulary")
    keyboard = [[key] for key in liste]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

def get_keyboard_languages():
    keyboard = [
            ["Русский 🇷🇺"],
            ["English 🇬🇧"],
            ["اللغة العربية🇪🇬"],
            ["Français 🇫🇷"]
        ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

def hello_world(update: Update, context: CallbackContext):
    if not context.user_data.get('initializated'):
        logger.info("Вызов нициализации")
        initialization(update, context)

    user_id = update.message.from_user.id
    user_fullname = update.message.from_user.full_name
    username = update.message.from_user.username
    user_input = update.message.text
    message = language(update, context)

    if context.user_data['first start'] == False:
        update.message.reply_text(f"{message['Choose lang start']}", parse_mode='HTML', reply_markup=get_keyboard_languages())
        context.user_data['first start'] = True
    else:
        if user_input == "Русский 🇷🇺":
            context.user_data['user_language'] = "RU"
        elif user_input == "Français 🇫🇷":
            context.user_data['user_language'] = "FR"
        elif user_input == "English 🇬🇧":
            context.user_data['user_language'] = "EN"
        elif user_input == "اللغة العربية🇪🇬":
            context.user_data['user_language'] = "AR"
        else:
            logger.error("Ошибка в выборе языка")

        db = Database()
        list_users = db.get_users_table()

        if user_id not in list_users:
            message = language(update, context)
            update.message.reply_text(f"{message['Instruction 1']}", parse_mode='HTML')
            update.message.reply_text(f"{message['Instruction 2']}", parse_mode='HTML')
            context.user_data['first start'] = False
            
        db.check_and_create_user(user_id, user_fullname, username)
    return

@only_admin_check
def get_words(update: Update, context: CallbackContext):
    if not context.user_data.get('initializated'):
        logger.info("Вызов нициализации")
        initialization(update, context)

    message = language(update, context)
    voc = Database()

    reponse = ""
    if context.user_data['get_words'] == False:
        context.user_data['get_words'] = True
        reponse = message["Get dict"]
        liste = voc.db_get_words("vocabulary")
        for nom in liste:
            reponse += f"🔹 <i>{nom}</i>\n"
        update.message.reply_text(reponse, parse_mode='HTML', reply_markup=get_keyboard())

    else:
        user_input = update.message.text
        context.user_data['get_words'] = False

        try:
            word, translation = voc.db_get_words(user_input, 1)
            logger.info(f"Загружен словарь {user_input}")
            number = 0
            for i in range(0, len(word)):
                number += 1
                reponse += f"{number}. {word[i]} — {translation[i]}\n"
            update.message.reply_text(f"{reponse} {message['To start']}")
        except Exception as e:
            update.message.reply_text(message["Dict error"])
            logger.error(e)

@only_admin_check
def choose_voc(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if not context.user_data.get('initializated'):
        print("Вызов нициализации")
        initialization(update, context)
        hello_world(update, context)


    message = language(update, context)
    voc = Database()
    liste = voc.db_get_words("vocabulary")

    if context.user_data['choose_in_progress'] == False:
        context.user_data['choose_in_progress'] = True
        reponse = message["Select dict"]
        for nom in liste:
            reponse += f"🔹 <i>{nom}</i>\n"
        update.message.reply_text(reponse, parse_mode='HTML', reply_markup=get_keyboard())

    else:
        user_input = update.message.text
        context.user_data['choose_in_progress'] = False

        word, translation = voc.db_get_words(user_input, is_dict=1)
        if user_input in liste:        
            my_voc = dict(zip(word, translation))
            random.shuffle(word)
            words_for_time = {key: my_voc[key] for key in word}

            if context.user_data['mode'] == "ru_to_fr":
                words_for_time = {value: key for key, value in words_for_time.items()}

            user_data[user_id]['words_for_time'] = {}
            user_data[user_id]['words_for_time'] = words_for_time
            start(update, context)
        else:
            update.message.reply_text(message["Dict error"])
        context.user_data['choose_in_progress'] = False

    return

@only_admin_check
def choose_mode(update: Update, context: CallbackContext, progress=0):
    if not context.user_data.get('initializated'):
        print("Вызов нициализации")
        initialization(update, context)

    message = language(update, context)

    if context.user_data['mode'] == "ru_to_fr":
        context.user_data['mode'] = "fr_to_ru"
        update.message.reply_text(message["Change mode fr to ru"])
    elif context.user_data['mode'] == "fr_to_ru":
        context.user_data['mode'] = "ru_to_fr"
        update.message.reply_text(message["Change mode ru to fr"])

@only_admin_check
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    message = language(update, context)


    for word, translations in user_data[user_id]['words_for_time'].items():
        if context.user_data['quiz_in_progress'] == False:
            context.user_data['quiz_in_progress'] = True
            update.message.reply_text(f"{message['Start quiz']} <b>{word}</b>", parse_mode='HTML')
        else:
            def capitalize_first_letter(phrase):
                if not phrase:
                    return phrase
                return phrase[0].upper() + phrase[1:]
            update.message.reply_text(capitalize_first_letter(word))

        correct_translations = [translation.strip().lower() for translation in translations.split(',')]
        logger.info(f"{user_id} : {word}, {translations}")

        if word not in user_data[user_id]['words']:
            user_data[user_id]['words'][word] = []
        user_data[user_id]['words'][word].append(correct_translations)

        context.user_data['testing_word'] = word
        del user_data[user_id]['words_for_time'][word]
        break
    return

@only_admin_check
def contin(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_fullname = update.message.from_user.full_name
    username = update.message.from_user.username
    ansver_count = 0
    message = language(update, context)
    reponse = message["Results"]


    if 'correct_count' not in context.user_data:
        context.user_data['correct_count'] = 0
    correct_count = context.user_data['correct_count']

    for word, translation in user_data[user_id]['words'].items():
        my_translation = ""
        if len(translation) > 1:
            ansver_count += 1
            if translation[1] in translation[0] or translation[2] == 1:
                correct_count += 1
                for i in translation[0]:
                    my_translation += f"{i}, "
                reponse += f"✅ {word} — {my_translation.rstrip(', ')}\n" 
            else:
                for i in translation[0]:
                    my_translation += f"{i}, "
                reponse += f"❌ {word} — {translation[1]} {message['False user translate']} {my_translation.rstrip(', ')})\n"
    if ansver_count < 1:
        update.message.reply_text(message["No result"], parse_mode='HTML')
    else:
        pourcentage = (correct_count * 100) / ansver_count
        rounded_pourcentage = round(pourcentage)
        reponse += f"{message['Statistique 1']} {correct_count} {message['Statistique 2']} {ansver_count}; {rounded_pourcentage}%"

        group_id = CHAT_ID
        context.bot.send_message(group_id, f"<b>Données d'utilisateur</b>\n<i>Name:</i> {user_fullname}\n<i>Username:</i> @{username}\n<i>User ID:</i> {user_id}\n\n{reponse}", parse_mode='HTML')
        reponse += message["Restart"]
        update.message.reply_text(reponse, parse_mode='HTML')

    del user_data[user_id]
    initialization(update, context)

    logger.info(correct_count)
    return
