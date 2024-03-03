from imports import *

def only_admin_check(func):
    def wrapped(update: Update, context: CallbackContext, *args, **kwargs):
        username = update.message.from_user.username
        user_id = update.message.from_user.id
        user_id = str(user_id)

        if only_admins and (username not in propriétaires) and (username not in admins) and (user_id not in propriétaires) and (user_id not in admins):
            print("Режим только для админов")
            update.message.reply_text("🛠 <b>Проводятся технические работы.</b>\nБот временно недоступен", parse_mode='HTML')
            return
        return func(update, context, *args, **kwargs)

    return wrapped

def initialization(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    context.user_data['quiz_in_progress'] = False
    context.user_data['choose_in_progress'] = False
    context.user_data['add_admin'] = False
    context.user_data['del_admin'] = False
    if not context.user_data.get('initializated'):
        context.user_data['mode'] = "fr_to_ru"
    context.user_data['initializated'] = True
    context.user_data['change_admin_mode'] = False


    if user_id not in user_data:
        user_data[user_id] = {}
    if 'words' not in user_data[user_id]:
        user_data[user_id]['words'] = {}
    print("Инициализировано")

    return

def get_keyboard():
    keyboard = [[key] for key in vocabulary.keys()]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

@only_admin_check
def choose_voc(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if not context.user_data.get('initializated'):
        print("Вызов нициализации")
        initialization(update, context)

    if context.user_data['choose_in_progress'] == False:
        context.user_data['choose_in_progress'] = True
        reponse = "👋 Bonjour! Sélectionnez un dictionnaire parmi ceux énumérés ci-dessous et entrez son nom:\n\n"
        for nom in vocabulary.keys():
            reponse += f"• <i>{nom}</i>\n"
        update.message.reply_text(reponse, parse_mode='HTML', reply_markup=get_keyboard())

    else:
        user_input = update.message.text
        user_input = user_input.strip().lower()
        context.user_data['choose_in_progress'] = False

        my_voc = {key.lower(): key for key, value in vocabulary.items()}
        if user_input in my_voc:        
            random.seed()  # Инициализация генератора случайных чисел
            shuffled_keys = list(vocabulary[f"{my_voc[user_input]}"].keys())
            random.shuffle(shuffled_keys)
            words_for_time = {key: vocabulary[f"{my_voc[user_input]}"][key] for key in shuffled_keys}

            if context.user_data['mode'] == "ru_to_fr":
                words_for_time = {value: key for key, value in words_for_time.items()}

            user_data[user_id]['words_for_time'] = {}
            user_data[user_id]['words_for_time'] = words_for_time
            start(update, context)
        else:
            update.message.reply_text("Dictionnaire non valide. Tapez /start encore une fois.")
        context.user_data['choose_in_progress'] = False

    return

@only_admin_check
def choose_mode(update: Update, context: CallbackContext, progress=0):
        if context.user_data['mode'] == "ru_to_fr":
            context.user_data['mode'] = "fr_to_ru"
            update.message.reply_text("🫡 Votre mode a été changé : Français ➡️ Russe\n\n/start pour commencer le quiz !")
        elif context.user_data['mode'] == "fr_to_ru":
            context.user_data['mode'] = "ru_to_fr"
            update.message.reply_text("🫡 Votre mode a été changé : Russe ➡️ Français\n\n/start pour commencer le quiz !")

@only_admin_check
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    for word, translations in user_data[user_id]['words_for_time'].items():
        if context.user_data['quiz_in_progress'] == False:
            context.user_data['quiz_in_progress'] = True
            update.message.reply_text(f"""
                🎉 Quiz est lancé. /stop pour terminer.\n\nEt ainsi, le premier mot: <b>{word.lower()}</b>
            """, parse_mode='HTML')
        else:
            update.message.reply_text(word.capitalize())

        correct_translations = [translation.strip().lower() for translation in translations.split(',')]
        print(word, ', ',translations)

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
    reponse = "<b>Vos résultats:</b>\n\n"
    ansver_count = 0
    if 'correct_count' not in context.user_data:
        context.user_data['correct_count'] = 0
    correct_count = context.user_data['correct_count']

    for word, translation in user_data[user_id]['words'].items():
        my_translation = ""
        if len(translation) > 1:
            ansver_count += 1
            if translation[1] in translation[0]:
                correct_count += 1
                for i in translation[0]:
                    my_translation += f"{i}, "
                reponse += f"✅ {word} — {my_translation.rstrip(', ')}\n" 
            else:
                for i in translation[0]:
                    my_translation += f"{i}, "
                reponse += f"❌ {word} — {translation[1]} (correct: {my_translation.rstrip(', ')})\n"
    if ansver_count < 1:
        update.message.reply_text("🤷‍♂️ <b>Aucun résultat.</b>\n/start pour commencer.", parse_mode='HTML')
    else:
        pourcentage = (correct_count * 100) / ansver_count
        rounded_pourcentage = round(pourcentage)
        reponse += f"\n<i>Statistique:</i>\n{correct_count} sur {ansver_count}; {rounded_pourcentage}%"

        group_id = 
        context.bot.send_message(group_id, f"<b>Données d'utilisateur</b>\n<i>Name:</i> {user_fullname}\n<i>Username:</i> @{username}\n<i>User ID:</i> {user_id}\n\n{reponse}", parse_mode='HTML')
        reponse += "\n\n/start pour commencer encore une fois !"
        update.message.reply_text(reponse, parse_mode='HTML')

    del user_data[user_id]
    initialization(update, context)

    print(correct_count)
    return
