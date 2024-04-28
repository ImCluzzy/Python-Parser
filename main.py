import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import telebot
import threading

bot = telebot.TeleBot("tg_api")
vk = vk_api.VkApi(token='vk_api')
long = VkBotLongPoll(vk, 'id_group_vk')
channel = "@id_group_tg"


def vk_bot():
    print('Подключение к VK, успешно!')

    for event in long.listen():
        if event.type == VkBotEventType.WALL_POST_NEW:
            print('Новый пост!')

            if event.obj.attachments:
                attachments = event.obj.attachments
                text = event.obj.text if event.obj.text else ""
                send_message_with_attachments_to_telegram(text, attachments)

            elif event.obj.text:
                text = event.obj.text
                send_message(text)

        else:
            print(event.type)
        print()


def send_message(text):
    print("Отправка сообщения в Telegram...")

    bot.send_message(channel, text)


def send_message_with_attachments_to_telegram(text, attachments):
    print("Отправка сообщения и медиа в Telegram...")
    media = []

    for attachment in attachments:
        photo_url = get_largest_photo_url(attachment['photo'])
        photo = telebot.types.InputMediaPhoto(photo_url)
        media.append(photo)
    print('Я тут!')
    for m in media:
        bot.send_photo(channel, m.media, caption=text, parse_mode='HTML')


def get_largest_photo_url(photo):
    sizes = ['w', 'z', 'y', 'x', 'm']
    for size in sizes:
        if size in photo:
            return photo[size]
    return photo['sizes'][-1]['url']


def get_video_url(video):
    video_url = video['player']
    return video_url


def main():
    vk_thread = threading.Thread(target=vk_bot)
    vk_thread.start()

    tg_thread = threading.Thread(target=bot.polling)
    tg_thread.start()

    # Ожидание завершения всех активных потоков перед выходом
    while threading.active_count() > 1:
        pass


if __name__ == '__main__':
    main()
