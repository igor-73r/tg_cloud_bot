from telebot import types
from scripts import db_handler


default_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
rm_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

rm_btn = types.KeyboardButton(text="Удалить текущий тег")
btn = types.KeyboardButton(text="Мои теги")

rm_keyboard.row(btn).row(rm_btn)
default_keyboard.add(btn)


def get_tags(user_id):
    tags = db_handler.get_tags(user_id=user_id)
    buttons = [types.InlineKeyboardButton(
        text=tag['tag_name'], callback_data=f"open:{tag['tag_id']}")
        for tag in tags]
    keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    return types.InlineKeyboardMarkup(keyboard)


def yes_no(current_tag):  # TODO Multi_Upload
    buttons = [types.InlineKeyboardButton(text="Да", callback_data=f"delete:yes:{current_tag}"),
               types.InlineKeyboardButton(text="Нет", callback_data=f"delete:no:{current_tag}")]
    keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    return types.InlineKeyboardMarkup(keyboard)


def get_files(call):
    tag_id = call.data.split(':')[1]
    files = db_handler.get_files(tag_id=tag_id)
    db_handler.update_current_tag(user_id=db_handler.get_db_user_id(call.message.chat.id),
                                  tag_name=db_handler.get_tag_by_id(tag_id))
    buttons = [types.InlineKeyboardButton(  # TODO none in name with photo
        text="Без имени" if file['f_name'] is None else file['f_name'], callback_data=f"send:{file['id']}")
        for file in files]
    keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    return types.InlineKeyboardMarkup(keyboard)
