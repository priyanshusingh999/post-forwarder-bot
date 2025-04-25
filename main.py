import requests
import time

# Load configuration from YAML file
config = {
    'bot_token': '8090023526:AAGMreA8iwhBZdcEk7Ho-beEeY5AQSSSjb4',
    'channel_ids': ['-1001997278322', '-1001990702629', '-1002021684427', '-1001802412197', '-1001992332883', '-1001827229996', '-1001715214476', '-1001883240370', '-1001731540969', '-1001616444194'],
    'owner_id': '2133811513'
}

BOT_TOKEN = config['bot_token']
CHANNEL_IDS = config['channel_ids']
OWNER_ID = config['owner_id']

# Function to get updates from the bot
def get_updates(offset=None):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
    params = {'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

# Function to send a message to the channel
def send_message(chat_id, text, reply_markup=None):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    params = {'chat_id': chat_id, 'text': text}
    if reply_markup:
        params['reply_markup'] = reply_markup
    requests.post(url, json=params)  # Use json to send the reply_markup as a JSON object

# Function to send a photo to the channel with an optional caption
def send_photo(chat_id, photo_id, caption=None):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    params = {'chat_id': chat_id, 'photo': photo_id}
    if caption:
        params['caption'] = caption
    requests.post(url, params=params)

# Function to send a video to the channel with an optional caption
def send_video(chat_id, video_id, caption=None):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendVideo'
    params = {'chat_id': chat_id, 'video': video_id}
    if caption:
        params['caption'] = caption
    requests.post(url, params=params)

# Function to handle incoming messages
def handle_message(message):
    chat_id = message['chat']['id']

    # Check if the user is the owner
    if str(chat_id) != OWNER_ID:
        first_name = message['chat'].get('first_name', '')
        last_name = message['chat'].get('last_name', '')
        rst_message = f"Welcome, {first_name} {last_name}! This Bot will Forward your Messages to Multiple Channels.\n \nYou are not authorized to use this bot. Please contact the owner."
        inline_keyboard = {
            "inline_keyboard": [
                [
                {"text": "Contact Owner", "url": "https://t.me/r_ajput999"}  # Add a
            ]
            ]
        }
        send_message(chat_id, rst_message, reply_markup=inline_keyboard)
        return

    # Check if the message is a command
    if 'text' in message:
        text = message['text']

        # Handle the /start command
        if text == '/start':
            first_name = message['chat'].get('first_name', '')
            last_name = message['chat'].get('last_name', '')
            welcome_message = f"Welcome, {first_name} {last_name}! This bot will forward your messages to multiple channels."

            # Create inline keyboard markup
            inline_keyboard = {
        "inline_keyboard": [
            [
                {"text": "JOIN CHANNEL", "url": "https://t.me/devx_coder"},
                {"text": "DEVELOPER", "url": "https://replit.com/@priyanshu999"}
            ],
            [
                {"text": "Git Hub", "url": "https://github.com/priyanshusingh999"}
                ]
        ]
    }

            send_message(chat_id, welcome_message, reply_markup=inline_keyboard)
            return  # Exit after sending the welcome message

        # Forward text messages to all channels
        for channel_id in CHANNEL_IDS:
            send_message(channel_id, text)

    # Check if the message contains a photo
    elif 'photo' in message:
        # Get the highest resolution photo
        photo_id = message['photo'][-1]['file_id']
        caption = message.get('caption', None)  # Get the caption if it exists

        # Forward photo to all channels
        for channel_id in CHANNEL_IDS:
            send_photo(channel_id, photo_id, caption)

    # Check if the message contains a video
    elif 'video' in message:
        # Get the video ID
        video_id = message['video']['file_id']
        caption = message.get('caption', None)  # Get the caption if it exists

        # Forward video to all channels
        for channel_id in CHANNEL_IDS:
            send_video(channel_id, video_id, caption)

def main():
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates['result']:
            if 'message' in update:
                handle_message(update['message'])
                # Update the offset to the latest update
                offset = update['update_id'] + 1

        time.sleep(1)  # Sleep for a second before checking for new updates

if __name__ == '__main__':
    main()
