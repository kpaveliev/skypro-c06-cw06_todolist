from random import randint

from django.core.management import BaseCommand

from todolist.settings import TG_TOKEN
from goals.models import Goal, Category
from bot.tg import TgClient
from bot.models import TgUser


class Command(BaseCommand):
    help = 'Start telegram bot'

    def __init__(self):
        self.category_mode: bool = False
        self.goal_mode: bool = False
        super().__init__()

    def handle(self, *args, **options):
        offset = 0
        tg_client = TgClient(TG_TOKEN)

        while True:
            response = tg_client.get_updates(offset=offset)

            for item in response.result:
                offset = item.update_id + 1

                # get key data
                chat_id = item.message.chat.id
                tg_user_id = item.message.from_.id
                message = item.message.text

                user = TgUser.objects.filter(
                    tg_user_id=tg_user_id, user_id__isnull=False
                ).first()

                # logic for goal creation - chose category
                if message == '/cancel':
                    self.category_mode = False
                    self.goal_mode = False
                    reply = f'Операция прервана, введите название задачи'
                    tg_client.send_message(chat_id=chat_id, text=reply)

                if self.category_mode:
                    category = Category.objects.filter(
                            pk=int(message), board__participants__user=user.user, is_deleted=False
                        ).first()
                    if not category:
                        reply = f'Неверная категория'
                    else:
                        reply = f'Категория выбрана. Пришлите название задачи'
                        self.goal_mode = True
                        self.category_mode = False

                    tg_client.send_message(chat_id=chat_id, text=reply)
                    continue

                # logic for goal creation - type goal
                if self.goal_mode:
                    goal = Goal.objects.create(
                        title=message, category=category
                    )
                    self.goal_mode = False
                    reply = f'Задача "{goal.title}" создана'
                    tg_client.send_message(chat_id=chat_id, text=reply)
                    continue

                # main logic for verified user
                if user:
                    if message == '/goals':
                        goals = Goal.objects.filter(
                            category__board__participants__user=user.user, is_deleted=False
                        ).all()
                        for goal in goals:
                            reply = f'#{goal.id} {goal.title}'
                            tg_client.send_message(chat_id=chat_id, text=reply)
                    if message == '/create':
                        categories = Category.objects.filter(
                            board__participants__user=user.user, is_deleted=False
                        ).all()
                        for category in categories:
                            reply = f'#{category.id} {category.title}'
                            tg_client.send_message(chat_id=chat_id, text=reply)
                        reply = 'Введите номер категории'
                        tg_client.send_message(chat_id=chat_id, text=reply)
                        self.category_mode = True
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

