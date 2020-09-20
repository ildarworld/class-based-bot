from datetime import datetime
from functools import wraps

from telegram import ChatAction

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def log(func):
    def wrapper(self=None, *args, **kwargs):
        func_str = func.__name__
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            logger.error(datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
                         + f' Error in {func_str} args: {args} and {kwargs} \nError: {ex}')
    return wrapper

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, self=None, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context,  *args, **kwargs)
        return command_func

    return decorator

