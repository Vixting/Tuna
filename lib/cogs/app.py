


import json
from discord import channel
from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions
from discord import Embed
from asyncio import TimeoutError
from ..db import db
import datetime
class Application(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(name="apply", aliases=["t"])
    async def apply(self, ctx):
        """Opens application in direct message."""
        answers = []
        cont = True

        embed = timedOut("Do you wish to proceed?", ctx, self.bot, "This query will close in two minutes.")
        sent = await ctx.author.send(embed=embed)
    
        await sent.add_reaction(u"\u2611")
        await sent.add_reaction(u"\u274C")
        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user==ctx.author and reaction.emoji in [u"\u2611", u"\u274C"], timeout=120)
            if reaction.emoji == u"\u2611":
                with open("./data/applications/Welcome") as f:
                    data = json.load(f)

                    for question in data["Questions"]:
                        if cont != True:
                            break
                        else:
                            embed = timedOut(question, ctx, self.bot, "This application will close in 20 minutes.")
                            sent = await ctx.author.send(embed=embed)
                            
                            try:
                                msg = await self.bot.wait_for(
                                    "message",
                                    timeout=1200,
                                    check =lambda message: message.author == ctx.author \
                                        and not message.guild
                                    )
                                if msg:
                                    contents = str(msg.content)
                                    answers.append(contents)
                                    

                            except TimeoutError:
                                await ctx.author.send(embed=timedOut("Query timed out", ctx, self.bot,f"ID: {ctx.author.id}"))
                                cont = False
                            
            else:
                cont = False
                await ctx.author.send(embed=timedOut("Application cancelled", ctx, self.bot,f"ID: {ctx.author.id}"))
                await sent.delete()
            
        except TimeoutError:
            cont = False
            await ctx.author.send(embed=timedOut("Query timed out", ctx, self.bot,f"ID: {ctx.author.id}"))
            await sent.delete()
            



                
        if cont == True:
            embed = timedOut("Do you wish to send your application?", ctx, self.bot, "This query will timed out in 10 minutes.")
  
            sent = await ctx.author.send(embed=embed)
            await sent.add_reaction(u"\u2611")
            await sent.add_reaction(u"\u274C")
        
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user==ctx.author and reaction.emoji in [u"\u2611", u"\u274C"], timeout=600)
                if reaction.emoji == u"\u2611":

                        end_embed = timedOut(f"Application by {ctx.author}", ctx, self.bot, f"ID: {ctx.author.id}")
                        embed.set_thumbnail(url=ctx.author.avatar_url)

                        i=-1
                        for question in data["Questions"]:
                            i=i+1
                            end_embed.add_field(name=question, value=answers[i], inline=False)
                        await self.bot.get_channel(795389697655570432).send(embed=end_embed)

                        await ctx.author.send(embed=timedOut("Thank you for your application", ctx, self.bot, f"ID: {ctx.author.id}"))
                else:
                    await ctx.author.send(embed=timedOut("Application cancelled", ctx, self.bot,f"ID: {ctx.author.id}"))
                    await sent.delete()
                
            except TimeoutError:

                await ctx.author.send(embed=timedOut("Query timed out", ctx, self.bot,f"ID: {ctx.author.id}"))

            
                

def timedOut(reason, ctx, bot, footer):
        embed = Embed(title=reason,
                                colour = ctx.author.colour,
                                timestamp=datetime.datetime.now())
        embed.set_footer(text=footer)
        embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
        return embed

        

    



def setup(bot):
    	bot.add_cog(Application(bot))
