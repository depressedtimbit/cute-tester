from os import name
from sqlite3.dbapi2 import Cursor
import discord
from discord.ext import commands
from discord.utils import get
import sqlite3

async def starboard_message(message, wbchannel, channel, star_amount):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT new_msg_id FROM starboard_messages WHERE old_msg_id = {message.id}')
        new_message_id = cursor.fetchone()
        if not new_message_id:
            embed = discord.Embed(title=message.content)
            embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
            embed.add_field(name="**orginal**", value=f'[jump](https://discord.com/channels/{message.guild.id}/{channel.id}/{message.id})')
            new_message = await wbchannel.send(embed=embed, content=f':dizzy: **{star_amount}** {channel.mention}')
            db.execute(f"INSERT INTO starboard_messages(old_msg_id, new_msg_id) VALUES({message.id},{new_message.id})")
            db.commit()
            db.close()
        else:
            try:
                embed = discord.Embed(title=message.content)
                embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                embed.add_field(name="**orginal**", value=f'[jump](https://discord.com/channels/{message.guild.id}/{channel.id}/{message.id})')
                url = message.attachments.url 
                if url: embed.set_image(url=url)
                new_message = await wbchannel.fetch_message(new_message_id[0])
                await new_message.edit(embed=embed, content=f':dizzy: **{star_amount}** {channel.mention}')
                db.close()
            except discord.errors.NotFound:
                cursor.execute(f"DELETE FROM starboard_messages WHERE new_msg_id = {new_message_id[0]}")
                db.commit()
                db.close()
                await starboard_message(message, wbchannel, channel, star_amount)

