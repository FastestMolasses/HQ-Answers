import config
import discord
import asyncio

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
        if message.author == self.user or not message.content.startswith('+'):
            return
        
        # Make sure to not respond to DM messages
        if isinstance(message.author, discord.User):
            return
    
    async def showChecker(self):
        """
            Checks when shows are live and joins all accounts to the game
        """
        await self.wait_until_ready()

        while not self.is_closed():
            try:
                # Check for shows
                broadcast = await hq.getBroadcast()

                # Join accounts if there is a game going on
                if broadcast:
                    await hq.joinGameWithAccounts(broadcast['broadcastId'])
            except Exception as e:
                print('ERROR WHILE GETTING SHOW INFORMATION!')
                print(e)

            await asyncio.sleep(60)

if __name__ == '__main__':
    client = MyClient()
    client.run(config.DISCORD_TOKEN)
