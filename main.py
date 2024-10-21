import time

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel

api_id = 'api_id'
api_hash = 'api_hash'
client = TelegramClient('anon', api_id, api_hash)

channel_username = 'канал'
search_word = 'слово'


async def main():
    client.start()
    entity = client.get_entity(channel_username)

    word_count = 0
    offset_id = 0
    limit = 100

    while True:
        history = client(GetHistoryRequest(
            peer=PeerChannel(entity.id),
            limit=limit,
            offset_date=None,
            offset_id=offset_id,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))

        messages = history.messages

        if not messages:
            break

        for message in messages:
            if hasattr(message, 'message'):
                word_count += message.message.lower().count(search_word.lower())

        offset_id = messages[-1].id
        time.sleep(1)

    client.disconnect()
    print(f'Слово "{search_word}" упоминается {word_count} раз(а) в канале {channel_username}.')


with client:
    client.loop.run_until_complete(main())
