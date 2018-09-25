import config
import discord
import asyncio
import networking
import messageBox


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        """
            Constructor that initializes background tasks.
        """
        super().__init__(*args, **kwargs)

        # Background tasks
        self.showCheckerBG = self.loop.create_task(self.showChecker())

        # Variables
        self.isGameLive = False
        self.answersCounts = [0, 0, 0]
        self.msgBox = messageBox.MessageBox()

    async def on_ready(self):
        """
            Called when the discord bot logs in.
        """
        print(f'{self.user.name} Logged In!')
        print('--------------------\n')

    async def on_message(self, message: discord.Message):
        """
            Handles all the discord commands.
        """
        # Make sure we don't respond to ourself or messages outside the channel
        # or when there is no active game
        if message.author == self.user or \
                message.channel.id != config.CHANNEL_ID or \
                not self.isGameLive:
            return

        # Make sure to not respond to DM messages
        if isinstance(message.author, discord.User):
            return

        # Prepare relevant variables
        msg = message.content.lower()

        if '1' in msg:
            self.answersCounts[0] += 1
            await self.msgBox.updateEmbedCounters(self.answersCounts)
        elif '2' in msg:
            self.answersCounts[1] += 1
            await self.msgBox.updateEmbedCounters(self.answersCounts)
        elif '3' in msg:
            self.answersCounts[2] += 1
            await self.msgBox.updateEmbedCounters(self.answersCounts)
        else:
            return

        # If the user submitted an answer, delete that message
        await message.delete()

    def resetAnswerCounts(self):
        """
            Resets the answer counters to 0.
        """
        self.answersCounts = [0, 0, 0]

    async def showChecker(self):
        """
            Checks when shows are live and connects to
            their websockets.
        """
        await self.wait_until_ready()

        while not self.is_closed():
            # Check for shows
            broadcast = await networking.getBroadcast()

            # If there is an active show
            if broadcast:
                self.isGameLive = True
                socketUrl = broadcast.get('socketURL')
                channel = self.get_channel(config.CHANNEL_ID)

                # Add the websocket handler to the event loop
                # This web socket will get the questions and answers from HQ
                asyncio.get_event_loop().run_until_complete(
                    networking.websocketHandler(socketUrl,
                                                channel,
                                                self.resetAnswerCounts,
                                                messageBox))
            else:
                self.isGameLive = False
                await asyncio.sleep(60)


if __name__ == '__main__':
    client = MyClient()
    client.run(config.DISCORD_TOKEN)
