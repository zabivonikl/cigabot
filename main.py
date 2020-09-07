from random import randint

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll

import sqlite3

import requests


class Bot:
    def __init__(self):
        token = ""
        self.session = vk_api.VkApi(token=token, client_secret=token)
        self.api = self.session.get_api()
        self.button = False
        self.category = "дешман"
        self.classic = False
        self.product = 'b'
        self.start_keyboard = {
            "buttons": [
                [{
                    "action": {
                        "type": "text",
                        "label": "Начать"
                    },
                    "color": "positive"
                }]
            ]}
        self.price_keyboard = {
            "buttons": [
                [{
                    "action": {
                        "type": "text",
                        "label": "Дешман"
                    },
                    "color": "negative"
                }],
                [{
                    "action": {
                        "type": "text",
                        "label": "Средний"
                    },
                    "color": "primary"
                }],
                [{
                    "action": {
                        "type": "text",
                        "label": "Элита"
                    },
                    "color": "positive"
                }]
            ]}
        self.main()

    def cigarettes(self, peer_id):
        with sqlite3.connect('database.db') as conn:
            curs = conn.cursor()
            curs.execute(f'''SELECT name, link FROM Cigarettes WHERE 
            (Class, Button) = ("{self.category}", "{self.button}")''')
            data = curs.fetchall()
        if data:
            item = data[randint(0, len(data) - 1)]
            answer = item[0]
            if item[1]:
                self.api.messages.send(peer_id=peer_id,
                                       random_id=randint(0, 1024),
                                       message=answer,
                                       attachment=item[1],
                                       keyboard=str(self.start_keyboard).replace("'", '"').replace('True', 'true'))
            else:
                self.api.messages.send(peer_id=peer_id,
                                       random_id=randint(0, 1024),
                                       message=answer,
                                       keyboard=str(self.start_keyboard).replace("'", '"').replace('True', 'true'))
        else:
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 1024),
                                   message='Сигарет с такими параметрами ещё не добавили',
                                   keyboard=str(self.start_keyboard).replace("'", '"').replace('True', 'true'))
        self.product = ''

    def beer(self, peer_id):
        with sqlite3.connect('database.db') as conn:
            curs = conn.cursor()
            curs.execute(f'''SELECT Name, Link FROM Beer WHERE 
            (Class, Classic) = ("{self.category}", "{self.classic}")''')
            data = curs.fetchall()
        if data:
            item = data[randint(0, len(data) - 1)]
            answer = item[0]
            if item[1]:
                self.api.messages.send(peer_id=peer_id,
                                       random_id=randint(0, 1024),
                                       message=answer,
                                       attachment=item[1],
                                       keyboard=str(self.start_keyboard).replace("'", '"').replace('True', 'true'))
            else:
                self.api.messages.send(peer_id=peer_id,
                                       random_id=randint(0, 1024),
                                       message=answer,
                                       keyboard=str(self.start_keyboard).replace("'", '"').replace('True', 'true'))
        else:
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 1024),
                                   message="Пиво с такими параметрами ещё не добавили",
                                   keyboard=str(self.start_keyboard).replace("'", '"').replace('True', 'true'))
        self.product = ''

    def energy_drinks(self, peer_id):
        with sqlite3.connect('database.db') as conn:
            curs = conn.cursor()
            curs.execute(f'''SELECT Name, Link FROM Energy WHERE Class = "{self.category}"''')
            data = curs.fetchall()
        if data:
            item = data[randint(0, len(data) - 1)]
            answer = item[0]
            if item[1]:
                self.api.messages.send(peer_id=peer_id,
                                       random_id=randint(0, 1024),
                                       message=answer,
                                       attachment=item[1],
                                       keyboard=str(self.start_keyboard).replace("'", '"').replace('True', 'true'))
            else:
                self.api.messages.send(peer_id=peer_id,
                                       random_id=randint(0, 1024),
                                       message=answer,
                                       keyboard=str(self.start_keyboard).replace("'", '"').replace('True', 'true'))
        else:
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 1024),
                                   message="Энергетиков с такими параметрами ещё не добавили",
                                   keyboard=str(self.start_keyboard).replace("'", '"').replace('True', 'true'))
        self.product = ''

    def main(self):
        while True:
            try:
                for event in VkBotLongPoll(self.session, 198484474).listen():
                    peer_id = event.object['message']['peer_id']
                    text = event.object['message']['text'].lower().split(' ')
                    if any(i in ['начать'] for i in text):
                        keyboard = {
                                    "buttons": [
                                        [{
                                            "action": {
                                                "type": "text",
                                                "label": "Сигареты"
                                            },
                                            "color": "positive"
                                        }],
                                        [{
                                            "action": {
                                                "type": "text",
                                                "label": "Пиво"
                                            },
                                            "color": "positive"
                                        }],
                                        [{
                                            "action": {
                                                "type": "text",
                                                "label": "Энергетики"
                                            },
                                            "color": "positive"
                                        }]
                                    ]}
                        self.api.messages.send(peer_id=peer_id,
                                               random_id=randint(0, 1024),
                                               message='Добро пожаловать в выбиралку. '
                                                       'Выберите интересующую вас продукцию.',
                                               keyboard=str(keyboard).replace("'", '"').replace('True', 'true'))
                    elif any(i in ['сигареты'] for i in text):
                        self.product = 'cigarettes'
                        keyboard = {
                            "buttons": [
                                [{
                                    "action": {
                                        "type": "text",
                                        "label": "С кнопкой"
                                    },
                                    "color": "primary"
                                }],
                                [{
                                    "action": {
                                        "type": "text",
                                        "label": "Без кнопки"
                                    },
                                    "color": "primary"
                                }],
                            ]}
                        self.api.messages.send(peer_id=peer_id,
                                               random_id=randint(0, 1024),
                                               message='Выберите тип',
                                               keyboard=str(keyboard).replace("'", '"').replace('True', 'true'))
                    elif any(i in ['кнопкой'] for i in text):
                        self.button = 1
                        self.api.messages.send(peer_id=peer_id,
                                               random_id=randint(0, 1024),
                                               message='Выберите класс',
                                               keyboard=str(self.price_keyboard).replace("'", '"')
                                               .replace('True', 'true'))
                    elif any(i in ['энергетики'] for i in text):
                        self.product = 'energy_drinks'
                        self.api.messages.send(peer_id=peer_id,
                                               random_id=randint(0, 1024),
                                               message='Выберите класс',
                                               keyboard=str(self.price_keyboard).replace("'", '"')
                                               .replace('True', 'true'))
                    elif any(i in ['кнопки'] for i in text):
                        self.button = 0
                        self.api.messages.send(peer_id=peer_id,
                                               random_id=randint(0, 1024),
                                               message='Выберите класс',
                                               keyboard=str(self.price_keyboard).replace("'", '"')
                                               .replace('True', 'true'))
                    elif any(i in ['пиво'] for i in text):
                        self.product = 'beer'
                        self.classic = 0
                        keyboard = {
                            "buttons": [
                                [{
                                    "action": {
                                        "type": "text",
                                        "label": "Классическое"
                                    },
                                    "color": "primary"
                                }],
                                [{
                                    "action": {
                                        "type": "text",
                                        "label": "Вкусовое"
                                    },
                                    "color": "primary"
                                }]
                            ]}
                        self.api.messages.send(peer_id=peer_id,
                                               random_id=randint(0, 1024),
                                               message='Выберите тип',
                                               keyboard=str(keyboard).replace("'", '"').replace('True', 'true'))
                    elif any(i in ['классическое'] for i in text):
                        self.classic = 1
                        self.api.messages.send(peer_id=peer_id,
                                               random_id=randint(0, 1024),
                                               message='Выберите класс',
                                               keyboard=str(self.price_keyboard).replace("'", '"')
                                               .replace('True', 'true'))
                    elif any(i in ['вкусовое'] for i in text):
                        self.classic = 0
                        self.api.messages.send(peer_id=peer_id,
                                               random_id=randint(0, 1024),
                                               message='Выберите класс',
                                               keyboard=str(self.price_keyboard).replace("'", '"')
                                               .replace('True', 'true'))
                    elif any(i in ['дешман'] for i in text):
                        self.category = 'Дешман'
                        if self.product == 'cigarettes':
                            self.cigarettes(peer_id)
                        elif self.product == 'beer':
                            self.beer(peer_id)
                        elif self.product == 'energy_drinks':
                            self.energy_drinks(peer_id)
                    elif any(i in ['средний'] for i in text):
                        self.category = 'Средний'
                        if self.product == 'cigarettes':
                            self.cigarettes(peer_id)
                        elif self.product == 'beer':
                            self.beer(peer_id)
                        elif self.product == 'energy_drinks':
                            self.energy_drinks(peer_id)
                    elif any(i in ['элита'] for i in text):
                        self.category = 'Элита'
                        if self.product == 'cigarettes':
                            self.cigarettes(peer_id)
                        elif self.product == 'beer':
                            self.beer(peer_id)
                        elif self.product == 'energy_drinks':
                            self.energy_drinks(peer_id)
            except KeyError:
                pass
            except requests.exceptions.ReadTimeout as error:
                self.api.messages.send(peer_id=447828812,
                                       random_id=randint(0, 1024),
                                       message=error)


if __name__ == "__main__":
    Bot()
