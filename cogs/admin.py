import discord
from discord.ext import commands
import aiohttp
from io import BytesIO
from itertools import cycle
import os

ping_cycle = cycle(['fuck off','leave me alone','i said leave me alone','what do you want','am busy'])

class admin(commands.Cog):
  
  def __init__(self, bot: commands.Bot):
        self.bot = bot

  @commands.command()
  async def ping(self, ctx):
        await ctx.message.reply(next(ping_cycle))

  @commands.command()
  async def help(self, ctx):
    await ctx.message.reply('look at this nerd they dont know the commands')
    await ctx.send('<:toffsmug:835669251243114526>')

  @commands.command()
  async def servers(self, ctx):
    if ctx.author.id == self.bot.owner_id:
      msg = f"currently in {len(list(self.bot.guilds))} servers:\n"
      for item in list(self.bot.guilds):
        msg = msg + item.name + "\n"
      await ctx.message.reply(msg)
    else:
      msg = f"currently in {len(list(self.bot.guilds))} servers\n"
      await ctx.message.reply(msg)
  @commands.command()
  @commands.is_owner()
  async def mind_control(self, ctx, arg1, arg2:int):
    print(arg2)
    channel = await self.bot.fetch_channel(arg2)
    await channel.send(arg1)
    
  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, user: discord.Member, *, reason = None):
    if ctx.message.author == user:
	    await ctx.message.reply('you cant kick yourself dumbass')
    elif not reason:
      await user.kick()
      await ctx.message.reply(f"**{user}** has been kicked.")
    else:
      await user.kick(reason=reason)
      await ctx.message.reply(f"**{user}** has been kicked for **{reason}**.")

  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def clear(self, ctx, limit: int):
          await ctx.channel.purge(limit=limit+1)
          await ctx.send(f'{limit} messages Cleared by {ctx.author.mention}', delete_after=5)

  @commands.command()
  @commands.has_permissions(manage_nicknames=True)
  async def change_bot_nick(self, ctx, *, arg=None):
    try:
        if not arg:
          await ctx.message.guild.me.edit(nick='')
          await ctx.message.reply('my nickname has been  reset')
        else:
          await ctx.message.guild.me.edit(nick=arg)
          await ctx.message.reply(f'nickname changed to  {arg}')
    except: 
        await ctx.message.reply('i cant change my own  nickname, 1984')

  @commands.command()
  @commands.has_permissions(manage_emojis=True)
  async def create_emote(self, ctx, url: str, *, name):
	  guild = ctx.guild
	  async with aiohttp.ClientSession() as ses:
		  	async with ses.get(url) as r:
        
  				try:
  					img_or_gif = BytesIO(await r.read())
  					b_value = img_or_gif.getvalue()
  					if r.status in range(200, 299):
  						await guild.create_custom_emoji(image=b_value, name=name)
  						await ctx.message.reply('Successfully created emoji')
  						await ses.close()
  					else:
  						await ctx.message.reply('Error when making request')
  						await ses.close()
  
  				except discord.HTTPException:
  					await ctx.message.reply('File size is too thicc 😏')

  @commands.command()
  @commands.is_owner()
  async def restart_bot(self, ctx):
    await ctx.send("<:qtdie:878143099430400032>")
    for file in os.listdir("cogs"):
     if file.endswith(".py"):
          name = file[:-3]
          self.bot.reload_extension(f"cogs.{name}")
          await ctx.send(f'reloaded {name}')

  @commands.command()
  @commands.is_owner()
  async def kill_bot(self, ctx):
    await ctx.send("<:qtdie:878143099430400032>")
    exit("bot closed")


def setup(bot):
    bot.add_cog(admin(bot))