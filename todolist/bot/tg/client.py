import requests

from marshmallow_dataclass import class_schema

from dc import GetUpdatesResponse, SendMessageResponse



class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url = self.get_url('getUpdates')

        params = {
            "offset": offset,
            "timeout": timeout
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        response = requests.get(url=url, headers=headers, params=params)

        GetUpdatesSchema = class_schema(GetUpdatesResponse)

        return GetUpdatesSchema().load(response.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        pass


if __name__ == '__main__':
    cl = TgClient('5677342297:AAHOFv46hV1rbRxgNPjQLhkOUSQ6rXvGl-A')
    print(cl.get_updates(offset=0, timeout=5))
