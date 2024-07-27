import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import telebot
import threading
import yaml
import os
import jobs

with open("config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)

tg_token = config["tg"]["token"]
tg_channel = "@" + config["tg"]["channel"]
vk_token = config["vk"]["token"]
vk_group_id = config["vk"]["long"]

bot = telebot.TeleBot(tg_token)
vk = vk_api.VkApi(token=vk_token)
vk.http.headers.update({'Connection': 'close'})
vk.http.timeout = 1000
long = VkBotLongPoll(vk, vk_group_id)

def vk_bot():
    print('Подключение к VK, успешно!')
    for event in long.listen():
        if event.type == VkBotEventType.WALL_POST_NEW:
            print('Новый пост!')
            if event.obj.attachments:
                attachments = event.obj.attachments
                text = event.obj.text if event.obj.text else ""
                jobs.telgram.send_message_with_attachments_to_telegram(text, attachments)
            elif event.obj.text:
                text = event.obj.text
                jobs.send_message(text)
        else:
            print(event.type)
        print()

def main():
    vk_thread = threading.Thread(target=vk_bot)
    vk_thread.start()
    tg_thread = threading.Thread(target=bot.polling)
    tg_thread.start()

    while threading.active_count() > 1:
        pass

if __name__ == '__main__':
    main()
