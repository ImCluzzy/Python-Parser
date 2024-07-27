import main
import telebot

def send_message_with_attachments_to_telegram(text, attachments):
    print("Отправка сообщения и медиа в Telegram...")
    media = []
    photo_attachments = []
    for attachment in attachments:
        if attachment['type'] == 'photo':
            photo_attachments.append(attachment['photo'])

    if photo_attachments:
        photo_url = get_largest_photo_url(photo_attachments[0])
        caption = truncate_text(text)
        photo = telebot.types.InputMediaPhoto(media=photo_url, caption=caption, parse_mode='HTML')
        media.append(photo)

        for photo_attachment in photo_attachments[1:]:
            photo_url = get_largest_photo_url(photo_attachment)
            photo = telebot.types.InputMediaPhoto(media=photo_url)
            media.append(photo)

    main.bot.send_media_group(main.tg_channel, media)

def send_message(text):
    print("Отправка сообщения в Telegram...")
    truncated_text = truncate_text(text)
    main.bot.send_message(main.tg_channel, truncated_text)

def get_largest_photo_url(photo):
    sizes = ['w', 'z', 'y', 'x', 'm']
    for size in sizes:
        if size in photo:
            return photo[size]
    return photo['sizes'][-1]['url']

def truncate_text(text, limit=1024):
    return text[:limit] + "..." if len(text) > limit else text
