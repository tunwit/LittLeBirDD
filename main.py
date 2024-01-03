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
import subprocess


# os.system("start cmd /k java -jar lavalink.jar")
with open("_config.json", "r") as f:
    config = json.load(f)

MODEL = config["model"]  # test for LittlePonYY | main for LittLeBirDD

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
]


close_by_cooling = False
intents = discord.Intents.all()

final_event = {"priority": 4, "event": None, "file": None, "des": None}


class LittLeBirDD(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            intents=intents,
            command_prefix=config[MODEL].get("defualt_prefix"),
            help_command=None,
            application_id=config[MODEL].get("application_id"),
        )
        self.model = MODEL
        self.config = config[MODEL]
        self.mango = MongoClient(self.config.get("mango"))["Main"]
        self.spotify_client = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=self.config.get("client_id"),
                client_secret=self.config.get("client_secret"),
            )
        )
        self.last = pylast.LastFMNetwork(
            api_key=self.config.get("last_api_key"),
            api_secret=self.config.get("last_api_secret"),
            username=self.config.get("last_username"),
            password_hash=pylast.md5(self.config.get("last_password")),
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
                        print("Changing Avartar")
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


# async def node_connect():
#     await wavelink.NodePool.create_node(bot=bot,host=config.get("host"),
#                                         port=config.get("port"),
#                                         password=config.get("password"),
#                                         https=config.get("https"),
#                                         spotify_client=spotify.SpotifyClient(client_id=config.get("client_id"),
#                                         client_secret=config.get("client_secret")))


async def node_connect():
    node = wavelink.Node(uri="http://localhost:2333", password="youshallnotpass")
    await wavelink.Pool.connect(client=bot, nodes=[node])


async def check_database_avaliable():
    for collection in DATABASE:
        alreadyhave = bot.mango.list_collection_names()
        if collection not in alreadyhave:
            bot.mango.create_collection(collection)
            print(f'Create new collaction named "{collection}"')


async def temporary_cooling():
    print("bot closing")
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
    aioschedule.every().days.at(bot.config["restart_at"]).do(temporary_cooling)
    pending.start()
    print("-------------------------------")
    print(f"{bot.user} is Ready")
    print("-------------------------------")


@bot.event
async def on_wavelink_node_ready(node: wavelink.NodeReadyEventPayload):
    print(f"Wavelink {node.node.identifier} connected")


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
    bot.run(bot.config["token"])
    if close_by_cooling:
        print("restarting")
        time.sleep(bot.config["restart_duration"])
        os.system("cls")
        os.execv(sys.executable, ["python"] + sys.argv)
