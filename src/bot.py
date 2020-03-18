import telegram
from telegram.ext import Updater, CommandHandler
from configparser import ConfigParser
from database.functions import *


class Bot:
    '''
    Classe que fará a comunicação com o bot do telegram.
    Necessita de um arquivo config.ini com o seguinte parâmetro:
        [telegram]
        token = <token>
    '''
    def __init__(self):
        parser = ConfigParser()
        parser.read('./config.ini')
        token = parser['telegram']['token']
        self.bot = telegram.Bot(token=token)
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        
        self.start_handler = CommandHandler('start', self.start)
        self.register_handler = CommandHandler('register', self.register_user)
        
        self.dispatcher.add_handler(self.start_handler)
        self.dispatcher.add_handler(self.register_handler)

    def start(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Bem vindo"
        )

    def register_user(self, update, context):
        chat_id = update.message.chat_id
        add_user(chat_id)

    def start_pooling(self):
        self.updater.start_polling()

    def send_report(self, global_report, local_report):
        report = (
            "De hora em hora o CoronaBot informa os números "
            "dos casos de coronavírus no Brasil e no mundo:\n\n"
            "======== Situação Global ========\n"
            f"- Total de casos: {global_report['total_cases']}\n"
            f"- Total de mortes: {global_report['total_deaths']}\n"
            f"- Casos hoje: {global_report['total_new_cases_today']}\n"
            f"- Mortes hoje: {global_report['total_new_deaths_today']}\n"
            "\n"
            "======== Situação no Brasil ========\n"
            f"- Total de casos: {local_report['total_cases']}\n"
            f"- Total de mortes: {local_report['total_deaths']}\n"
            f"- Casos hoje: {local_report['total_new_cases_today']}\n"
            f"- Mortes hoje: {local_report['total_new_deaths_today']}\n"
            "\n\n"
            "Fonte: thevirustracker.com"
        )

        user_ids = get_users()
        for user_id in user_ids:
            self.bot.send_message(user_id, report)
