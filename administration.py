from imports import *
from quiz import initialization

def restricted(func):
    def wrapped(update: Update, context: CallbackContext, *args, **kwargs):
        username = update.message.from_user.username
        if username in propriétaires:
            return func(update, context, *args, **kwargs)
        else:
            update.message.reply_text("Ты не админ! Иди отсюда!")

    return wrapped

@restricted
def add_admin(update: Update, context: CallbackContext):
    if context.user_data.get('add_admin', False) is False:
        initialization(update, context)
        print(f"Вызов инициализации для обнуления данных пользователя.")

        context.user_data['add_admin'] = True
        update.message.reply_text("Введите username или ID нового админа. Важно вводить только username.")
    else:
        user_input = update.message.text
        admins.append(user_input.strip().replace("@", ""))
        update.message.reply_text("✅ Админ добавлен!")
        print(admins)
        context.user_data['add_admin'] = False

@restricted
def del_admin(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    
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

@restricted
def change_admin_mode(update: Update, context: CallbackContext):
    global only_admins
    if only_admins == True:
        only_admins = False
    else:
        only_admins = True

    update.message.reply_text(f"Режим для одминов изменен. Теперь {only_admins}")
    return

@restricted
def send_message_to_all_users(update: Update, context: CallbackContext):
    try:
        chat_ids = [chat.id for chat in context.bot.get_chat_administrators(update.message.chat_id)]
        
        print(len(chat_ids))
        # for chat_id in chat_ids:
        #     context.bot.send_message(chat_id, text="Ваше сообщение всем пользователям")
        
        update.message.reply_text("Сообщение отправлено всем пользователям")
    except TelegramError as e:
        update.message.reply_text(f"Ошибка при отправке сообщения: {e}")