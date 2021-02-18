
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
        pass



    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Utils")



def setup(bot):
    bot.add_cog(Utils(bot))        