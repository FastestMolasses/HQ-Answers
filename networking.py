import re
import json
import aiohttp
import discord
import messageBox

BEARER_TOKEN = ''
URL = 'https://api-quiz.hype.space/shows/now?type='
HEADERS = {
    'Authorization': f'Bearer {BEARER_TOKEN}',
    'x-hq-client': 'Android/1.3.0'
}


async def request(method: str, url: str, headers: dict = None,
                  data: dict = None, stringify: bool = True,
                  username: str=None, password: str=None):
    """
        Asynchronous request that supports authentication and all
        RESTful HTTP calls. Returns back a JSON dict.

        :param method: The HTTP method to use.
        :param url: The URL to send a request to.
        :param headers: The headers for the request.
        :param data: The data to send.
        :param stringify: Whether to stringify the data or not.
        :param username: Username used for authentication.
        :param password: Password usef for authentication.
    """
    # Setup and format data
    auth = None
    if username and password:
        auth = aiohttp.BasicAuth(
            login=username, password=password, encoding='utf-8')
    if data and stringify:
        data = json.dumps(data, sort_keys=False, separators=(',', ':'))

    # Make the request
    async with aiohttp.ClientSession(headers=headers, auth=auth) as session:
        async with session.request(method=method, url=url, data=data, timeout=5) as response:
            try:
                # Return the response in JSON
                d = await response.read()
                return json.loads(d)
            except:
                return {}


async def getBroadcast():
    """
        Returns the broadcast data from HQ. If a game is live,
        it will return a dict of the game show information, otherwise
        it will return None.
    """
    r = await request(method='GET', url=URL)
    return r.get('broadcast')


async def websocketHandler(url: str, channel: discord.TextChannel,
                           resetFunc, messageBox: messageBox.MessageBox):
    """
        Handles websocket connections to HQ. Will retrieve both questions
        and answers during a live HQ game.

        :param url: The url of the socket to connect to.
        :param channel: The discord channel to send messages to.
        :param resetFunc: A callback to reset the answer counters when a new question appears
        :param messageBox: Used to store the discord embed information to display on Discord
    """
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url, headers=HEADERS, heartbeat=5, timeout=30) as ws:
            await channel.send('HQ Trivia game is live!')

            lastQuestion = ''

            # For every message received from the websocket...
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    # Parse data into a dict object
                    message = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', msg.data)
                    messageData = json.loads(message)

                    if messageData.get('error'):
                        await channel.send('Connection settings invalid!')

                    elif messageData.get('type') == 'question':
                        question = messageData.get('question')
                        answers = [i.get('text')
                                   for i in messageData.get('answers')]

                        print('QUESTION: ' + question)
                        print('ANSWERS: ' + str(answers))

                        # If the question has changed, then reset the answer counters
                        if lastQuestion != question:
                            lastQuestion = question
                            resetFunc()
                            # Reset the question embed
                            await messageBox.resetEmbed(channel, question, answers)
