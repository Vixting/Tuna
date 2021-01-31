from discord.ext.commands import Cog
from discord.ext.commands import command, cooldown, BucketType
from discord import Member,Embed


from discord import HTTPException
from discord.ext.commands import BadArgument

from aiohttp import request
from typing import Optional
from random import choice, randint

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["hi"], hidden=True)
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello','Hi','Hey'))} {ctx.author.mention}!")

    #@command(name="dice", aliases=["roll"])
    #async def roll_dice(self, ctx, die_string: str):
    #    dice, value = (int(term) for term in  die_string.split("d"))
    #    if dice <= 100:
    #        rolls = [randint(1, value) for i in range(dice)]
    #        await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")
    #    else:
    #        await ctx.send("Too many dice, limit: input <= 100.")

    # @roll_dice.error
    # async def roll_dice_error(self, ctx, exc):
    #     if isinstance(exc.original, HTTPExcption):
    #         await ctx.send("Result too many characters, please try a lower number")

    # @command(name="slap", aliases=["hit"])
    # @cooldown(1, 60, BucketType.user)
    # async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "no reason"):
    #     await ctx.send(f"{ctx.author.display_name} slapped {member.mention} for {reason}")
    

    # @slap_member.error
    # async def slap_member_error(self, ctx, exc):
    #     if isinstance(exc, BadArgument):
    #         await ctx.send("I cannot find that member.")

    #Removed cause useless
    # @command(name="echo", aliases=["say"])
    # async def echo(self, ctx, *, message):
    #     await ctx.message.delete()
    #     await ctx.send(message)

    #Removed cause bandwidth
    # @command(name="fact")
    # @cooldown(2, 60, BucketType.user)
    # async def animal_fact(self, ctx, animal: str):
    #     if (animal := animal.lower()) in ("dog","cat","panda","fox","bird","koala"):
    #         fact_url = f"https://some-random-api.ml/facts/{animal}"
    #         image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird'else animal}"

    #         async with request("Get", image_url, headers={}) as response:
    #             if response.status == 200:
    #                 data = await response.json()
    #                 image_,,link = data["link"]
    #             else:
    #                 image_link = None

    #             async with request("GET", fact_url, headers={}) as response:
    #                 if response.status == 200:
    #                     data = await response.json()

    #                     embed = Embed(title=f"{animal.title()} fact",
    #                                            description=data["fact"],
    #                                            colour=ctx.author.colour)

    #                     embed.set_image(url=image_link)
    #                     await ctx.send(embed=embed)

    #                 else:
    #                     await ctx.send(f"API returned a {response.status} status")
    #     else:
    #         await ctx.send(f"No facts are avalaible for {animal}, sorry")

    @command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f"{ctx.author.display_name}, pong!")


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")



def setup(bot):
    bot.add_cog(Fun(bot))
