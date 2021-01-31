
import mariadb
from datetime import datetime
from typing import Optional
from discord.ext.commands import Cog
from discord.ext.commands import command 
from discord import Embed, Member


from ..db import db


class info(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="userinfo", aliases=["ui","mi"])
    async def user_info(self, ctx, target : Optional[Member]):

        def SteamID(target):
            if check := db.field(f"SELECT SteamID FROM users Where UserID = {target.id}"):
                return check
            else:
                return "N/A"
            

        target = target or ctx.author
        embed = Embed(title="User information",
                      colour=target.colour,
                      timestamp=datetime.utcnow())
        embed.set_thumbnail(url=target.avatar_url)
        embed.set_footer(text=f'ID: {ctx.author.id}')
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

            
        fields =   [("Name", str(target),True),
                    ("ID", target.id, True),
                    ("Bot?", target.bot, True),
                    ("Linked SteamID: ",f"`{SteamID(target)}`",True),
                    ("Top role", target.top_role.mention, True),
                    ("Status", str(target.status).title(), True),
                    ("Activity", f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}", False),
                    ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                    ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                    ("Boosted", bool(target.premium_since), True)]
        
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)
    @command(name="serverinfo", aliases=["guildinfo","si","gi"])
    async def server_info(self, ctx):
        
        embed = Embed(title="Server Infornmation",
                      colour=ctx.author.colour,
                      timestamp=datetime.utcnow())
        embed.set_footer(text=f'ID: {ctx.author.id}')
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)


        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]


        fields = [("ID", ctx.guild.id, True),
				  ("Owner", ctx.guild.owner, True),
                  ("Statuses", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
				  ("Region", ctx.guild.region, True),
				  ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Members", len(ctx.guild.members), True),
				  ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
				  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
				  ("Banned members", len(await ctx.guild.bans()), True),
				  ("Text channels", len(ctx.guild.text_channels), True),
				  ("Voice channels", len(ctx.guild.voice_channels), True),
				  ("Categories", len(ctx.guild.categories), True),
				  ("Roles", len(ctx.guild.roles), True),
				  ("Invites", len(await ctx.guild.invites()), True),
				  ("\u200b", "\u200b", True)]
        
        for name, value, inline in fields:
            embed.add_field(name=name,value=value,inline=inline)
        await ctx.send(embed=embed)

	
        
        
        

		

        

        
        

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("info")



def setup(bot):
    bot.add_cog(info(bot))        