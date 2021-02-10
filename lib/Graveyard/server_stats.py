

# from typing import Optional
# from discord.ext.commands import Cog
# from discord.ext.commands import command 
# from discord import Embed, Member
# import datetime
# import mariadb
# import sys
# from ..db import db


# class server_stats(Cog):

#     def __init__(self, bot):

#         self.bot = bot

#     @Cog.listener()
#     async def on_ready(self):
#         if not self.bot.ready:
#             self.bot.cogs_ready.ready_up("server_stats")
    
#     def PlayerUID(self, cursor, SteamID):

        
#         cursor.execute("SELECT PlayerUID FROM PlayerStats")
#         players = cursor.fetchall()
#         for player in players:
#             if str(player) == f"('{SteamID}',)":
#                 return player
#         else:
#             return False
    
#     def PlayerStatus(self, cursor, SteamID):

#         cursor.execute("SELECT * FROM PlayerStatus WHERE MapID = 4")
#         rows = cursor.fetchall()
        
#         for row in rows:
#             if row[0] == SteamID:
#                 return row[4],row[5],row[6]
    
#     def PlayerStats(self, cursor, SteamID):
#         cursor.execute("SELECT * FROM PlayerStats")
#         rows = cursor.fetchall()

#         for row in rows:
#             if row[0] == SteamID:
#                 return row[2],row[3],row[4],row[5],row[6],row[7]
    
#     def Connect(self):
#         conn = mariadb.connect(
#             user="nordic",
#             password="8itEJuK6saKAmE1aL451w326Bujo44",
#             database="a3nordicwasteland",
#             host="178.63.16.206",
#             port=3306)
#         cursor = conn.cursor()
#         return cursor
    

        
                
                
    
#     @command(name="server_stats",aliases=["ss","stats"])
#     async def server_stats(self, ctx):

#         cursor = self.Connect()

#         if SteamID := db.field(f"SELECT SteamID FROM users Where UserID = {ctx.author.id}"):

#             if Player := self.PlayerUID(cursor, SteamID):
#                 Balance, Bounty, BountyKills = self.PlayerStatus(cursor, SteamID)
#                 PlayerKills, AIKills, TeamKills, DeathCount, ReviveCount, CaptureCount = self.PlayerStats(cursor, SteamID)
                
                        

#                 embed = Embed(title=f"Statistics for `{SteamID}`",
#                             colour = ctx.author.colour,
#                             timestamp=datetime.datetime.now())
#                 embed.set_thumbnail(url=ctx.author.avatar_url)
#                 embed.set_footer(text=f'ID: {ctx.author.id}')
#                 embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        
#                 fields = [("Balance", Balance, True),
#                           ("Player Kills", PlayerKills, True),
#                           ("KDr: ", round(int(PlayerKills)/int(DeathCount), 2), True),
#                           ("Bounty", Bounty, True),
#                           ("AI Kills", AIKills, True),
#                           ("Team Kills", TeamKills, True),
#                           ("Death Count", DeathCount, True),
#                           ("Revive Count", ReviveCount, True),
#                           ("Capture Count", CaptureCount, True)]
                    
#                 for name, value, inline in fields:
#                     embed.add_field(name=name, value=value, inline=inline)
                
#                 await ctx.send(embed=embed)
            


#             else:
#                 await ctx.send("Specified Steam ID not found in remote DB")

#         else:
#             await ctx.send("No Steam ID in local DB, pleas use !link")


#     #Removed because kinda pointless in terms of server 

#     # @command(name="server_weather", aliases=["sw"])
#     # async def server_weather(self,ctx):
#     #     await ctx.send("Under Construction :)")
        
#     #     cursor = self.Connect()

#     #     cursor.execute("SELECT FROM ServerTime WHERE MapID = 1")
        
#     #     DayTime = cursor.execute("SELECT DayTime FROM ServerTime WHERE MapID = 1")
#     #     Fog = cursor.execute("SELECT Fog FROM ServerTime WHERE MapID = 1")
#     #     OverCast = cursor.execute("SELECT Overcast FROM ServerTime WHERE MapID = 1")
#     #     Rain = cursor.execute("SELECT Rain FROM ServerTime WHERE MapID = 1")

#     #     embed = Embed(title=f"Server Weather",
#     #                         colour = ctx.author.colour,
#     #                         timestamp=datetime.datetime.now())
#     #     embed.set_thumbnail(url=ctx.author.avatar_url)
#     #     embed.set_footer(text=f'ID: {ctx.author.id}')
#     #     embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

#     #     fields = [("Time", DayTime, True),
#     #             ("Fog", Fog, True),
#     #             ("Overcast", OverCast, True),
#     #             ("Rain", Rain, True)]
                    
#     #     for name, value, inline in fields:
#     #         embed.add_field(name=name, value=value, inline=inline)
        
#     #     await ctx.send(embed=embed)
                





# def setup(bot):
#     bot.add_cog(server_stats(bot))        