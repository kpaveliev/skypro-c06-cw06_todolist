from random import randint

from django.core.management import BaseCommand

from todolist.settings import TG_TOKEN
from goals.models import Goal
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
                offset = item.update_id + 1

                chat_id = item.message.chat.id
                tg_user_id = item.message.from_.id
                message = item.message.text

                user = TgUser.objects.filter(
                    tg_user_id=tg_user_id, user_id__isnull=False
                ).first().user()

                # logic for verified user
                if user:
                    if message == '/goals':
                        goals = Goal.objects.filter(user=user).all()
                        for goal in goals:
                            reply = f'#{goal.id} {goal.title}'
                            tg_client.send_message(chat_id=chat_id, text=reply)
                    else:
                        tg_client.send_message(chat_id=chat_id, text='Неизвестная команда')

                # logic for not verified user
                else:
                    verification_code = randint(10000, 99999)
                    tg_user = TgUser.objects.filter(tg_user_id=tg_user_id).first()

                    if not tg_user:
                        TgUser.objects.create(
                            tg_user_id=tg_user_id, tg_chat_id=chat_id, verification_code=verification_code
                        )
                    else:
                        tg_user.verification_code = verification_code
                        tg_user.save()

                    reply = (f"Подтвердите, пожалуйста, свой аккаунт. "
                             f"Для подтверждения необходимо ввести код: {verification_code} "
                             f"на сайте")
                    tg_client.send_message(chat_id=item.message.chat.id, text=reply)

