from imports import *


my_vocabulary = vocabulary

def initialization(update: Update, context: CallbackContext):
    context.user_data['mode_in_progress'] = False
    context.user_data['quiz_in_progress'] = False
    context.user_data['choose_in_progress'] = False
    context.user_data['initializated'] = True
    context.user_data['mode'] = "fr_to_ru"
    print("Initializated")

    return

def invers_start(update: Update, context: CallbackContext, user_data):
    user_id = update.message.from_user.id

def choose_voc(update: Update, context: CallbackContext):
    if context.user_data.get('initializated', False):
        print("Инициализация не необходима")
    else:
        print("Инициализация")
        initialization(update, context)

    context.user_data['choose_in_progress'] = True
    reponse = "Bonjour! Sélectionnez un dictionnaire parmi ceux énumérés ci-dessous et entrez son nom:\n"
    for i in my_vocabulary.keys():
        reponse += f"{i}\n"
    update.message.reply_text(reponse)

    return

def choose_mode(update: Update, context: CallbackContext, progress=0):
    if progress == 0:
        update.message.reply_text("Выберете режим и введите его номер:\n\n1. Français ➡️ Russe\n2. Russe ➡️ Français")
        context.user_data['mode_in_progress'] = True
    else:
        user_input = update.message.text
        if user_input == '1':
            context.user_data['mode'] = "fr_to_ru"
            update.message.reply_text("Вы выбрали Français ➡️ Russe")
        elif user_input == '2':
            context.user_data['mode'] = "ru_to_fr"
            update.message.reply_text("Вы выбрали Russe ➡️ Français")
        else:
            update.message.reply_text("Ошибка ввода. Введите команду /choose_mode еще раз.")
        context.user_data['mode_in_progress'] = False



# def choose_voc(update: Update, context: CallbackContext, user_input, user_data):
#     context.user_data['choose_in_progress'] = False
#     print(my_vocabulary[f"{user_input}"])
#     random.seed()  # Инициализация генератора случайных чисел
#     shuffled_keys = list(my_vocabulary[f"{user_input}"].keys())
#     random.shuffle(shuffled_keys)
#     words_for_time = {key: my_vocabulary[f"{user_input}"][key] for key in shuffled_keys}

#     user_data['words_for_time'] = words_for_time
#     start(update, context)

#     return user_data

def start(update: Update, context: CallbackContext, user_data) -> None:
    for word, translations in user_data['words_for_time'].items():
        try:
            if context.user_data['quiz_in_progress'] == False:
                context.user_data['quiz_in_progress'] = True
                update.message.reply_text(f"""
                                            Quiz est lancé. Entrez les traductions des mots. 
                                            Si vous voulez terminer, envoyez /stop \n\nEt ainsi, le premier mot: {word.lower()}
                                            """)
            else:
                update.message.reply_text(word)
        except:
            context.user_data['quiz_in_progress'] = True
            update.message.reply_text(f"""
                                        Quiz est lancé. Entrez les traductions des mots. 
                                        Si vous voulez terminer, envoyez /stop \n\nEt ainsi, le premier mot: {word.lower()}
                                        """)

        correct_translations = [translation.strip().lower() for translation in translations.split(',')]
        print(word, ', ',translations)

        if word not in user_data['words']:
            user_data['words'][word] = []
        user_data['words'][word].append(correct_translations)

        context.user_data['testing_word'] = word
        del user_data['words_for_time'][word]
        break
    return user_data

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
