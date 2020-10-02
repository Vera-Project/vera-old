![](https://cdn.discordapp.com/attachments/699596234104504450/700653694865113098/banner.png)
# Info

Vera is an AI powered discord chatbot that uses the Chatterbot framework to learn to speak.

He will reply to all messages in a specified channel and learn from everything said to him.

# Setup

Vera runs on python3.8 and has several required modules to function `discord, coloredlogs, chatterbot, discord_webhook, filetype`

These can all be installed with `pip install -r requirements.txt`

### steps

 1. Install python 3 or later `Python 3.8 reccomended`
 2. install dependencies by navigating to the vera folder and running the command `pip install -r requirements.txt`
 3. Add your settings to the config file

	 `settings.json` options

	**token**: The token for your discord bot, you can create a bot [here](https://discord.com/developers/applications)
	**webhook**: The webhook you want Vera to send updates to (when he comes online)
	**status**: The discord status you want Vera to display
	**channel**: The name of the channel you want Vera to speak in.
	**prefix**: The character you want to prefix commands
	**admin**: The Discord user id of the owner of the bot, vera will only react to some commands if they are issued by the right person.

4. Run Vera `python3 app.py`

# The database

Vera will create a `.db` file on first boot named `database.db`, This is where Veras AI model is stored.

An existing database can be used just by copying it to the Vera directory and making sure it is called `database.db`.

Our pre-trained model is available on [our discord server.](https://discord.gg/jeXnXqH)

# Image support

To make Vera a more successful shitposter we added support for vera to randomly chose an image to send if one is sent to him, he also has a random chance of sending an image in response to a message.

# Support us

Currently we are not accepting donations but we would love if you could come hang out in [our Discord server](https://discord.com/invite/AJkQAUm).
