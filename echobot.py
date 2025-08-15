from time import sleep
import requests
import json
from settings import TOKEN

BASE_URL = f'https://api.telegram.org/bot{TOKEN}'


def get_updates(offset: int | None):
    url = f'{BASE_URL}/getUpdates'
    params = {'offset': offset}
    response = requests.get(url, params=params)
    return response.json().get("result", [])


def send_message(chat_id: int, text: str):
    url = f'{BASE_URL}/sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=data)


def send_photo(chat_id: int, photo: str):
    url = f'{BASE_URL}/sendPhoto'
    data = {'chat_id': chat_id, 'photo': photo}
    requests.post(url, data=data)


def send_voice(chat_id: int, voice: str):
    url = f'{BASE_URL}/sendVoice'
    data = {'chat_id': chat_id, 'voice': voice}
    requests.post(url, data=data)


def send_document(chat_id: int, document: str):
    url = f"{BASE_URL}/sendDocument"
    data = {'chat_id': chat_id, 'document': document}
    requests.post(url, data=data)


def send_audio(chat_id: int, audio: str):
    url = f'{BASE_URL}/sendAudio'
    data = {'chat_id': chat_id, 'audio': audio}
    requests.post(url, data=data)


def send_animation(chat_id: int, animation: str):
    url = f"{BASE_URL}/sendAnimation"
    data = {'chat_id': chat_id, 'animation': animation}
    requests.post(url, data=data)


def send_contact(chat_id: int, phone_number: str, first_name: str, last_name: str = ""):
    url = f"{BASE_URL}/sendContact"
    data = {
        'chat_id': chat_id,
        'phone_number': phone_number,
        'first_name': first_name,
        'last_name': last_name
    }
    requests.post(url, data=data)


def send_video_note(chat_id: int, video_note: str):
    url = f"{BASE_URL}/sendVideoNote"
    data = {'chat_id': chat_id, 'video_note': video_note}
    requests.post(url, data=data)


def send_poll(chat_id: int, question: str, options: list):
    url = f"{BASE_URL}/sendPoll"
    data = {
        'chat_id': chat_id,
        'question': question,
        'options': json.dumps(options) 
    }
    requests.post(url, data=data)


def updater(token: str):
    offset = None

    while True:
        updates = get_updates(offset)

        for update in updates:
            if 'message' in update:
                message = update['message']
                user_id = message['from']['id']

                if 'text' in message:
                    text = message['text']
                    send_message(user_id, text)

                elif 'photo' in message:
                    photo = message['photo'][0]['file_id']
                    send_photo(user_id, photo)

                elif 'voice' in message:
                    voice = message['voice']['file_id']
                    send_voice(user_id, voice)

                elif 'document' in message:
                    document = message['document']['file_id']
                    send_document(user_id, document)

                elif 'audio' in message:
                    audio = message['audio']['file_id']
                    send_audio(user_id, audio)

                elif 'animation' in message:
                    animation = message['animation']['file_id']
                    send_animation(user_id, animation)

                elif 'contact' in message:
                    contact = message['contact']
                    send_contact(
                        user_id,
                        contact['phone_number'],
                        contact['first_name'],
                        contact.get('last_name', "")
                    )

                elif 'video_note' in message:
                    video_note = message['video_note']['file_id']
                    send_video_note(user_id, video_note)

                elif 'poll' in message:
                    poll = message['poll']
                    question = poll['question']
                    options = [opt['text'] for opt in poll['options']]
                    send_poll(user_id, question, options)

            offset = update['update_id'] + 1

        sleep(1)


if __name__ == '__main__':
    updater(TOKEN)
