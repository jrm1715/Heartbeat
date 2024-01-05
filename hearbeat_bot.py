from guilded import ChatMessage
from guilded.ext import commands
from guilded import ChatMessage, User
from guilded.abc import Messageable
import functools
import aiohttp
import asyncio
import guilded
import schedule
import os

# Constants 
API_KEY = os.getenv('TEST_API_KEY')
ANNOUNCEMENT_MESSAGE_1 = 'This is a test message to be sent to channel one'
ANNOUNCEMENT_MESSAGE_2 = 'This is a test message to be sent to channel two'
CHANNEL_ID_1 = '633e93af-d7ee-4be4-9634-9a6da3ecdb05'
CHANNEL_ID_2 = '8f86f53c-9341-4a1d-8475-8f3bb89716e3'
BOT_ID = '58e580ab-a4ba-4d2d-80f3-899266a66006'
USER_ID = 'dKbL9V94'
MESSAGE_CONTENT = 'This is a direct message from a bot'
HISTORY_CHANNEL_ID = 'a4132f77-138b-4dbf-bb61-9e923cffc282'
SERVER_ADMIN = 'dKbL9V94'

# Time configuration
INTERVAL = 12 # Change this value to adjust the interval duration
UNIT = 'hours' # Change this vaulue to specify the time unit ('seconds', 'minutes', 'hours') 


async def schedule_message():
    """
    Asynchronous function to schedule and send announcement messages at regular intervals.
    
    This function runs indefinitely, sleeping for the specified interval duration
    and then sending predefined announcement messages to specific channels.
    """

    while True:
        await asyncio.sleep(get_interval_duration())
        await send_message(ANNOUNCEMENT_MESSAGE_1, CHANNEL_ID_1)
        await send_message(ANNOUNCEMENT_MESSAGE_2, CHANNEL_ID_2)      


def get_interval_duration():
    """
    Calculate the total duration for the sleep interval based on the specified time unit and interval.
    
    Returns:
        int: The total duration for the sleep interval in seconds.
    """
    unit_multipliers = {
        'seconds': 1,
        'minutes': 60,
        'hours' : 3600
    }
    unit_multiplier = unit_multipliers.get(UNIT, 1)
    return INTERVAL * unit_multiplier
    

async def send_message(message, channel_id):
        """
        Sends a message to a specified Guilded channel.

        Parameters:
            channel_id (str): The ID of the channel to send the message to.
            message (str): The content of the message to send.

        Returns:
            None
        """
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }

        data = {'content': message}
        url = f'https://www.guilded.gg/api/v1/channels/{channel_id}/messages'
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url, json=data) as response:
                if response.status == 201:
                    print('Message sent successfully!')
                else:
                    print(f'Error sending message: {await response.text()}')


# Bot commands
bot = commands.Bot(command_prefix='!heart ')


# Gets the last 30 messages from the given channel and post them to the designated channel called 'History'
@bot.command()
async def history(ctx):
    channel_command_rec = ctx.channel.id
    channel_author_id = ctx.author.id

    if channel_command_rec == HISTORY_CHANNEL_ID and channel_author_id == SERVER_ADMIN:
        channel = bot.get_channel(CHANNEL_ID_1)
        message_list = []
        messages = await channel.history(limit=30)
        
        
        for message in messages:                  
            formatted_message = f"{message.author}: {message.content}"
            message_list.append(formatted_message)            

        message_list.reverse()

        final_message = '\n'.join(message_list)
        
        await send_message(final_message, HISTORY_CHANNEL_ID)


@bot.event
async def on_ready():
    print('Bot is ready.')


async def main():
    task1 = schedule_message()
    task2 = bot.start(API_KEY)
    await asyncio.gather(task1, task2)    


if __name__ == '__main__':
    asyncio.run(main())


