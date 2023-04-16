from telebot import types
from scripts import db_handler


default_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn = types.KeyboardButton(text="Мои теги")
default_keyboard.add(btn)


def get_tags(user_id):
    tags = [i['tag_name'] for i in db_handler.get_tags(user_id=user_id)]
    buttons = [types.InlineKeyboardButton(
        text=tag, callback_data=f'open:{tag}')
        for tag in tags]
    keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    return types.InlineKeyboardMarkup(keyboard)


def get_files(call):
    tag_name = call.data.split(':')[1]
    # print(call.message.from_user.id)
    files = db_handler.get_files(call.message.chat.id, tag_name=tag_name)
    for i in files:
        print(i)
    buttons = [types.InlineKeyboardButton(  # TODO none in name with photo
        text="Без имени" if file['f_name'] == None else file['f_name'], callback_data=f"send:{file['id']}") #{file['f_id']}
        for file in files]
    keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    return types.InlineKeyboardMarkup(keyboard)
