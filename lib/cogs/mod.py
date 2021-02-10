from asyncio import sleep
from datetime import datetime, timedelta
from re import search
from typing import Optional

from discord.ext.menus import MenuPages, ListPageSource
from discord import Embed, Member
from discord import utils
from discord.utils import get
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions


from ..db import db

class Mod(Cog):
    def __init__(self,bot):
        self.bot=bot
    
    @command(name="modMenu")
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def modMenu(self, ctx, targets : Greedy[Member]):
        def blueprintEmbed(title):
            sent = Embed(title=title,
                        colour = ctx.author.colour,
                        timestamp=datetime.now())
            sent.set_footer(text=f'ID: {ctx.author.id}')
            sent.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            return sent
        
        async def question(self):
            quest = await ctx.send(embed=blueprintEmbed("add reason"))
            await quest.add_reaction(reacts["yes"])
            await quest.add_reaction(reacts["no"])


        reacts = {"mute" : u"\U0001F4AC",
                  "ban" : u"\U0001F528",
                  "kick" : u"\U0001F460",
                  "yes" : u"\u2611",
                  "no" : u"\u274C"}
            
        commands = {u"\U0001F4AC" : self.mute_members,
                    u"\U0001F528" : self.ban_members,
                    u"\U0001F460" : self.kick}
                
        for target in targets:      
            fields =   [("Name", str(target),True),
                        ("ID", target.id, True),
                        ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                        ("To mute: ", reacts["mute"], True),
                        ("To ban: ", reacts["ban"], True),
                        ("To kick: ", reacts["kick"], True)]
            
            menu = blueprintEmbed("Mod menu")
            for name, value, inline in fields:
                menu.add_field(name=name, value=value, inline=inline)
            menu = await ctx.send(embed=menu)
            
            await menu.add_reaction(reacts["mute"])
            await menu.add_reaction(reacts["ban"])
            await menu.add_reaction(reacts["kick"])


            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user==ctx.author and reaction.emoji in [reacts["ban"], reacts["mute"], reacts["kick"]], timeout=600)
                if reaction.emoji:
                    await question(self)
                    answer, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user==ctx.author and reaction.emoji in [reacts["yes"], reacts["no"]], timeout=600)
                    if answer.emoji == reacts["yes"]:
                        await ctx.send("Enter reason: ")
                        try:
                            reason = await self.bot.wait_for(
                                        "message",
                                        timeout=1200,
                                        check =lambda message: message.author == ctx.author \
                                            and  message.guild
                                        )
                            if reaction.emoji == reacts["mute"]:
                                await ctx.send("testing")
                            else:
                                await commands[reaction.emoji](target, str(reason)) 
                        except TimeoutError:
                            await ctx.send("Query timed out")               
                    else:
                        await commands[reaction.emoji](ctx, target)
            except TimeoutError:
                await ctx.send("Query time out.")

                       


                                
       

    
    @command(name="kick")
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick(self,ctx,targets : Greedy[Member],*,reason:Optional[str]="No reason given"):
        """Kicks members (Greedy)."""
        if len(targets):
            for target in targets:
                if (ctx.guild.me.top_role.position > target.top_role.position 
                    and not target.guild_permissions.administrator):
                    await target.kick(reason=reason)
                    await ctx.send(f"{target} kicked.")
                else:
                    await ctx.send("That user is above you, or an adminstrator.")
        else:
            await ctx.send("Missing recquired argument(s).")
                
    @command(name="ban")
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def ban_members(self,ctx,targets:Greedy[Member],*,reason:Optional[str]="No reason given"):
        """Bans members (Greedy)."""
        if len(targets):
            for target in targets:
                if (ctx.guild.me.top_role.position > target.top_role.position and not target.guild_permissions.administrator):
        
                    await target.ban(reason=reason)
                    await ctx.send(f"{target} banned.")
                else:
                    await ctx.send("That user is above you, or an adminstrator.")
        else:
            await ctx.send("Missing recquired argument(s).")
    
    @command(name="clear",aliases=["remove","rmv"])
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def clear_message(self, ctx, targets : Greedy[Member], limit : Optional[int]=10):
        """Clears messages, defauly = 10, specified member(s) (Greedy) will remove only those messagess."""
        def check(message):
            return not len(targets) or message.author in targets
            
        with ctx.channel.typing():
            await ctx.message.delete()
            purged = await ctx.channel.purge(limit=limit,check=check)

            await ctx.send(f"Deleted {len(purged):,} messages.", delete_after = 6)
    
    async def mute_members(self,ctx, message,targets,minutes,reason):
        unmutes=  []
        
        for target in targets:
            if (ctx.guild.me.top_role.position > target.top_role.position and not target.guild_permissions.administrator):
                if not utils.get(ctx.guild.roles, name="Shadow") in target.roles:
                    if message.guild.me.top_role.position > target.top_role.position:
                        role_ids = ",".join([str(r.id) for r in target.roles])
                        end_time = datetime.utcnow()+timedelta(minutes=minutes) if minutes else "Indefinite"

                        db.execute("INSERT INTO mutes VALUES (?,?,?,?,?,?)", target.id, role_ids, ctx.author.display_name, reason, minutes, getattr(end_time, "isoformat", lambda : "Indefinite")())
                        db.commit()

                        await target.edit(roles=[])
                        await target.add_roles(utils.get(ctx.guild.roles,name="Shadow"))

                        embed =Embed(title="Member Muted",
                                    colour=target.colour,
                                    timestamp=datetime.utcnow())
                    

                        embed.set_footer(text=f'ID: {target.id}')
                        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                        #embed.set_thumbnail(url=target.avatar.url)

                        fields = [("Member", target.display_name, False),
                                ("Action by: ", message.author.display_name, False),
                                ("Duration", f"{minutes:,} hours(s)" if minutes else "Indefinite", False),
                                ("Reason", reason, False)]
                        
                        for name, value, inline in fields:
                            embed.add_field(name=name, value=value, inline=inline)
                    
                        await self.bot.get_channel(800742053075091456).send(embed=embed)
                        await ctx.send(f"{target.display_name} muted.")
                        
                        if minutes:
                            unmutes.append(target)
            
                else:
                    await ctx.send(f"{target.display_name} is already muted.")
            else:
                await ctx.send(f"{target.display_name} is above you or an admin.")
                
        return unmutes


    @command(name="mute")
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def mute_command(self, ctx, targets : Greedy[Member], minutes : Optional[int] = 0, *, reason : Optional[str] = "No reason given"):
        """Mutes members, takes members varaible (Greedy), meaning that multiple users can be selected.."""
        if not len(targets):
            await ctx.send("Missing recquired argument(s)")
        else:
            unmutes = await self.mute_members(ctx, ctx.message, targets, minutes, reason)
            if len(unmutes):
                await sleep(minutes*60)
                await self.unmute_members(ctx, ctx.guild, targets)


                
    async def unmute_members(self,ctx,guild,targets, *, reason="Mute time expired"):
        for target in targets:
            if (ctx.guild.me.top_role.position > target.top_role.position and not target.guild_permissions.administrator):
                if utils.get(ctx.guild.roles, name="Shadow") in target.roles:
                    role_ids = db.field("SELECT RoleIDS FROM mutes WHERE UserID = ?", target.id)
                    roles = [guild.get_role(int(id_)) for id_ in role_ids.split(",") if len(id_)]

                    db.execute("DELETE FROM mutes WHERE UserID = ?", target.id)
                    db.commit()

                    await target.edit(roles=roles)

                    embed = Embed(title="Member unmuted",
                                colour=target.colour,
                                timestamp=datetime.utcnow())
                    
                    embed.set_footer(text=f'ID: {target.id}')
                    embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

                    fields = [("Member", target.display_name, False),
                            ("Reason", reason, False)]
                    
                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)
                    
                    await self.bot.get_channel(800742053075091456).send(embed=embed)
            else:
                await ctx.send(f"{target.display_name} is not muted.")
                
          

                
    @command(name="unmute")
    @bot_has_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    async def unmute_command(self, ctx, targets : Greedy[Member], *, reason : Optional[str] = "No reason given"):
        """Unmutes members, takes members varaible (Greedy), meaning that multiple users can be selected."""
        if not len(targets):
            await ctx.send("Missing recquired arguemt(s)")
        else:
            await self.unmute_members(ctx, ctx.guild, targets, reason=reason)
            await ctx.send("Action completed")
    
    @command(name="muteInfo", aliases=["mI"])
    @has_permissions(manage_roles=True)
    async def testMutes_command(self ,ctx, targets : Greedy[Member]):
        """Displays information on muted members."""
        if len(targets):
            for target in targets:
                if mute := db.field("SELECT * FROM mutes WHERE UserID = ? ", target.id):
                    SanctionedBy = db.field("SELECT SanctionedBy FROM mutes WHERE UserID = ?", target.id)
                    RoleIDS = db.field("SELECT RoleIDS FROM mutes WHERE UserID = ?", target.id)
                    reason = db.field("SELECT reason FROM mutes WHERE UserID = ?", target.id)
                    duration = db.field("SELECT duration FROM mutes WHERE UserID = ?", target.id)
                    EndTime = db.field("SELECT EndTime FROM mutes WHERE UserID = ?", target.id)

                    embed = Embed(title="Mute Info",
                                colour=target.colour,
                                timestamp=datetime.utcnow())
                    
                    embed.set_footer(text=f'ID: {ctx.author.id}')
                    embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                    
                    roles = [ctx.guild.get_role(int(id_)) for id_ in RoleIDS.split(",") if len(id_)]
                   # embed.add_field(name="Roles", value=[str(roles[i]).split("'>,",1)[1] for i in range(len(roles))], inline=False)
                    #embed.add_field(name="Roles", value = [str(role).split("=",1)[1] for role in roles], inline = False)
                    #embed.add_field(name="Roles", value=[str(roles[i]).split("'>",1)[1] for i in range(len(roles))], inline=False)
                    embed.add_field(name="Roles", value =[str(role) for role in roles], inline=False)
                    
                    

                    fields = [("Sanctioned by: ", SanctionedBy, True),
                            ("Reason: ", reason, True),
                            ("Duration: ", duration if duration != 0 else "Indefinite", True),
                            ("End time: ", EndTime if EndTime != 0 else "Indefinite", True),
                            ("UserID: ", target.id, True),
                            ("Display name: ", target.display_name, True)]
                            #("Roles: ", role_names, True)]
                    
                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)
                    
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("User specified is not muted.")
        else:
            await ctx.send("Missing recquired argument(s)")

 
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("mod")

def setup(bot):
    bot.add_cog(Mod(bot))