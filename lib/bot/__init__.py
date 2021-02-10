from asyncio import sleep
from datetime import datetime
from glob import glob

import apscheduler
import discord

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed, File, DMChannel
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument,
							  CommandOnCooldown)
from discord.ext.commands import when_mentioned_or, command, has_permissions

from ..db import db
from discord.ext.commands import when_mentioned_or

OWNER_IDS = [300363459797712906]
#COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")] #will return python files from cog folder
COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")] #will return python files from cog folder
IGNOR_EXCEPOPTIONS = (CommandNotFound, BadArgument)


def get_prefix(bot,message):
    PREFIX = db.field("SELECT Prefix FROM guilds Where GuildID = ?", 789865655444439040) #fox will make it not multi server applicable
    return when_mentioned_or(PREFIX)(bot,message)





class ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)
            

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.ready = False
        self.cogs_ready = ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(command_prefix=get_prefix, owner_ids=OWNER_IDS)

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded")
        print("setup completed")

    def run(self, version):
        self.VERSION = version

        print("running setup...")
        self.setup()

        with open("./lib/bot/token", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("running bot")
        super().run(self.TOKEN, reconnect=True)
        print("running bot")
    
    def update(self):
        db.multiexec("INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)", 
                    ((guild.id, ) for guild in self.guilds))
        db.commit()

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)
        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)
            else:
                await ctx.send("I'm not ready to recieve commands, please wait a few seconds.")

    async def on_connect(self):
        print("Bot connecting")
        self.update()

    async def on_disconnected(self):
        print("bot disconected")

    async def print_message(self):
        await self.stdout.send("I am a timed notification")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("something went wrong")

        await self.stdout.send("An error occured")

        raise

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNOR_EXCEPOPTIONS]):
            pass
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("Missing one or more recquired arguments.")

        elif isinstance(exc, ValueError):
            await ctx.send("Values inputed are not valid.")

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"That command is on {str(exc.cooldown.type.split('.')[-1])} cooldown. Try again {exc.retry_after:,.2f} seconds")


        elif hasattr(exc, "original"): #checks for attribute original, raises that
            raise exc.original

            if isinstance(exc.original, Forbidden):
                await ctx.send("I do not have permssion to do that.")


        else: #if not found raises standard exeption
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.ready=True
            self.guild = self.get_guild(303492362498473995)
            self.stdout = self.get_channel(755508987155316876)
            #await bot.change_presence(activity=discord.Game(name=""))


            # self.scheduler.add_job(self.print_message, CronTrigger(day_of_week="sat", hour="18", minute="3"))
            # self.scheduler.start()

            #
            #
            # embed = Embed(title="Side Operation", description="Feel free to come along, but you don't have to, no need to inform HR either! Make sure your mods are up to date.",
            # colour=0x7CFC00, timestamp=datetime.utcnow())
            #
            # fields = [("Time:", "Starts at 7:30 pm (GMT) wednesdays, though come along 15 minutes ealier in order to be ready please.", True)]
            #
            # for name, value, inline in fields:
            #     embed.add_field(name=name,value=value,inline=inline)
            #
            # embed.set_footer(text="BSM")
            # embed.set_author(name="BSM", icon_url=self.guild.icon_url)
            # embed.set_thumbnail(url=self.guild.icon_url)
            # embed.set_image(url="https://cdn.discordapp.com/attachments/720436278495281203/720437251359637564/mainop.jpg")
            #
            # await self.stdout.send(embed=embed)
            # await channel.send(file=File("./data/images/mainop.jpg"))

            print("bot ready")
            while not self.cogs_ready.all_ready():
                await sleep(0.5)
            await self.stdout.send("Now online")
            self.ready = True
            print("bot ready")

        else:
            print("bot reconnected")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
