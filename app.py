import vk_api
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from data import find_pokemon
import json

vk_session = vk_api.VkApi(token='a2164ceb7b39703b7667f6c893dc4770b70773aa456799e0fd2abc18582c8b3bd1c94f6f90716fa8ef9fe')


def get_button_text(label, color, payload=''):
    return {
        'action': {
            'type': 'text',
            'payload': json.dumps(payload),
            'label': label
        },
        'color': color
    }


keyboard = {
    'one_time': False,
    'buttons': [
        [
            get_button_text(label='Green', color='positive'),
            get_button_text(label='Red', color='negative')
        ],
        [
            get_button_text(label='Blue', color='primary')
        ]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.text == 'Green' or event.text == 'Red':
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='Positive or Negative',
                keyboard=keyboard
                )
        elif event.text == 'Blue':
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='Primary',
                keyboard=keyboard
            )
