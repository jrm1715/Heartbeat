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

# Announcement Messages. Add more messages here
ANNOUNCEMENT_MESSAGE_1 = 'This is a test message to be sent to channel one'
ANNOUNCEMENT_MESSAGE_2 = 'This is a test message to be sent to channel two'
ANNOUNCEMENT_MESSAGE_3 = 'Channel 3 test meessage'

#Channel IDs. Add more channel IDs here
CHANNEL_ID_1 = '633e93af-d7ee-4be4-9634-9a6da3ecdb05'
CHANNEL_ID_2 = '8f86f53c-9341-4a1d-8475-8f3bb89716e3'
CHANNEL_ID_3 = 'ab99fdde-d575-4de6-9f83-86d8e762adb7'

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
        await send_message(ANNOUNCEMENT_MESSAGE_3, CHANNEL_ID_3)     


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


# Bot command prefix
bot = commands.Bot(command_prefix='!heart ')


# Gets the last 30 messages from the channel the command was received and posts them into that same channel
@bot.command()
async def history(ctx):
    channel_command_rec = ctx.channel.id
    channel_author_id = ctx.author.id
    
    channel = bot.get_channel(channel_command_rec)
    message_list = []
    messages = await channel.history(limit=30)        
        
    for message in messages:                  
        formatted_message = f"{message.author}: {message.content}"
        if (message.author.id != "dz01zWpA"):
            message_list.append(formatted_message)

    message_list.reverse()

    final_message = '\n'.join(message_list)    
    
    await send_message(final_message, channel_command_rec)


@bot.event
async def on_ready():
    print('Bot is ready.')


async def main():
    task1 = schedule_message()
    task2 = bot.start(API_KEY)
    await asyncio.gather(task1, task2)    


if __name__ == '__main__':
    asyncio.run(main())


