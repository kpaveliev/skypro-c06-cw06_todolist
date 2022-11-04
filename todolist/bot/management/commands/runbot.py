from random import randint
from typing import Optional

from django.core.management import BaseCommand

from todolist.settings import TG_TOKEN
from goals.models import Goal, Category
from bot.models import TgUser
from bot.tg import TgClient
from bot.tg._dc import GetUpdatesResponse


class Command(BaseCommand):
    help = 'Start telegram bot'

    def __init__(self):
        self.offset = 0
        self.tg_client = TgClient(TG_TOKEN)
        self.response: GetUpdatesResponse
        self.chat_id: int
        self.tg_user_id: int
        self.message: str

        self.user: TgUser
        self.category: Category
        self.goal: Goal

        self.category_mode: bool = False
        self.goal_mode: bool = False
        super().__init__()

    def handle(self, *args, **options):
        while True:
            self.response = self.tg_client.get_updates(offset=self.offset)

            for item in self.response.result:
                self.offset = item.update_id + 1

                # get key data
                self.chat_id = item.message.chat.id
                self.tg_user_id = item.message.from_.id
                self.message = item.message.text

                self.user = TgUser.filter(
                    tg_user_id=self.tg_user_id, user_id__isnull=False
                ).first()

                # logic for goal creation - chose category
                if self.message == '/cancel':
                    self.category_mode = False
                    self.goal_mode = False
                    reply = f'Операция прервана, введите название задачи'
                    self.tg_client.send_message(chat_id=self.chat_id, text=reply)

                if self.category_mode:
                    self.category = Category.objects.filter(
                            pk=int(self.message), board__participants__user=self.user.user, is_deleted=False
                        ).first()
                    if not self.category:
                        reply = f'Неверная категория'
                    else:
                        reply = f'Категория выбрана. Пришлите название задачи'
                        self.goal_mode = True
                        self.category_mode = False

                    self.tg_client.send_message(chat_id=self.chat_id, text=reply)
                    continue

                # logic for goal creation - type goal
                if self.goal_mode:
                    self.goal = Goal.objects.create(
                        user=self.user.user, title=self.message, category=category
                    )
                    self.goal_mode = False
                    reply = f'Задача "{goal.title}" создана'
                    self.tg_client.send_message(chat_id=self.chat_id, text=reply)
                    continue

                # main logic for verified user
                if self.user:
                    if self.message == '/goals':
                        goals = Goal.objects.filter(
                            category__board__participants__user=self.user.user, is_deleted=False
                        ).all()
                        for goal in goals:
                            reply = f'#{goal.id} {goal.title}'
                            self.tg_client.send_message(chat_id=self.chat_id, text=reply)
                    if self.message == '/create':
                        categories = Category.objects.filter(
                            board__participants__user=self.user.user, is_deleted=False
                        ).all()
                        for category in categories:
                            reply = f'#{category.id} {category.title}'
                            self.tg_client.send_message(chat_id=self.chat_id, text=reply)
                        reply = 'Введите номер категории'
                        self.tg_client.send_message(chat_id=self.chat_id, text=reply)
                        self.category_mode = True
                    else:
                        self.tg_client.send_message(chat_id=self.chat_id, text='Неизвестная команда')

                # logic for not verified user
                else:
                    verification_code = randint(10000, 99999)
                    tg_user = TgUser.objects.filter(tg_user_id=self.tg_user_id).first()

                    if not tg_user:
                        TgUser.objects.create(
                            tg_user_id=self.tg_user_id, tg_chat_id=self.chat_id, verification_code=verification_code
                        )
                    else:
                        tg_user.verification_code = verification_code
                        tg_user.save()

                    reply = (f"Подтвердите, пожалуйста, свой аккаунт. "
                             f"Для подтверждения необходимо ввести код: {verification_code} "
                             f"на сайте")
                    self.tg_client.send_message(chat_id=self.chat_id, text=reply)

    def _choose_category(self):
        """Logic for /create command"""
        pass

