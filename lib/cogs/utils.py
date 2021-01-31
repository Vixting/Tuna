
from discord import channel
from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions
from typing import Optional
from discord.ext.commands import Cog, Greedy
from discord import Embed, Member
from asyncio import sleep

from datetime import datetime



class Utils(Cog):
    def __init__(self,bot):
        self.bot=bot
    
    @command(name="remind", aliases=["rem"])
    async def remind(self,ctx,target : Greedy[Member],*,  time:int,  msg:Optional[str]="No reason given"):
        await ctx.send("wrf")
        if time and msg and len(target):
            for target in target:
                await ctx.send(f"Reminding {target} in {time} ")
                await sleep(time)
                await ctx.send("zzz")
                embed = Embed(title=msg,
                                        colour = ctx.author.colour,
                                        timestamp=datetime.now())
                embed.set_footer(text=f'ID: {ctx.author.id}')
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                await target.send(embed=embed)
        else:
            await ctx.send("Missing recquired argument(s)")



    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Utils")



def setup(bot):
    bot.add_cog(Utils(bot))        