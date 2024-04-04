import pyperclip
import re
import time
import requests
import json
import keyboard
import class_tkinter
import config


pull = []

auth_keys = {"access_token": '',
             "refresh_token": ''}


class Call:
    @staticmethod
    def get_auth_keys(url):  # функция обновления токенов
        while True:
            result = requests.get(url, headers={"Authorization": f'{config.auth.decode("UTF-8")}'})
            if str(result) == "<Response [200]>":
                dictionary = json.loads(result.text)
                auth_keys["access_token"] = dictionary["access_token"]
                auth_keys["refresh_token"] = dictionary["refresh_token"]
                break
            elif str(result) in config.server_error_codes:
                print(f'{result} Сервис A1 не доступен!')
                time.sleep(10)

    @property
    def copy(self):
        phone = pyperclip.paste()
        try:
            if re.search(r'\D{,50}', phone):
                phone = re.sub('\D{,50}', '', phone)

                if phone[0:2] == "80" and phone[2:4] in config.area_codes:
                    phone = '375' + phone[2:]

                if phone[0:2] == "44" or phone[0:2] in config.area_codes:
                    phone = "375" + phone

                if phone[0:3] != '375':
                    # Не верный формат номера телефона
                    phone = ''

                if phone[0:3] == '375' and len(phone) < 12:
                    # Не верный формат номера телефона
                    phone = ''

                if phone[0:3] == '375' and len(phone) > 12:
                    # Не верный формат номера телефона
                    phone = ''
            else:
                phone = ''
            return phone
        except IndexError:
            pass

    @staticmethod
    def request(phone):
        if phone != '':
            pull.clear()
            pull.append(class_tkinter.Tkinter.loading())
            while True:
                time.sleep(1)
                try:
                    result = requests.post(f'https://vats.a1.by/crm-api/open-api/v1/call/outgoing?'
                                           f'company_id={config.company_id}&source={str(pull[0])}&destination={phone}',
                                           headers={"Authentication": f'{auth_keys["access_token"]}'})
                    if str(result) == "<Response [200]>":
                        break
                    if str(result) == "<Response [429]>":
                        time.sleep(0.5)
                    if str(result) == "<Response [400]>" or "<Response [401]>" or "<Response [403]>" \
                            or "<Response [404]>":
                        Call.get_auth_keys(config.url_update_access_tokens_a1)
                    if str(result) in config.server_error_codes:
                        break
                except requests.exceptions.RequestException:
                    pass
        else:
            pass


def key():
    a = Call()
    keyboard.add_hotkey('Ctrl + Alt', lambda: Call.request(a.copy))
    keyboard.wait('Ctrl + Q')
