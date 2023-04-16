from scripts import db_handler, config, keyboards
import telebot


def get_data(message, doc_type, file_id, file_name=None):
    bot = telebot.TeleBot(config.TOKEN)
    try:
        db_handler.new_file(user_id=message.from_user.id,
                            tag_name=message.caption,
                            file_id=file_id,
                            f_type=doc_type,
                            file_name=file_name)
        bot.send_message(message.chat.id, text="Файл успешно загружен!", reply_markup=keyboards.default_keyboard)
    except Exception:
        bot.send_message(message.chat.id, text="Что то пошло не так", reply_markup=keyboards.default_keyboard)

    # if message.caption:  # TODO Обработка ввода тега
    #     file_data['tag_name'] = message.caption
    # else:
    #     bot.reply_to(message, text='Введите тег')
    # print(file_data)


def send_data(call):
    f_id = call.data.split(':')[1]
    print(f_id, "f_id")
    file_data = db_handler.get_file_by_id(f_id)
    print(file_data.type, file_data.file_id, "file_data")
    type_handler(call.message.chat.id, file_data.type, file_data.file_id)
    # if file_data:
    #     bot.send_document(chat_id=file_data['chat_id'], document=file_data['file_id'])
    # else:
    #     pass


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
