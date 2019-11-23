import vk_api
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.upload import VkUpload
import requests
import json
from io import BytesIO
from poki import get_pokemon_data

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
            get_button_text(label='История запросов', color='secondary')
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
                message='🔎Последнии n запросов🔎',
                keyboard=keyboard
            )
        else:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='🚀Начинаем искать покемона в нашей базе данных...🚀'
            )
            data = get_pokemon_data(event.text.lower())
            
            if data != 'Error':
                pokemon_id = data['_id']
                pokemon_sprite = 'https://assets.pokemon.com/assets/cms2/img/pokedex/full/{:03}.png'.format(pokemon_id)
                file_img = requests.get(pokemon_sprite).content
                
                with open('pokemon.png', 'wb') as f:
                    f.write(bytearray(file_img))

                upload_server = vk.photos.getMessagesUploadServer()
                photo_req = requests.post(upload_server['upload_url'], files={'photo': open('pokemon.png', 'rb')}).json()
                photo = vk.photos.saveMessagesPhoto(
                    photo=photo_req['photo'],
                    server=photo_req['server'],
                    hash=photo_req['hash']
                )[0]
                vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='Фото:',
                attachment='photo'+str(photo['owner_id'])+'_'+str(photo['id'])
                )
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message=f'''💫Мы нашли покемона с этим именем/номером!💫
                                {pokemon_id} - {data.get('name').title()}
                                Type - {data.get('pokemonType')[0].title()}
                                Average Height - {data.get('height') / 10} m
                                Average Weight - {data.get('weight') / 10} kg
                                
                            ''',
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='😥Мы не можем найти такого покемона, попробуйте еще раз!😥'
                )
