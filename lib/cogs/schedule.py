

import apscheduler
import discord
import textwrap
import sys

from PIL import Image, ImageFont, ImageDraw

import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import datetime
import json

from discord import utils
from discord.utils import get
from discord import channel, Embed
from discord.ext.commands import command, has_permissions, CheckFailure, Cog, Greedy
from typing import Optional
from asyncio import TimeoutError
from ..db import db

class schedule(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        
        sys.setrecursionlimit(10000)



    async def send(self):


     
        db.execute("SELECT * FROM schedules")
        
        schedules = db.records("SELECT * FROM schedules")
        for schedule in schedules:
            self.scheduler.add_job(self.announcment, CronTrigger(day_of_week=schedule[2],hour=schedule[3],minute=schedule[4]), (schedule[0], schedule[1]))



        self.scheduler.start() 

    @command(name="announce", aliases=["an"])
    @has_permissions(manage_messages=True)
    async def announce(self, ctx, member, title,*,description:Optional[str]=" "):
        """Announcment command, role must be able to view #announcments."""
        if not utils.get(ctx.guild.roles, name=member):
            await ctx.send("Specified role was not located, role must be able to view #announcments")
        else:
            embed, file = await self.announcment(title, description, ctx.author.display_name, member, False)
            preview = await ctx.send(file=file,embed=embed)

            details = Embed(
                title="Announcment details",
                description="Tick if you wish to send",
                colour=self.bot.user.colour,
                timestamp=datetime.datetime.now())

            embed.set_footer(text= f"This query will close in 2 minutes.")

            fields = [("Mentioning", f"`@{member}`" , True),
                      ("Title:", f"`{title}`", True),
                      ("Description:", f"`{description}`", True),
                      ("Destination: ", f"`#Announcments`", True)]
            
            for name, value, inLine in fields:
                details.add_field(name=name, value=value, inline=inLine)
            
            sent = await ctx.send(embed=details)

            await sent.add_reaction(u"\u2611")
            await sent.add_reaction(u"\u274C")

            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user==ctx.author and reaction.emoji in [u"\u2611", u"\u274C"], timeout=600)
                if reaction.emoji == u"\u2611":
                    await self.announcment(title, description, ctx.author.display_name, member, True)
                else:
                    await ctx.send("Cancelling query")

                    await sent.delete()
                    await preview.delete()
            
            except TimeoutError:
                await ctx.send("Query timedo out.")

                await sent.delete()
                await preview.delete()






        


    @command(name="schedules")
    async def schedules(self, ctx):

        embed = Embed(
                  title="Schedules",
                  colour=ctx.author.colour,
                  timestamp=datetime.datetime.now())
        
        db.execute("SELECT * FROM schedules")
        
        schedules = db.records("SELECT * FROM schedules")

        days = {"mon" : "monday",
                "tus" : "tuesday",
                "wed" : "wednesday",
                "thur" : "thurseday",
                "fri" : "friday",
                "sat" : "saturday",
                "sun" : "sunday"
                }

        for schedule in schedules:
            embed.add_field(name=f"`{schedule[0]}` - {schedule[1]}", value=f"scheduled for {days[schedule[2]]} at {schedule[3]}:{schedule[4]}", inline=False)
        await ctx.send(embed=embed)


    async def announcment(self, title, description, author=False, role=False, post=False):

        announcmentChannel = 795328151030464512

        img = "./data/images/announcement.png"
        font_path = "./data/fonts/roboto/Roboto-Black.ttf"

        image = Image.open(img)
        draw = ImageDraw.Draw(image)
        
        def fontSize(font_path, font_size):
            font = ImageFont.truetype(font_path, font_size)
            return font
        
        margin = 10
        offset = 140

        descriptionSize = fontSize(font_path, 26)
        titleSize = fontSize(font_path, 36)

        for line in textwrap.wrap(str(description), width=25):
            draw.text((margin, offset), line, font=descriptionSize, fill=(255,255,255))
            offset += descriptionSize.getsize(line)[1]

        draw.text((70,26), title, (255,255,0), font=titleSize)

        
        image.save("text.png")
        file=discord.File("text.png", filename="image.png")
        
        embed = Embed(
                  timestamp=datetime.datetime.now())

        
        embed.set_footer(text= f"Scheduled Announcment" if not author else f'Announcment by: {author}')
        embed.set_image(url="attachment://image.png")

  
        if post:
            if role:
                mention = utils.get(self.bot.get_guild(789865655444439040).roles, name=role)
                await self.bot.get_channel(announcmentChannel).send(f"{mention.mention}")
            await self.bot.get_channel(announcmentChannel).send(file=file, embed=embed)
        else:
            embed.title = "Preview"
            return embed, file
    


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("schedule")

        await self.send()
        



def setup(bot):
    bot.add_cog(schedule(bot))        