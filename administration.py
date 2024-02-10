from imports import *
from quiz import initialization

def add_admin(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    
    if username in propriétaires:
        if context.user_data['add_admin'] == False:
            initialization(update, context)
            print(f"Вызов инициализации для обнуления данных пользователя.")

            context.user_data['add_admin'] = True
            update.message.reply_text("Введите username нового админа. Важно вводить только username.")
        else:
            user_input = update.message.text
            admins.append(user_input.strip().replace("@", ""))
            update.message.reply_text("✅ Админ добавлен!")
            print(admins)
            context.user_data['add_admin'] = False

    else:
        update.message.reply_text("Ты что здесь делаешь? Иди отсюда!")

def del_admin(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    
    if username in propriétaires:
        if context.user_data['del_admin'] == False:
            initialization(update, context)
            print(f"Вызов инициализации для обнуления данных пользователя.")

            context.user_data['del_admin'] = True
            reponse = "Введите username админа, которого хотите удалить. Важно вводить только username. Вот список действующий админов:\n\n"
            for admin in admins:
                reponse += f"{admin}\n"
            update.message.reply_text(reponse)
        else:
            user_input = update.message.text
            user_input = user_input.strip().replace("@", "")
            if user_input in admins:
                admins.remove(user_input)
                update.message.reply_text("✅ Админ удален!")
            else:
                update.message.reply_text("❌ <b>Админ не найден!</b>\nПопробуйте еще раз /del_admin", parse_mode='HTML')

            print(admins)
            context.user_data['del_admin'] = False

    else:
        update.message.reply_text("Ты что здесь делаешь? Иди отсюда!")
