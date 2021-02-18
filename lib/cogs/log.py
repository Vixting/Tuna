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
            embed = templateEmbed("Username change", "", after)
            
            fields = [("Before", f"`{before.display_name}`", False),
                        ("After", f"`{after.display_name}`", False)]
            
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            
            await self.bot.get_channel(800742053075091456).send(embed=embed)
        
        if before.discriminator != after.discriminator:
            embed = templateEmbed("Discriminator change", "", after)
            
            fields = [("Before", before.discriminator, False),
                        ("After", after.discriminator, False)]
            
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            
            #await self.LogChannel.send(embed=embed)
            await self.bot.get_channel(800742053075091456).send(embed=embed)



        if before.avatar_url != after.avatar_url:
            embed = templateEmbed("Avatar change", f"Edit by: `{after.display_name} #{after.discriminator}`", False, before)
            embed.set_image(url=after.avatar_url)

            await self.bot.get_channel(800742053075091456).send(embed=embed)
            


            

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = templateEmbed(self.bot, "Displayname Change", "", after)
            
            fields = [("Before", f"`{before.display_name} #{before.discriminator}`", False),
                        ("After", f"`{after.display_name} #{before.discriminator}`", False)]
            
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            
            #await self.LogChannel.send(embed=embed)
            await self.bot.get_channel(800742053075091456).send(embed=embed)
        
        elif before.roles != after.roles:
            
            embed = templateEmbed(self.bot, "Role Updates", f"User: `{after.display_name} #{after.discriminator}`", after)
                
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
                embed = templateEmbed(self.bot, "Message Edit", f"Edit by: `{after.author.name} #{after.author.discriminator}`", False, after)
 
                fields = [("Before", before.content, False),
                          ("After", after.content, False)]
                
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
                
                await self.bot.get_channel(800742053075091456).send(embed=embed)


    @Cog.listener()
    async def on_message_delete(self, message):

        if not message.author.bot:
            embed = templateEmbed(self.bot, "Message deletion", f"Athor: `{message.author.name} #{message.author.discriminator}`", False, message)
        
            fields = [("Content", message.content, False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            
            await self.bot.get_channel(800742053075091456).send(embed=embed)
    
    @Cog.listener()
    async def on_member_remove(self, member):

        guild = member.guild
        async for entry in guild.audit_logs(limit=1):

            if str(entry.action) == "AuditLogAction.kick":

                embed = templateEmbed(self.bot, "Member Kicked", f"{member.mention} has been kicked by {entry.user.mention}", member)
                embed.add_field(name='Reason:', value=f"{entry.reason}", inline=True)
             
                await self.bot.get_channel(800742053075091456).send(embed=embed)

            elif str(entry.action) == "AuditLogAction.ban":

                embed = templateEmbed(self.bot, "Member Banned", f"{member.mention} has been banned by {entry.user.mention}", member)
                embed.add_field(name='Reason:', value=f"{entry.reason}", inline=True)    

                await self.bot.get_channel(800742053075091456).send(embed=embed)

def templateEmbed(bot, title, description, member=False, message=False):
    embed = Embed(title=title,
                  description=description,
                  colour=member.colour if member else message.author.colour,
                  timestamp=datetime.datetime.now())

    embed.set_thumbnail(url=member.avatar_url if member else message.author.avatar_url)
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    embed.set_footer(text=f'ID: {member.id if member else message.author.id}')
    return embed
    

def setup(bot):
    bot.add_cog(log(bot))        