class starboard(commands.Cog):
  
    def __init__(self, bot: commands.Bot):
            self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM starboard WHERE guild_id = {payload.guild_id}')
        result = cursor.fetchone()
        if result[2]:
            channel = await self.bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            wbchannel = await self.bot.fetch_channel(result[1])
            if payload.emoji.name == "⭐":
                reaction = get(message.reactions, emoji=payload.emoji.name)
                if reaction and reaction.count >= result[4]:
                    if result[3]:
                        await starboard_message(message, wbchannel, channel, reaction.count)
                    elif not payload.member == message.author:
                        await starboard_message(message, wbchannel, channel, reaction.count)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM starboard WHERE guild_id = {payload.guild_id}')
        result = cursor.fetchone()
        if result[2]:
            channel = await self.bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            wbchannel = await self.bot.fetch_channel(result[1])
            if payload.emoji.name == "⭐":
                reaction = get(message.reactions, emoji=payload.emoji.name)
                if not reaction or reaction.count < result[4]:
                    if result[3]:
                        try:
                            cursor.execute(f'SELECT new_msg_id FROM starboard_messages WHERE old_msg_id = {message.id}')
                            new_message_id = cursor.fetchone()
                            new_message = await wbchannel.fetch_message(new_message_id[0])
                            await new_message.delete()
                        except discord.errors.NotFound: 
                            cursor.execute(f"DELETE FROM starboard_messages WHERE new_msg_id = {new_message_id[0]}")
                            db.commit()
                            db.close()
                    elif not payload.member == message.author:
                        try:
                            cursor.execute(f'SELECT new_msg_id FROM starboard_messages WHERE old_msg_id = {message.id}')
                            new_message_id = cursor.fetchone()
                            new_message = await wbchannel.fetch_message(new_message_id[0])
                            await new_message.delete()
                        except discord.errors.NotFound: 
                            cursor.execute(f"DELETE FROM starboard_messages WHERE new_msg_id = {new_message_id[0]}")
                            db.commit()
                            db.close()
                        
                else:
                    await starboard_message(message, wbchannel, channel, reaction.count)
    
    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def starboard(self, ctx):
        await ctx.message.reply(
            'Availble Setup Commands \nstarboard channel: `!cute starboard channel <channel>`\nenable and disable: `!cute starboard enable/disable`\nstar amount `!cute starboard set_star_amount <number>`\nenable self stars `!cute starboard self_star <enable/disable>`'
            )
    
    @starboard.command()
    async def channel(self, ctx, channel:discord.TextChannel):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT channel_id FROM starboard WHERE guild_id = {ctx.guild.id}')
        result = cursor.fetchone()
        if result is None:
            sql = (f"INSERT INTO starboard(guild_id, channel_id) VALUES({ctx.guild.id},{channel.id})")
            await ctx.message.reply(f"Channel has been set to {channel.mention}")
        elif result is not None:
            sql = (f"UPDATE starboard SET channel_id = {channel.id} WHERE guild_id = {ctx.guild.id}")
            await ctx.message.reply(f"Channel has been changed to {channel.mention}")
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
    
    @starboard.command()
    async def enable(self, ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT channel_id FROM starboard WHERE guild_id = {ctx.guild.id}')
        channel = cursor.fetchone()
        if not channel:
            await ctx.message.reply("you need to set a starboard channel first")
            cursor.close()
            db.close()
        else:
                sql = (f"UPDATE starboard SET enabled = 1 WHERE guild_id = {ctx.guild.id}")
                await ctx.message.reply(f"starboard in this server has been enabled")
                cursor.execute(sql)
                db.commit()
                cursor.close()
                db.close()
    
    @starboard.command()
    async def disable(self, ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT channel_id FROM starboard WHERE guild_id = {ctx.guild.id}')
        channel = cursor.fetchone()
        if not channel:
            await ctx.message.reply("you need to set a starboard channel first")
            cursor.close()
            db.close()
        else:
                sql = (f"UPDATE starboard SET enabled = 0 WHERE guild_id = {ctx.guild.id}")
                await ctx.message.reply(f"starboard in this server has been disabled")
                cursor.execute(sql)
                db.commit()
                cursor.close()
                db.close()
    
    @starboard.command()
    async def set_star_amount(self, ctx, staramount:int):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT channel_id FROM starboard WHERE guild_id = {ctx.guild.id}')
        channel = cursor.fetchone()
        if not channel:
            await ctx.message.reply("you need to set a starboard channel first")
            cursor.close()
            db.close()
        else:
            sql = (f"UPDATE starboard SET required_stars = {staramount} WHERE guild_id = {ctx.guild.id}")
            if staramount == 1:
                replymessage = "a message now needs 1 star to be added to the starboard"
            else: replymessage = f"a message now needs {staramount} stars to be added to the starboard"
            await ctx.message.reply(replymessage)
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
    
    @starboard.command()
    async def self_star(self, ctx, arg=None):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT channel_id FROM starboard WHERE guild_id = {ctx.guild.id}')
        channel = cursor.fetchone()
        if not channel:
            await ctx.message.reply("you need to set a starboard channel first")
            cursor.close()
            db.close()
        else: 
            if not arg:
                cursor.execute(f'SELECT self_star FROM starboard WHERE guild_id = {ctx.guild.id}')
                self_star_enabled = cursor.fetchone()[0]
                if self_star_enabled:
                    await ctx.message.reply("self stars are currently enabled")
                    print(self_star_enabled)
                    cursor.close()
                    db.close()
                else:
                    await ctx.message.reply("self stars are currently disabled")
                    print(self_star_enabled)
                    cursor.close()
                    db.close()
            elif arg.lower() == "enable":
                sql = (f"UPDATE starboard SET self_star = 1 WHERE guild_id = {ctx.guild.id}")
                await ctx.message.reply(f"self stars in this server have been enabled")
                cursor.execute(sql)
                db.commit()
                cursor.close()
                db.close()
            elif arg.lower() == "disable":
                sql = (f"UPDATE starboard SET self_star = 0 WHERE guild_id = {ctx.guild.id}")
                await ctx.message.reply(f"self stars in this server have been disabled")
                cursor.execute(sql)
                db.commit()
                cursor.close()
                db.close()
            else:
                ctx.message.reply('would you like to enable or disable self stars?')
                cursor.close()
                db.close()

def setup(bot):
    bot.add_cog(starboard(bot))
