from random import randint

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
        self.tg_user: TgUser
        self.category: Category
        self.goal: Goal

        self.category_mode: bool = False
        self.goal_mode: bool = False
        super().__init__()

    def handle(self, *args, **options):
        while True:
            self._get_response()

            if self.user:
                reply = self._main_logic()
            else:
                reply = self._verify

            self._send_reply(reply=reply)

    def _get_response(self) -> None:
        """Get key data from response"""
        # get key data from response
        self.response = self.tg_client.get_updates(offset=self.offset)

        for item in self.response.result:
            self.offset = item.update_id + 1
            self.chat_id = item.message.chat.id
            self.tg_user_id = item.message.from_.id
            self.message = item.message.text

            self.user = TgUser.objects.filter(
                tg_user_id=self.tg_user_id, user_id__isnull=False
            ).first()

    def _main_logic(self) -> str:
        """Logic for verified user"""
        # key commands
        if self.message == '/cancel':
            self.category_mode = False
            self.goal_mode = False
            reply = f'Операция прервана, введите название задачи'
        elif self.message == '/goals':
            reply = self._goals()
        elif self.message == '/create':
            reply = self._create()

        # logic for goal creation - choose category, create goal
        elif self.category_mode:
            reply = self._choose_category()
        elif self.goal_mode:
            reply = self._create_goal()
        else:
            reply = 'Неизвестная команда'

        return reply

    def _verify(self) -> str:
        """Starting logic"""
        verification_code = randint(10000, 99999)

        self.tg_user = TgUser.objects.filter(tg_user_id=self.tg_user_id).first()
        if not self.tg_user:
            TgUser.objects.create(
                tg_user_id=self.tg_user_id,
                tg_chat_id=self.chat_id,
                verification_code=verification_code
            )
        else:
            self.tg_user.verification_code = verification_code
            self.tg_user.save()

        reply = (f"Подтвердите, пожалуйста, свой аккаунт. "
                 f"Для подтверждения необходимо ввести код: {verification_code} "
                 f"на сайте")
        return reply

    def _goals(self) -> list:
        """Logic for /goals command - choose category"""
        goals = Goal.objects.filter(
            category__board__participants__user=self.user.user, is_deleted=False
        ).all()
        return [f'#{goal.id} {goal.title}' for goal in goals]

    def _create(self) -> list:
        """Logic for /create command - list of categories"""
        categories = Category.objects.filter(
            board__participants__user=self.user.user, is_deleted=False
        ).all()

        self.category_mode = True

        return [f'#{category.id} {category.title}' for category in categories]

    def _choose_category(self) -> str:
        """Logic for /create command - choose category"""

        self.category = Category.objects.filter(
            pk=int(self.message), board__participants__user=self.user.user, is_deleted=False
        ).first()

        if not self.category:
            reply = f'Неверная категория'
        else:
            reply = f'Категория выбрана. Пришлите название задачи'
            self.goal_mode = True
            self.category_mode = False

        return reply

    def _create_goal(self) -> str:
        """Logic for /create command - create goal"""
        self.goal = Goal.objects.create(
            user=self.user.user, title=self.message, category=self.category
        )
        self.goal_mode = False
        return f'Задача "{self.goal.title}" создана'

    def _send_reply(self, reply: str | list) -> None:
        """Send reply"""
        if type(reply) == list:
            for item in reply:
                self.tg_client.send_message(chat_id=self.chat_id, text=item)
        else:
            self.tg_client.send_message(chat_id=self.chat_id, text=reply)
