import telebot

from scripts import config, db_handler, keyboards


def new_empty_tag(message):
    bot = telebot.TeleBot(config.TOKEN)
    db_handler.new_tag(user_id=message.from_user.id, tag_name=message.text)
    db_handler.update_current_tag(user_id=db_handler.get_db_user_id(message.from_user.id), tag_name=message.text)
    bot.send_message(message.chat.id, text=f"Тег '{message.text}' создан!")


def search_tag_from_message(message):
    bot = telebot.TeleBot(config.TOKEN)
    tags = db_handler.get_tags(message.from_user.id)
    res = None
    for tag in tags:
        if message.text == tag['tag_name']:
            res = tag
            break
    if res:
        db_handler.update_current_tag(user_id=db_handler.get_db_user_id(message.from_user.id), tag_name=res['tag_name'])
        bot.send_message(message.chat.id, text=f"Вы переключились на тег '{res['tag_name']}'")
    else:
        new_empty_tag(message)
        db_handler.update_current_tag(user_id=db_handler.get_db_user_id(message.from_user.id), tag_name=message.text)


def remove_tag(call):
    bot = telebot.TeleBot(config.TOKEN)
    op = call.data.split(':')[1]
    tag = call.data.split(':')[2]
    if op == 'no':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, text=f"Тег {tag} сохранен", reply_markup=keyboards.default_keyboard)
    else:
        db_handler.remove_tag_by_name(call.message, tag)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, text=f"Тег {tag} удален", reply_markup=keyboards.default_keyboard)
