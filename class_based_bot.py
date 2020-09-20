import os
import logging

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
from telegram import (ParseMode)
from telegram.error import BadRequest
from telegram import (ReplyKeyboardMarkup)

from decorators import log


class ClassBasedBot:

    MAIN_KEYBOARD = [['1', '2'],
                     ['3'],
                     ['4']
                     ]
    main_markup= ReplyKeyboardMarkup(MAIN_KEYBOARD)

    def __init__(self, token):
        self.updater = Updater(token, use_context=True)
        self._register_handlers()
        self._start_polling()

    def _start_polling(self):
        self.updater.start_polling()
        self.updater.idle()

    @property
    def dispatcher(self):
        return self.updater.dispatcher

    def _register_handlers(self):
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_error_handler(self.error)

    def _start_polling(self):
        self.updater.start_polling()
        self.updater.idle()

    @log
    def start(self, update, context):
        """Send message on `/start`."""
        logging.info(f'Message to start {update.message.text}')
        update.message.reply_text(
            'Hi there',
            reply_markup=self.main_markup
        )

    @log
    def error(self, update, context):
        devs = [os.getenv('DEVS')]
        print('Error happened')
        if update.effective_message:
            text = 'Sheet happens'
            update.effective_message.reply_text(text, reply_markup=bb.main_markup)
        trace = "".join(traceback.format_tb(sys.exc_info()[2]))
        payload = ""
        if update.effective_user:
            payload += f' with the user {mention_html(update.effective_user.id, update.effective_user.first_name)}'
        if update.effective_chat:
            payload += f' within the chat <i>{update.effective_chat.title}</i>'
            if update.effective_chat.username:
                payload += f' (@{update.effective_chat.username})'
        if update.poll:
            payload += f' with the poll id {update.poll.id}.'
        text = f"Hey.\n The error <code>{context.error}</code> happened{payload}. The full traceback:\n\n<code>{trace}" \
            f"</code>"
        for dev_id in devs:
            context.bot.send_message(dev_id, text, parse_mode=ParseMode.HTML)


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    ClassBasedBot(token=os.getenv('BOT_TOKEN'))
