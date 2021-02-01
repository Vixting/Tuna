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

        async def blueprint(self):
            embed = Embed(title=choice(["Hi!","Hello!","Hey!","Guten Tag!", "Hallå!", "Oi!"]),
                    description=f"Welcome to {member.guild.name} {member.mention}, please read rules in <#795328095850332160> and start an application with !apply",
                    colour=member.colour)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await self.bot.get_channel(795328358648119327).send(embed=embed)
            await member.add_roles(utils.get(member.guild.roles,name="Member"))

        check = db.field("SELECT UserID FROM users Where UserID = ?", member.id)

        if check:
            await blueprint(self)

        else:
            db.execute("INSERT INTO users (UserID) VALUES (?)", member.id)
            db.execute("UPDATE users SET Join_Date=(?) WHERE UserID=(?)", datetime.datetime.now(), member.id)

            await blueprint(self)
            #await member.edit(roles=[member.guild.get_role(id_) for id_ in (755536620148752394, 755868062497898607)]) use for multiple roles

        

def setup(bot):
    bot.add_cog(Welcome(bot))