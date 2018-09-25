# HQ Answers Bot
### Crowdsourced HQ Trivia Discord Bot

Invite this discord bot to your server and it will automatically collect answers from users whenever an HQ game is live. It will display everybody's answers nicely in any channel you specify.

### Installation
```
$ git clone https://github.com/FastestMolasses/HQ-Answers.git
$ cd HQ-Answers
$ pip install -r requirements.txt
$ touch config.py
```

Your `config.py` file should look like this. Enter the relevant information.

```
DISCORD_TOKEN = 'enter your discord bot token'
CHANNEL_ID = 000000 # Should be the channel you want the bot to post in. Leave as int.
```
