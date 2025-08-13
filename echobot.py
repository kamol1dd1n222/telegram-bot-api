from time import sleep
import requests
from settings import TOKEN

BASE_URL = f'https://api.telegram.org/bot{TOKEN}'


def get_updates(offset: int | None):
    params = {
        'offset': offset
    }
    getupdates_url = f'{BASE_URL}/getUpdates'
    response = requests.get(getupdates_url, params=params)

    return response.json()["result"]


def send_message(chat_id: int, text: str):
    params = {
        'chat_id': chat_id,
        'text': text
    }

    sendmessage_url = f'{BASE_URL}/sendMessage'
    requests.get(sendmessage_url, params=params)


def send_contact(chat_id: int, first_name: str, phone_number: str):
    params = {
        'chat_id': chat_id,
        'first_name': first_name,
        'phone_number': phone_number,
    }

    sendmessage_url = f'{BASE_URL}/sendContact'
    requests.get(sendmessage_url, params=params)


def send_photo(chat_id: int, photo: str):
    params = {
        'chat_id': chat_id,
        'photo': photo,
    }

    sendmessage_url = f'{BASE_URL}/sendPhoto'
    requests.get(sendmessage_url, params=params)


def updater(token: str):

    offset = None

    while True:

        updates = get_updates(offset)

        for update in updates:
            
            if 'message' in update:
                message = update['message']
                user = update['message']['from']

                if 'text' in message:
                    text = message['text']
                    send_message(user['id'], text)
                elif 'contact' in message:
                    contact = message['contact']
                    send_contact(user['id'], contact['first_name'], contact['phone_number'])
                elif 'photo' in message:
                    photo = message['photo'][0]
                    send_photo(user['id'], photo['file_id'])

            offset = update['update_id'] + 1

        sleep(1)

if __name__ == '__main__':
    updater(TOKEN)
