import config
import discord
import asyncio
import networking


class MyClient(discord.Client):
    async def on_ready(self):
        """
            Called when the discord bot logs in
        """
        print(f'{self.user.name} Logged In!')
        print('--------------------\n')

    async def on_message(self, message: discord.Message):
        """
            Handles all the discord commands
        """
        # Make sure we don't respond to ourself or non-commands
        if message.author == self.user or not message.content.startswith('-'):
            return

        # Make sure to not respond to DM messages
        if isinstance(message.author, discord.User):
            return

        # Prepare relevant variables
        msg = message.content.lower()
        msgChannel = message.channel

        if msg == '':
            pass
        elif msg == '':
            pass

    async def showChecker(self):
        """
            Checks when shows are live and joins all accounts to the game
        """
        await self.wait_until_ready()

        while not self.is_closed():
            # Check for shows
            broadcast = await networking.getBroadcast()

            # If there is an active show
            if broadcast:
                socketUrl = broadcast['broadcast'].get('socketURL')
                channel = self.get_channel(config.CHANNEL_ID)

                # Add the websocket handler to the event loop
                # This web socket will get the questions and answers from HQ
                asyncio.get_event_loop().run_until_complete(
                    networking.websocketHandler(socketUrl, channel))
            else:
                await asyncio.sleep(60)


if __name__ == '__main__':
    client = MyClient()
    client.run(config.DISCORD_TOKEN)
