from imports import *
from quiz import choose_voc, choose_mode, initialization, done_voc
from administration import  add_admin, del_admin

TOKEN = token
my_vocabulary = vocabulary

results = {}
my_context = {}

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    # user_sum = {}

    for word, translations in user_data[user_id]['words_for_time'].items():
        if context.user_data['quiz_in_progress'] == False:
            context.user_data['quiz_in_progress'] = True
            update.message.reply_text(f"""
                Quiz est lancé. Entrez les traductions des mots. Si vous voulez terminer, envoyez /stop \n\nEt ainsi, le premier mot: {word.lower()}
            """)
        else:
            update.message.reply_text(word)


        correct_translations = [translation.strip().lower() for translation in translations.split(',')]
        print(word, ':',translations)

        if user_id not in user_data:
            user_data[user_id] = {}
        if 'words' not in user_data[user_id]:
            user_data[user_id]['words'] = {}
        if word not in user_data[user_id]['words']:
            user_data[user_id]['words'][word] = []
        user_data[user_id]['words'][word].append(correct_translations)

        context.user_data['testing_word'] = word
        del user_data[user_id]['words_for_time'][word]
        break

def handle_text_input(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_input = update.message.text

    try:
        if context.user_data['mode_in_progress'] == True:
            choose_mode(update, context, 1)

        elif context.user_data['quiz_in_progress'] == True:
            print(user_input)
            word = context.user_data.get('testing_word')
            user_data[user_id]['words'][word].append(user_input.strip().lower())  # Сохраняем введенный текст

            if len(user_data[user_id]['words_for_time']) > 0:
                start(update, context)
            else:
                contin(update, context)

        elif context.user_data['choose_in_progress'] == True:
            done_voc(update, context)
        elif context.user_data['add_admin'] == True:
            add_admin(update, context)
        elif context.user_data['del_admin'] == True:
            del_admin(update, context)
        else:
            update.message.reply_text("Entrée inattendue. Tapez /start pour commencer.")
            
    except Exception as e:
        update.message.reply_text("⚠️ <b>Фатальная ошибка.</b>\nПопробуйте запустить еще раз /start", parse_mode='HTML')
        initialization(update, context)
        print(f"Вызов инициализации для обнуления данных пользователя.\nОшибка: {e}")

def contin(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
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
        update.message.reply_text("Результаты отсутствуют.")
    else:
        pourcentage = (correct_count * 100) / ansver_count
        rounded_pourcentage = round(pourcentage)
        reponse += f"\n<i>Statistique:</i>\n{correct_count} sur {ansver_count}; {rounded_pourcentage}%"

        update.message.reply_text(reponse, parse_mode='HTML')

    del user_data[user_id]
    context.user_data['quiz_in_progress'] = False

    print(correct_count)

def main() -> None:
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", choose_voc))
    dp.add_handler(CommandHandler("stop", contin))
    dp.add_handler(CommandHandler("choose_mode", choose_mode))
    dp.add_handler(CommandHandler("add_admin", add_admin))
    dp.add_handler(CommandHandler("del_admin", del_admin))


    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text_input))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
