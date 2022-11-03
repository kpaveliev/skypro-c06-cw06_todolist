from django.core.management import BaseCommand

from bot.tg import TgClient

from todolist.settings import TG_TOKEN


class Command(BaseCommand):
    help = 'Start telegram bot'

    def handle(self, *args, **options):
        offset = 0
        tg_client = TgClient(TG_TOKEN)

        while True:
            response = tg_client.get_updates(offset=offset)
            for item in response.result:
                offset = item.update_id + 1
                print(item.message)