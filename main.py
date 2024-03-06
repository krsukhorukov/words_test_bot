from imports import *
from quiz import choose_voc, choose_mode, initialization, contin, start, get_words
from administration import  add_admin, del_admin, change_admin_mode, send_message_to_all_users

TOKEN = token

def handle_text_input(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_input = update.message.text
    user_fullname = update.message.from_user.full_name
    username = update.message.from_user.username

    try:
        if context.user_data['choose_in_progress'] == True:
            choose_voc(update, context)

        elif context.user_data['quiz_in_progress'] == True:
            print(user_input)
            word = context.user_data.get('testing_word')
            user_data[user_id]['words'][word].append(user_input.strip().lower())  # Сохраняем введенный текст

            if len(user_data[user_id]['words_for_time']) > 0:
                start(update, context)
            else:
                contin(update, context)

        elif context.user_data['add_admin'] == True:
            add_admin(update, context)
        elif context.user_data['del_admin'] == True:
            del_admin(update, context)
        elif context.user_data['get_words'] == True:
            get_words(update, context)
        else:
            update.message.reply_text("🫠 <b>Entrée inattendue.</b>\nTapez /start pour commencer.", parse_mode="HTML")
            
    except Exception as e:
        update.message.reply_text("⚠️ <b>Фатальная ошибка.</b>\nПопробуйте запустить еще раз /start", parse_mode='HTML')
        group_id = 
        context.bot.send_message(group_id, f"⚠️ {user_fullname} столкнулся(ась) с ошибкой.\n\n<b>Données d'utilisateur</b>\n<i>Username:</i> @{username}\n<i>User ID:</i> {user_id}", parse_mode='HTML')

        initialization(update, context)
        print(f"Вызов инициализации для обнуления данных пользователя.\nОшибка: {e}")

def main() -> None:
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", choose_voc))
    dp.add_handler(CommandHandler("stop", contin))
    dp.add_handler(CommandHandler("changer_mode", choose_mode))
    dp.add_handler(CommandHandler("get_words", get_words))
    dp.add_handler(CommandHandler("ajouter_admin", add_admin))
    dp.add_handler(CommandHandler("supprimer_admin", del_admin))
    dp.add_handler(CommandHandler("change_admin_mode", change_admin_mode))
    dp.add_handler(CommandHandler("send_message_to_all_users", send_message_to_all_users))


    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text_input))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
