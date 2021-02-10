

# from discord.ext.commands import Cog
# from discord.ext.commands import command 
# from discord import Embed
# import datetime

# from ..db import db


# class link(Cog):
#     def __init__(self, bot):
#         self.bot = bot

#     @Cog.listener()
#     async def on_ready(self):
#         if not self.bot.ready:
#             self.bot.cogs_ready.ready_up("link")
    
#     @command(name="link")
#     async def link(self, ctx, SteamID : int):
#         if len(str(SteamID)) == 17:
            
#             if db.field(f"SELECT UserID FROM users Where UserID = {ctx.author.id}"):
#                   db.execute(f"UPDATE users SET SteamID={SteamID} WHERE UserID={ctx.author.id}")
#                   db.commit() #manual commit because of testing
#                   await ctx.send(f"Linked  Discord user ID: `{ctx.author.id}` with SteamID: `{SteamID}`")
            
#             else:
#                 db.execute("INSERT INTO users (UserID) VALUES (?)", ctx.author.id)
#                 db.execute(f"UPDATE users SET SteamID={SteamID} WHERE UserID={ctx.author.id}")
#                 db.commit()
#                 await ctx.send("User ID not found in local data base, UserID linked with SteamID automatically.")
          
        
#         else:
#             await ctx.send("That is not a valid Steam ID")
    
#     @command(name="checklink")
#     async def CheckLink(self, ctx):

#         if check := db.field(f"SELECT SteamID FROM users Where UserID = {ctx.author.id}"):
#             await ctx.send(f"Your are linked with: {str(check)}")
#         else:
#             await ctx.send("No SteamID set")
        
        


# def setup(bot):
#     bot.add_cog(link(bot))        