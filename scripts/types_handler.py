def get_type(bot):
    @bot.message_handler(content_types=['document'])
    def doc_handler(message):
        get_data(message=message, doc_type='document')


    @bot.message_handler(content_types=['video'])
    def doc_handler(message):
        get_data(message=message, doc_type='video')


    @bot.message_handler(content_types=['audio'])
    def doc_handler(message):
        get_data(message=message, doc_type='audio')


    @bot.message_handler(content_types=['photo'])
    def doc_handler(message):
        get_data(message=message, doc_type='photo')


    @bot.message_handler(content_types=['video_note'])
    def doc_handler(message):
        get_data(message=message, doc_type='video_note')


    @bot.message_handler(content_types=['voice'])
    def doc_handler(message):
        get_data(message=message, doc_type='voice')



