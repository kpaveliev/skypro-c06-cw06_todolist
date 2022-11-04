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
        print(TG_TOKEN)

        while True:
            response = tg_client.get_updates(offset=offset)
            for item in response.result:
                offset = item.update_id + 1

                user = TgUser.objects.filter(tg_user_id=item.message.from_.id,  user_id__isnull=False).first()
                if user:
                    if item.message.text == '/goals':
                        goals = self._get_goals(user.user)
                        tg_client.send_message(chat_id=item.message.chat.id, text=goals)
                    else:
                        tg_client.send_message(chat_id=item.message.chat.id, text='Неизвестная команда')
                elif TgUser.objects.filter(tg_user_id=item.message.from_.id).first():
                    tg_client.send_message(chat_id=item.message.chat.id, text='Существует')

                else:
                    verification_code = self._create_object(item.message.chat.id, item.message.from_.id)
                    text = (f"Подтвердите, пожалуйста, свой аккаунт. "
                            f"Для подтверждения необходимо ввести код: {verification_code} "
                            f"на сайте")
                    tg_client.send_message(chat_id=item.message.chat.id, text=text)

    @staticmethod
    def _create_object(chat_id, tg_user_id) -> int:
        """Generate verification code and create user"""
        verification_code = randint(10000, 99999)
        TgUser.objects.create(
            tg_user_id=tg_user_id, tg_chat_id=chat_id, verification_code=verification_code
        )
        return verification_code

    @staticmethod
    def _get_goals(user) -> str:
        """Get list of user goals"""
        goal_objects = Goal.objects.filter(user=user).all()
        goals = '\n'.join([goal.title for goal in goal_objects])
        return goals
