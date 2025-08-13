import requests
from settings import TOKEN


BASE_URL = f'https://api.telegram.org/bot{TOKEN}'

params = {
    'chat_id': 6974980318,
    'text': 'Nima gap'
}

sendmessage_url = f'{BASE_URL}/sendMessage'
response = requests.get(sendmessage_url, params=params)
