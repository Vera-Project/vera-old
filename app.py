import discord
import asyncio
import logging
import coloredlogs
import json
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from chatterbot import comparisons
from chatterbot import response_selection
from discord_webhook import DiscordWebhook,DiscordEmbed
import random,os, requests, shutil,time
import string
import filetype
import urllib.request
import db_module
import sqlite3

chatbot = ChatBot(
    name='Vera',
    logic_adapters=[

        {
            'import_path': 'chatterbot.logic.BestMatch',
            'statement_comparison_function': 'comparisons.levenshtein_distance',
            'response_selection_method': response_selection.get_most_frequent_response
        }
    ],
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.db')
logger = logging.getLogger(__name__)
fmt = ("%(asctime)s - %(message)s")
coloredlogs.install(fmt=fmt, logger=logger)
f = open("settings.json","r")
settings = json.load(f)
token = settings['token']
webhook_url = settings['webhook']
status = settings['status']
prefix = settings['prefix']
class VeraBot(discord.Client):
    async def webhook_online(self):

        servers_serving = ""
        amt_server = 0
        for s in self.guilds:
            servers_serving = servers_serving+"\n"+s.name
            amt_server += 1
        try:
            webhook = DiscordWebhook(webhook)
            embed = DiscordEmbed(title=f'Vera Online Running On:  {str(amt_server)} Server(s)\nRunning As: {str(self.user)}', description=f'Using Key: {l_key}\nServing Server(s):\n{str(servers_serving)}\n', color=242424)
            webhook.add_embed(embed)
            response = webhook.execute()
        except:
            logger.info(f"Error in inital webhook")

    async def on_ready(self):
        if settings['status'] != "":
            await self.change_presence(activity=discord.Game(name=str(status)))
        await self.webhook_online()
        logger.info(f"{self.user} is now online.")

    async def StringGen(stringLength=8):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    def downloadFile(self, url, path):
        try:
            letters = string.ascii_lowercase
            path = path+''.join(random.choice(letters) for i in range(8))
            r = requests.get(url)
            if r.status_code == 200:
                kind = filetype.guess(r.content)
                path = path+"."+kind.extension
                with open(path, 'wb') as f:
                    f.write(r.content)
        except Exception as e:
            logger.critical(f"Error: {e}")



    def getImage(self,filelocation):
        file = random.choice([x for x in os.listdir(filelocation) if os.path.isfile(os.path.join(filelocation, x))])
        return filelocation + file

    async def on_message(self,message):

        #Ignore the bypass variable, it was from a old whitelist that is not included.
        bypass = "true"
        if message.author == self.user:
            return
        if bypass == "false":
             if settings['channel_name'] in message.channel.name:
                if res:
                    pass
                else:
                    msg = discord.Embed(title=f"Unauthorised Use Of Vera",description=f"This Server Has Not Been Added To The Vera Whitelist. Please Contact Staff On The Vera Discord Server (discord.gg/EqHwKUb) If You Believe This Was A Mistake.",color=16711680)
                    await message.channel.send(embed=msg)
                    return
        else:
            pass


        if message.guild == None or settings['channel_name'] in message.channel.name:
            if message.content == settings['prefix']+"quit" and message.author.id in settings['admin']:
                logger.info("Exiting")
                self.loop.stop()
                await self.logout()

                exit()
            else:
                if message.content == "" and message.attachments == True or len(message.attachments) > 0:
                    await message.channel.trigger_typing()
                    image = self.getImage(f"images/")
                    for file in message.attachments:
                        self.downloadFile(file.url, './images/')

                    await message.channel.send(file=discord.File(image))
                else:
                    logger.info(f"Input: {message.content}")
                    await message.channel.trigger_typing()
                    num = random.randint(1,20)
                    if num == 10:
                        image = self.getImage("images/")
                        await message.channel.send(file=discord.File(image))
                    else:
                        if message.content != "":
                            res = chatbot.get_response(message.content)
                            while "discord.gg" or "@everyone" in res:
                                res = chatbot.get_response(message.content)
                            db_module.add_chatlog(message,res)
                            try:
                                await message.channel.send(str(res))
                                logger.info(f"Output: {res}")
                            except discord.errors.HTTPException as l:
                                logger.info(f"Error, {str(l)}")
                        else:
                            logger.info(f"Passed blank message")



listTrainer = ListTrainer(chatbot)
corpTrainer = ChatterBotCorpusTrainer(chatbot)
bot = VeraBot()
bot.run(token)
