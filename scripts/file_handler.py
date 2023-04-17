from scripts import db_handler, config, keyboards, features
import telebot
import threading

bot = telebot.TeleBot(config.TOKEN)


def reset_tag(message):
    db_handler.update_current_tag(db_handler.get_db_user_id(message.from_user.id), None)


timer = threading.Timer(600, reset_tag)


def get_data(message, doc_type, file_id, file_name=None):
    current_tag = db_handler.get_current_tag(db_handler.get_db_user_id(message.from_user.id))

    if not message.caption and current_tag is None:
        features.match_tag(message=message, d_type=doc_type, f_id=file_id, f_name=file_name)

    elif not message.caption and current_tag is not None:
        print(current_tag)
        features.load_file(message, current_tag, doc_type, file_id, file_name)

    elif message.caption and current_tag is None or current_tag is not None:
        db_handler.update_current_tag(db_handler.get_db_user_id(message.from_user.id), message.caption)
        current_tag = db_handler.get_current_tag(db_handler.get_db_user_id(message.from_user.id))
        print(current_tag)
        features.load_file(message=message, tag_name=message.caption,
                           doc_type=doc_type, file_id=file_id, file_name=file_name)


def send_data(call):
    f_id = call.data.split(':')[1]
    print(f_id, "f_id")
    file_data = db_handler.get_file_by_id(f_id)
    print(file_data.type, file_data.file_id, "file_data")
    type_handler(call.message.chat.id, file_data.type, file_data.file_id)


def type_handler(chat_id, type, file_id):
    bot = telebot.TeleBot(config.TOKEN)
    match type:
        case 'document':
            bot.send_document(chat_id, document=file_id, reply_markup=keyboards.default_keyboard)
        case 'video':
            bot.send_video(chat_id, video=file_id, reply_markup=keyboards.default_keyboard)
        case 'audio':
            bot.send_audio(chat_id, audio=file_id, reply_markup=keyboards.default_keyboard)
        case 'video_note':
            bot.send_video_note(chat_id, data=file_id, reply_markup=keyboards.default_keyboard)
        case 'voice':
            bot.send_voice(chat_id, voice=file_id, reply_markup=keyboards.default_keyboard)
        case 'photo':
            bot.send_photo(chat_id, photo=file_id, reply_markup=keyboards.default_keyboard)
