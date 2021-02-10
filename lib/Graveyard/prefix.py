
# from discord.ext.commands import Cog
# from discord.ext.commands import CheckFailure
# from discord.ext.commands import command, has_permissions

# from ..db import db

# class Misc(Cog):
#     def __init__(self, bot):
#         self.bot = bot
    
#     @command(name="prefix")
#     @has_permissions(manage_guild=True)
#     async def change_prefix(self, ctx, new: str):
#         if len(new) > 5:
#             await ctx.send("Prefix cannot be longer than 5 characters")
        
#         else:
#             db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?",new,ctx.guild.id)
#             await ctx.send(f"Prefix set to {new}")
#             db.commit()
    
#     @change_prefix.error
#     async def change_prefix_error(self, ctx, exc):
#         if isinstance(exc, CheckFailure):
#             await ctx.send("You do not have correct permissions")
    
#     @Cog.listener()
#     async def on_ready(self):
#         if not self.bot.ready:
#             self.bot.cogs_ready.ready_up("prefix")

# def setup(bot):
#     bot.add_cog(Misc(bot))