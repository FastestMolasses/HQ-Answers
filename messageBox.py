import discord


class MessageBox:
    def __init__(self):
        self.embed = discord.Embed(title='HQ Crowdsourced Answers')
        self.discordMsg = None  # Stores the discord message object, so we can edit the msg

    async def resetEmbed(self, channel: discord.TextChannel, question: str, answers: list):
        """
            Recreates the discord embed with the updated
            information. Will also automatically send the
            embed to the channel.

            :param channel: The discord channel to send the embed to.
            :param question: The trivia question being asked
            :param answers: A list of all the potential answers to the question
        """
        # If we have an existing message, delete it before posting the new one
        # if self.discordMsg:
        #     await self.discordMsg.delete()

        self.embed = self.createEmbed(question, answers, [0, 0, 0])
        self.question = question
        self.answers = answers
        self.discordMsg = await channel.send(embed=self.embed)

    async def updateEmbedCounters(self, counts: list):
        """
            Updates the discord embed with the new data.

            :param counts: A list of all the answer counts to each question
        """
        if not self.discordMsg:
            return

        self.embed = self.createEmbed(self.question, self.answers, counts)
        # Edit the discord message to the new embed
        await self.discordMsg.edit(embed=self.embed)

    def createEmbed(self, question: list, answers: list, counts: list):
        """
            Creates a discord embed object.

            :param: The question to be displayed.
            :parma: The list of potential answers
        """
        embed = discord.Embed(title=question, color=0x4286F4)
        # embed.add_field(name='Question', value=question, inline=False)

        for i in range(min((len(answers), len(counts)))):
            embed.add_field(name=answers[i], value=counts[i], inline=False)

        embed.set_footer(text='Made by FMolasses')
        return embed
