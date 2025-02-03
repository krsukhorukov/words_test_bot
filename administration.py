from imports import *
from quiz import initialization, hello_world, choose_voc
import languages as lg

def create_bot(token):
    return Bot(token=token)

def get_keyboard_id():
    voc = Database()
    user_id = voc.get_users_table()
    keyboard = [[key] for key in [user_id]]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

def language(update: Update, context: CallbackContext):
    if context.user_data['user_language'] == "RU":
        return lg.l_RU
    elif context.user_data['user_language'] == "FR":
        return lg.l_FR
    elif context.user_data['user_language'] == "AR":
        return lg.l_AR
    else:
        return lg.l_EN

def restricted(func):
    def wrapped(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.message.from_user.id
        db = Database()
        admin_status = db.get_user_data(user_id, block_status=True)
        if admin_status == 10:
            return func(update, context, *args, **kwargs)
        else:
            update.message.reply_text("Ты не админ! Иди отсюда!⛔️")

    return wrapped

def new_user(update: Update, context: CallbackContext):
    hello_world(update, context)

def send_message(bot, user_id, message):
    try:
        bot.send_message(chat_id=user_id, text=message)
        print("Сообщение отправлено успешно!")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

@restricted
def change_admin_status(update: Update, context: CallbackContext):
    initialization(update, context)
    langue = language(update, context)

    db = Database()
    def create_table_image_from_db_data(df):
        if isinstance(df, list):
            df = pd.DataFrame(df)

        # Преобразование специфических математических символов в обычные
        df = df.applymap(lambda x: str(x).translate(str.maketrans({
            "\U0001D434": "A",  # MATHEMATICAL ITALIC CAPITAL A
            "\U0001D45F": "l",  # MATHEMATICAL ITALIC SMALL L
            "\U0001D45A": "i",  # MATHEMATICAL ITALIC SMALL I
            "\U0001D463": "n",  # MATHEMATICAL ITALIC SMALL N
            "\U0001D452": "a"   # MATHEMATICAL ITALIC SMALL A
        })))

        # Устанавливаем подходящий шрифт
        plt.rcParams['font.family'] = 'STIXGeneral'
        plt.rcParams['mathtext.fontset'] = 'stix'

        fig, ax = plt.subplots(figsize=(24, len(df) * 0.6))
        ax.axis('tight')
        ax.axis('off')

        table = ax.table(
            cellText=df.values,
            colLabels=df.columns,
            cellLoc='center',
            loc='center',
            colColours=['#f2f2f2'] * len(df.columns),
        )
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.5, 1.5)

        plt.savefig('table.png', bbox_inches='tight', dpi=300)

        resize_image('table.png', 'table.jpg')

    def resize_image(image_path, output_path):
        with Image.open(image_path) as img:
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            width, height = img.size
            max_size = (10000, 10000)
            min_size = (10, 10)

            if width > max_size[0] or height > max_size[1] or width < min_size[0] or height < min_size[1]:
                img.thumbnail(max_size, Image.ANTIALIAS)
                img.save(output_path, quality=95)
            else:
                img.save(output_path, quality=95)

    def send_photo(bot, chat_id):
        with open('table.jpg', 'rb') as photo:
            bot.send_photo(chat_id=chat_id, photo=photo)
        os.remove('table.jpg')
        os.remove('table.png')
        return

    if context.user_data['change_admin_status'] == False:
        context.user_data['change_admin_status'] = True
        context.user_data['change_admin_status_stage'] = 1
        voc = Database()
        user_ids = voc.get_users_table()
        user_id = update.message.from_user.id

        keyboard = [[str(user_id)] for user_id in user_ids]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        bot = create_bot(TOKEN)
        df = db.get_users_table(is_keyboard=False)
        create_table_image_from_db_data(df)
        send_photo(bot, user_id)
        update.message.reply_text(text=f"{langue['Change admin statis (1)']}", parse_mode="HTML", reply_markup=reply_markup)

    elif (context.user_data['change_admin_status'] == True) and (context.user_data['change_admin_status_stage'] == 1):
        context.user_data['change_admin_status_stage'] = 2

        context.user_data['id_for_change'] = int(update.message.text)
        update.message.reply_text(langue["Change admin statis (2)"], parse_mode='HTML')
    
    elif  (context.user_data['change_admin_status'] == True) and (context.user_data['change_admin_status_stage'] == 2):
        new_status = int(update.message.text)
        id_to_change = context.user_data['id_for_change']
        if 0 <= new_status <= 10:
            db.change_admin_status(id_to_change, new_status)
            context.user_data['change_admin_status'] = False
            context.user_data['change_admin_status_stage'] = 0
            context.user_data['id_for_change'] = 0
            reponse = f"✅ {langue['Change admin status succes (1)']} <b>{id_to_change}</b> {langue['Change admin status succes (2)']} {new_status}"
            update.message.reply_text(reponse, parse_mode='HTML')
        else:
            update.message.reply_text(langue["Change admin status error"], parse_mode='HTML')

@restricted
def change_admin_mode(update: Update, context: CallbackContext):
    initialization(update, context)
    user_id = update.message.from_user.id
    db = Database()
    only_admins = db.admin_mode(user_id)

    # важное оповещение
    logger.warning(f"Режим для одминов изменен. Теперь {only_admins}")
    update.message.reply_text(f"Режим для одминов изменен. Теперь **{only_admins}**", parse_mode='Markdown')
    return

@restricted
def send_message_to_all_users(update: Update, context: CallbackContext):
    initialization(update, context)
    try:
        chat_ids = [chat.id for chat in context.bot.get_chat_administrators(update.message.chat_id)]
        
        print(len(chat_ids))
        # for chat_id in chat_ids:
        #     context.bot.send_message(chat_id, text="Ваше сообщение всем пользователям")
        
        update.message.reply_text("Сообщение отправлено всем пользователям")
    except TelegramError as e:
        update.message.reply_text(f"Ошибка при отправке сообщения: {e}")