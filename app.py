import vk_api
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.upload import VkUpload
import requests
import json
from io import BytesIO
from poki import get_pokemon_data, get_pokemontype_emoji, get_random_pokemon

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


def get_info_pokemon(data_pokemon):
    pokemon_id = data_pokemon['_id']
    pokemon_sprite = 'https://assets.pokemon.com/assets/cms2/img/pokedex/full/{:03}.png'.format(pokemon_id)
    file_img = requests.get(pokemon_sprite).content

    with open('pokemon.png', 'wb') as f:
        f.write(bytearray(file_img))

    upload_server = vk.photos.getMessagesUploadServer()
    photo_req = requests.post(upload_server['upload_url'],
                              files={'photo': open('pokemon.png', 'rb')}).json()
    photo = vk.photos.saveMessagesPhoto(
        photo=photo_req['photo'],
        server=photo_req['server'],
        hash=photo_req['hash']
    )[0]

    pokemon_info_message = f"""
    📌 Уникальный номер: {pokemon_id}
    💬 Имя: {data_pokemon['name'].title()}
    {get_pokemontype_emoji(data_pokemon['pokemonType'][-1])} Тип: {', '.join(data_pokemon.get('pokemonType')).title()}
    📏 Рост: {data_pokemon.get('height') / 10} м
    🗿 Вес: {data_pokemon.get('weight') / 10} кг
                    """

    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message=pokemon_info_message,
        attachment='photo' + str(photo['owner_id']) + '_' + str(photo['id']),
    )


keyboard = {
    'one_time': False,
    'buttons': [
        [
            get_button_text(label='История запросов', color='secondary'),
            get_button_text(label='Испытать удачу', color='primary')
        ]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.text == 'История запросов':
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='🔎 Последнии n запросов 🔎',
                keyboard=keyboard
            )
        elif event.text == 'Испытать удачу':
            data = get_random_pokemon()
            get_info_pokemon(data)
        else:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='🚀 Начинаем искать покемона в нашей базе данных... 🚀',
                keyboard=keyboard
            )
            data = get_pokemon_data(event.text.lower())

            if data != 'Error':
                get_info_pokemon(data)
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='😥Мы не можем найти такого покемона, попробуйте еще раз!😥',
                    keyboard=keyboard
                )
