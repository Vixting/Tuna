from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed
from random import choice
import datetime
from discord import utils

from ..db import db

class Welcome(Cog):
    def __init__(self,bot):
        self.bot=bot

    @Cog.listener()
    async def on_ready(self):
        self.bot.cogs_ready.ready_up("welcome")

    @Cog.listener()
    async def on_member_join(self, member):
        print("epic")
        #Todo make it more oop, this kinda bad future me
        check = db.field("SELECT UserID FROM users Where UserID = ?", member.id)
        if check:
            embed = Embed(title=choice(["Hi!","Hello!","Hey!","Guten Tag!", "Hallå!", "Oi!"]),
                    description=f"Welcome back to {member.guild.name} {member.mention}, please read rules in <#795328095850332160> and start an application with !apply",
                    colour=member.colour)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await self.bot.get_channel(795328358648119327).send(embed=embed)
            await member.add_roles(utils.get(member.guild.roles,name="Member"))
            #await member.edit(roles=[member.guild.get_role(id_) for id_ in (755536620148752394, 755868062497898607)])

        else:
            db.execute("INSERT INTO users (UserID) VALUES (?)", member.id)
            db.execute("UPDATE users SET Join_Date=(?) WHERE UserID=(?)", datetime.datetime.now(), member.id)
            embed = Embed(title=f"Welcome",
                    description=f"Welcome to {member.guild.name} {member.mention}, please read rules in <#795328095850332160> and start an application with !apply",
                    colour=member.colour)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await  self.bot.get_channel(795328358648119327).send(embed=embed)

            await member.add_roles(utils.get(member.guild.roles,name="Member"))
            #await member.edit(roles=[member.guild.get_role(id_) for id_ in (755536620148752394, 755868062497898607)]) use for multiple roles

    @Cog.listener()
    async def on_member_leave(self, member):
        #this doesnt run when member leaves, idfk
        db.execute("UPDATE users SET Leave_Date=(?) WHERE UserID=(?)", datetime.datetime.now(), member.id)

        print("asd")
        embed = Embed(title=choice(["Bye","Goodbye","Adiose"]),
                    description=f"We hope you enjoyed your stay {member.mention}",
                    colour=member.colour)
        embed.set_thumbnail(url=member.avatar_url)
        
        await self.bot.get_channel(795328358648119327).send(embed=embed)
        

def setup(bot):
    bot.add_cog(Welcome(bot))