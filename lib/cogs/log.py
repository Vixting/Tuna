from discord.ext.commands import Cog
from discord.ext.commands import command 
from discord import Embed
import datetime

class log(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.LogChannel = self.bot.get_channel(800742053075091456)
            self.bot.cogs_ready.ready_up("log")

    @Cog.listener()
    async def on_user_update(self, before, after): #Should make this more oop, 1-2 function to handle embeds
        if before.name != after.name:

            embed = Embed(title=f"Username change",
                          colour = after.colour,
                          timestamp=datetime.datetime.now())
            embed.set_thumbnail(url=after.avatar_url)
            embed.set_footer(text=f'ID: {after.id}')
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            
            fields = [("Before", before.name, False),
                        ("After", after.name, False)]
            
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            
            await self.bot.get_channel(800742053075091456).send(embed=embed)
        
        if before.discriminator != after.discriminator:
            embed = Embed(title=f"Discriminator change",
                          colour = after.colour,
                          timestamp=datetime.datetime.now())
            embed.set_thumbnail(url=after.avatar_url)
            embed.set_footer(text=f'ID: {after.id}')
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            
            fields = [("Before", before.discriminator, False),
                        ("After", after.discriminator, False)]
            
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            
            #await self.LogChannel.send(embed=embed)
            await self.bot.get_channel(800742053075091456).send(embed=embed)



        if before.avatar_url != after.avatar_url:

            embed = Embed(title=f"Avatar Change",
                          description = f"Edit by: {after.display_name}",
                          colour = after.colour,
                          timestamp=datetime.datetime.now())
            embed.set_thumbnail(url=before.avatar_url)
            embed.set_image(url=after.avatar_url)

            embed.set_footer(text=f'ID: {after.id}')
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await self.bot.get_channel(800742053075091456).send(embed=embed)
            


            

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = Embed(title=f"Displayname Change ",
                          colour = after.colour,
                          timestamp=datetime.datetime.now())
            embed.set_thumbnail(url=after.avatar_url)
            embed.set_footer(text=f'ID: {after.id}')
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            
            fields = [("Before", before.display_name, False),
                        ("After", after.display_name, False)]
            
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            
            #await self.LogChannel.send(embed=embed)
            await self.bot.get_channel(800742053075091456).send(embed=embed)
        
        elif before.roles != after.roles:
            embed = Embed(title=f"Role Updates",
                          description =f"User: {after.display_name}",
                          colour = after.colour,
                          timestamp=datetime.datetime.now())
            embed.set_thumbnail(url=after.avatar_url)
            embed.set_footer(text=f'ID: {after.id}')
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                
            if (len([r.mention for r in before.roles]) > len([r.mention for r in after.roles])):
                difference = set([r.mention for r in before.roles]) - set([r.mention for r in after.roles])
                Type = "Removal"
            else:
                difference = set([r.mention for r in after.roles]) - set([r.mention for r in before.roles])
                Type = "Addition"

                
            fields = [("Before",", ".join([r.mention for r in before.roles]), False),
                        ("After",", ".join([r.mention for r in after.roles]), False),
                        (Type, difference, False)]
            
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.bot.get_channel(800742053075091456).send(embed=embed)

        
        
        

    @Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot:
            if before.content != after.content:

                embed = Embed(title=f"Message Edit",
                          #description = f"Edit by: {after.author.display_name}",
                          colour = after.author.colour,
                          timestamp=datetime.datetime.now())
                embed.set_thumbnail(url=after.author.avatar_url)
                embed.set_footer(text=f'ID: {after.id}')
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

                if (len([before.content]) > len([after.content])):
                    difference = set([before.content]) - set([after.content])
                else:
                    difference = set([after.content]) - set([before.content])

                
                
                fields = [("Before", before.content, False),
                            ("After", after.content, False),
                            ("Difference", difference, False)]
                
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
                
                await self.bot.get_channel(800742053075091456).send(embed=embed)


    @Cog.listener()
    async def on_message_delete(self, message):

        if not message.author.bot:

            embed = Embed(title=f"Message Deletion",
                        description = f"Author: {message.author.display_name}",
                        colour = message.author.colour,
                        timestamp=datetime.datetime.now())
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_footer(text=f'ID: {message.author.id}')
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            
            fields = [("Content", message.content, False)]
            
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            
            await self.bot.get_channel(800742053075091456).send(embed=embed)
    
    @Cog.listener()
    async def on_member_remove(self, member):

        guild = member.guild
        async for entry in guild.audit_logs(limit=1):

            print(entry)
            if str(entry.action) == "AuditLogAction.kick":


                embed = Embed(title="Member Kicked",
                                      description=f"{member.mention} has been kicked by {entry.user.mention}",
                                      colour=member.colour,
                                      timestamp=datetime.datetime.now())
                embed.add_field(name='Reason:', value=f"{entry.reason}", inline=True)
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text=f'ID: {member.id}')
                await self.bot.get_channel(800742053075091456).send(embed=embed)

            elif str(entry.action) == "AuditLogAction.ban":


                embed = Embed(title="Member Banned",
                                      description=f"{member.mention} has been banned by {entry.user.mention}",
                                      colour=member.colour,
                                      timestamp=datetime.datetime.now())
                embed.add_field(name='Reason:', value=f"{entry.reason}", inline=True)
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text=f'ID: {member.id}')
                await self.bot.get_channel(800742053075091456).send(embed=embed)


def setup(bot):
    bot.add_cog(log(bot))        