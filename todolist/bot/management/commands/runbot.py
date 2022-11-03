from random import randint

from django.core.management import BaseCommand

from todolist.settings import TG_TOKEN
from bot.tg import TgClient
from bot.models import TgUser


class Command(BaseCommand):
    help = 'Start telegram bot'

    def handle(self, *args, **options):
        offset = 0
        tg_client = TgClient(TG_TOKEN)

        while True:
            response = tg_client.get_updates(offset=offset)
            for item in response.result:

                tg_user_id = item.message.from_.id
                chat_id = item.message.chat.id
                offset = item.update_id + 1

                if TgUser.objects.filter(tg_user_id=tg_user_id).first():
                    tg_client.send_message(chat_id=chat_id, text='Существует')

                else:
                    # generate verification code and send it to user
                    verification_code = randint(10000, 99999)
                    TgUser.objects.create(
                        tg_user_id=tg_user_id, tg_chat_id=chat_id, verification_code=verification_code
                    )
                    text = (f"Подтвердите, пожалуйста, свой аккаунт. "
                            f"Для подтверждения необходимо ввести код: {verification_code} "
                            f"на сайте")
                    tg_client.send_message(chat_id=chat_id, text=text)
