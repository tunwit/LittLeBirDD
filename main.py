import logsetup #essential
import logging

from discord.ext import commands,tasks
import json
import os
import discord
import wavelink
import random
import spotipy
from spotipy import SpotifyClientCredentials
from delete_schedule import delete
import pylast
from datetime import datetime
from pymongo.mongo_client import MongoClient
import time
import aioschedule
import sys
import asyncio
import itertools
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('littlebirdd')
from config import CONFIG,MODEL,TOKEN,APPLICATION_ID,MONGO,CLIENT_ID,CLIENT_SECRET,LAST_API_KEY,LAST_API_SECRET,LAST_USERNAME,LAST_PASSWORD

DATABASE = [
    "customrandom",
    "deletefile",
    "level",
    "lplaylist",
    "notification",
    "searchstatistic",
    "searchstatistic2",
    "serverstate",
    "toggle",
    "trackvc",
    "Usage_information",
    "welcome",
    "reminder",
    "vip",
    "ban",
    "dev",
    "music_channel"
]


close_by_cooling = False
intents = discord.Intents.all()

final_event = {"priority": 4, "event": None, "file": None, "des": None}


class LittLeBirDD(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            intents=intents,
            command_prefix=CONFIG.get("defualt_prefix"),
            help_command=None,
            application_id=APPLICATION_ID,
        )
        self.model = MODEL
        self.config = CONFIG
        self.mango = MongoClient(MONGO)["Main"]
        self.spotify_client = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
            )
        )
        self.last = pylast.LastFMNetwork(
            api_key=LAST_API_KEY,
            api_secret=LAST_API_SECRET,
            username=LAST_USERNAME,
            password_hash=pylast.md5(LAST_PASSWORD),
        )

    async def access_database(self, file):
        with open(f"database/{file}.json", "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        return data

    async def setup_hook(self):
        # await self.create_db_pool()
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and not filename.startswith("_"):
                await bot.load_extension(f"cogs.{filename[:-3]}")

        await self.tree.sync()


bot = LittLeBirDD()


@tasks.loop()
async def change_ac():
    statuses = [
        "/help|For more infomation",
        "Beta test",
        "Waiting for someone to use",
        f"Now is in 【{len(bot.guilds)}】 servers",
    ]
    statuses.extend(final_event["des"])
    for status in itertools.cycle(statuses):
        activity = discord.Game(name=status)
        await bot.change_presence(status=discord.Status.online, activity=activity)
        await asyncio.sleep(15)


@tasks.loop(seconds=15)
async def change_profile():
    with open(f"holidays.json", "r", encoding="utf-8") as json_file:
        data: dict = json.load(json_file)

    current_date = datetime.now()

    for _class, schedule in data.items():
        for r, event in schedule.items():
            start = datetime.strptime(
                event["start"].format(y=current_date.year), "%Y-%m-%d %H:%M:%S"
            )
            end = datetime.strptime(
                event["end"].format(y=current_date.year), "%Y-%m-%d %H:%M:%S"
            )
            if start <= current_date <= end:
                if event != final_event["event"]:
                    if event["priority"] < final_event["priority"]:
                        logger.info('Changing Avartar')
                        final_event["priority"] = event["priority"]
                        final_event["file"] = event["file"]
                        final_event["event"] = r
                        final_event["des"] = event["des"]
                        if MODEL == "main":
                            with open(f'profile\{final_event["file"]}', "rb") as image:
                                try:
                                    await bot.user.edit(avatar=image.read())
                                except:
                                    pass
                        else:
                            with open(f"profile\default.png", "rb") as image:
                                try:
                                    await bot.user.edit(avatar=image.read())
                                except:
                                    pass

async def node_connect(): 
    node1 = wavelink.Node(uri ='http://n1.ll.darrennathanael.com:2269', password="glasshost1984")
    # node2 = wavelink.Node(uri ='http://lavalink.rudracloud.com:2333', password="RudraCloud.com")
    # node3 = wavelink.Node(uri ='http:/localhost:2333', password="youshallnotpass")
    await wavelink.Pool.connect(client=bot, nodes=[node1])

async def check_database_avaliable():
    for collection in DATABASE:
        alreadyhave = bot.mango.list_collection_names()
        if collection not in alreadyhave:
            bot.mango.create_collection(collection)
            logger.info(f'Create new collaction named "{collection}"')


async def temporary_cooling():
    logger.info("bot closing")
    global close_by_cooling
    close_by_cooling = True
    await bot.close()


@tasks.loop(seconds=10)
async def pending():
    await asyncio.create_task(aioschedule.run_pending())


@bot.event
async def on_ready():
    delete.start()
    change_profile.start()
    change_ac.start()
    await check_database_avaliable()
    await node_connect()
    if bot.config["restart"]:                        
        aioschedule.every().days.at(bot.config["restart_at"]).do(temporary_cooling)
    pending.start()
    logger.info("-------------------------------")
    logger.info(f"{bot.user} is Ready")
    logger.info("-------------------------------")


@bot.event
async def on_wavelink_node_ready(node: wavelink.NodeReadyEventPayload):
    logger.info(f"Wavelink {node.node.identifier} connected")


@bot.command()
async def load(ctx, extension):
    await ctx.message.delete()
    if ctx.author.id != 407176297991634954:
        return
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Extension`{extension}`loaded suscessful!!")


@bot.command()
async def unload(ctx, extension):
    await ctx.message.delete()
    if ctx.author.id != 407176297991634954:
        return
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Extension`{extension}`unloaded suscessful!!", delete_after=5)


@bot.command()
async def reload(ctx, extension):
    await ctx.message.delete()
    if ctx.author.id != 407176297991634954:
        return
    try:
        await bot.unload_extension(f"cogs.{extension}")
        await bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"Extension`{extension}`reloaded suscessful!!", delete_after=5)
    except:
        await bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"Extension`{extension}`load suscessful!!", delete_after=5)


if __name__ == "__main__":
    bot.run(TOKEN,log_level=logging.ERROR)
    if close_by_cooling:
        logger.info("restarting")
        time.sleep(bot.config["restart_duration"])
        os.system("cls")
        os.execv(sys.executable, ["python"] + sys.argv)
