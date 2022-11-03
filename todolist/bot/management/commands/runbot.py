from django.core.management import BaseCommand

from bot.tg import TgClient

from todolist.settings import TG_TOKEN
from bot.models import TgUser


class Command(BaseCommand):
    help = 'Start telegram bot'

    def handle(self, *args, **options):
        offset = 0
        tg_client = TgClient(TG_TOKEN)

        while True:
            response = tg_client.get_updates(offset=offset)
            for item in response.result:
                # check if user exists in TgUser
                tg_user_id = item.message.from_.id
                chat_id = item.message.chat.id
                offset = item.update_id + 1

                if TgUser.objects.filter(tg_user_id=tg_user_id).first():
                    tg_client.send_message(chat_id=chat_id, text='Существует')
                else:
                    TgUser.objects.create(tg_user_id=tg_user_id, tg_chat_id=chat_id)
                    tg_client.send_message(chat_id=chat_id, text='Привет')
