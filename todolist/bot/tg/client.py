import requests

from dc import GetUpdatesResponse, SendMessageResponse
# from schemas import GetUpdatesSchema, SendMessageSchema


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

        return GetUpdatesResponse(**response.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        pass


if __name__ == '__main__':
    cl = TgClient('5677342297:AAHOFv46hV1rbRxgNPjQLhkOUSQ6rXvGl-A')
    print(cl.get_updates(offset=0, timeout=5))
