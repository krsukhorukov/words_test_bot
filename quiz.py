from imports import *


my_vocabulary = vocabulary

def initialization(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    context.user_data['mode_in_progress'] = False
    context.user_data['quiz_in_progress'] = False
    context.user_data['choose_in_progress'] = False
    context.user_data['add_admin'] = False
    context.user_data['del_admin'] = False
    context.user_data['initializated'] = True
    context.user_data['mode'] = "fr_to_ru"


    if user_id not in user_data:
        user_data[user_id] = {}
    if 'words' not in user_data[user_id]:
        user_data[user_id]['words'] = {}
    print("Инициализировано")

    return

def choose_voc(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    if only_admins == True:
        print("Режим только для админов")
        try:
            if username in propriétaires or username in admins:

                if context.user_data.get('initializated', False):
                    print("Инициализация не необходима")
                else:
                    print("Вызов нициализации")
                    initialization(update, context)

                context.user_data['choose_in_progress'] = True
                reponse = "Bonjour! Sélectionnez un dictionnaire parmi ceux énumérés ci-dessous et entrez son nom:\n"
                for i in my_vocabulary.keys():
                    reponse += f"{i}\n"
                update.message.reply_text(reponse)
            else:
                update.message.reply_text("ℹ️ <b>Проводятся технические работы.</b>\nБот временно не доступен", parse_mode='HTML')

        except:
            update.message.reply_text("ℹ️ <b>Проводятся технические работы.</b>\nБот временно не доступен", parse_mode='HTML')
    
    else:
        if context.user_data.get('initializated', False):
            print("Инициализация не необходима")
        else:
            print("Вызов нициализации")
            initialization(update, context)

        context.user_data['choose_in_progress'] = True
        reponse = "Bonjour! Sélectionnez un dictionnaire parmi ceux énumérés ci-dessous et entrez son nom:\n"
        for i in my_vocabulary.keys():
            reponse += f"{i}\n"
        update.message.reply_text(reponse)

    return

def done_voc(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_input = update.message.text
    user_input = user_input.strip().lower()
    context.user_data['choose_in_progress'] = False
    if user_input in my_vocabulary:        
        random.seed()  # Инициализация генератора случайных чисел
        shuffled_keys = list(my_vocabulary[f"{user_input}"].keys())
        random.shuffle(shuffled_keys)
        words_for_time = {key: my_vocabulary[f"{user_input}"][key] for key in shuffled_keys}

        if context.user_data['mode'] == "ru_to_fr":
            words_for_time = {value: key for key, value in words_for_time.items()}

        user_data[user_id]['words_for_time'] = {}
        user_data[user_id]['words_for_time'] = words_for_time
        start(update, context)
    else:
        update.message.reply_text("Dictionnaire non valide. Tapez /start encore une fois.")


def choose_mode(update: Update, context: CallbackContext, progress=0):
    if progress == 0:
        update.message.reply_text("Выберете режим и введите его номер:\n\n1. Français ➡️ Russe\n2. Russe ➡️ Français")
        context.user_data['mode_in_progress'] = True
    else:
        user_input = update.message.text
        if user_input == '1':
            context.user_data['mode'] = "fr_to_ru"
            update.message.reply_text("Votre mode Français ➡️ Russe")
        elif user_input == '2':
            context.user_data['mode'] = "ru_to_fr"
            update.message.reply_text("Votre mode Russe ➡️ Français")
        else:
            update.message.reply_text("Requête invalide. Tapez /choose_mode encore une fois.")
        context.user_data['mode_in_progress'] = False



def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    for word, translations in user_data[user_id]['words_for_time'].items():
        if context.user_data['quiz_in_progress'] == False:
            context.user_data['quiz_in_progress'] = True
            update.message.reply_text(f"""
                Quiz est lancé. Entrez les traductions des mots. Si vous voulez terminer, envoyez /stop \n\nEt ainsi, le premier mot: {word.lower()}
            """)
        else:
            update.message.reply_text(word)

        correct_translations = [translation.strip().lower() for translation in translations.split(',')]
        print(word, ', ',translations)

        if word not in user_data[user_id]['words']:
            user_data[user_id]['words'][word] = []
        user_data[user_id]['words'][word].append(correct_translations)

        context.user_data['testing_word'] = word
        del user_data[user_id]['words_for_time'][word]
        break
    return

def contin(update: Update, context: CallbackContext, user_data):
    reponse = ""
    if 'correct_count' not in context.user_data:
        context.user_data['correct_count'] = 0
    correct_count = context.user_data['correct_count']

    for word, translation in user_data['words'].items():
        print(translation)
        my_translation = ""
        if len(translation) > 1:
            if translation[1] in translation[0]:
                correct_count += 1
                for i in translation[0]:
                    my_translation += f"{i}, "
                reponse += f"✅ {word} — {my_translation.rstrip(', ')}\n" 
            else:
                for i in translation[0]:
                    my_translation += f"{i}, "
                reponse += f"❌ {word} — <s>{translation[1]}</s> (correct: {my_translation.rstrip(', ')})\n"

    update.message.reply_text(f"<b>Vos résultats:</b>\n\n{reponse}", parse_mode='HTML')
    # process_user_results(user_id, reponse)
    context.user_data['quiz_in_progress'] = False

    print(correct_count)
    return
