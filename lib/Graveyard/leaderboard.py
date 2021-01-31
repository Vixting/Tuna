



from discord.ext.commands import Cog
from discord.ext.commands import command 
from discord import Embed
import datetime
import mariadb
import sys
from ..db import db


class server_stats(Cog):

    def __init__(self, bot):

        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("leaderboard")    
    
    @command(name="leaderboard")
    async def server_stats(self, ctx, query : str):
        if (query := query.lower()) in ("kills","aikills","teamkills","capture_points","capture_count","revive_count","bankmoney","bounty","all"):
    
            conn = mariadb.connect(
                user="nordic",
                password="8itEJuK6saKAmE1aL451w326Bujo44",
                database="a3nordicwasteland",
                host="178.63.16.206",
                port=3306)
            cursor = conn.cursor()

        



def setup(bot):
    bot.add_cog(server_stats(bot))        