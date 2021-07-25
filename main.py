import discord
import os
import time
import random
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure, check, CommandNotFound
from itertools import cycle
import aiohttp
from io import BytesIO
from lists import carslist
from lists import memes as memeslist
from lists import final_fantasy_list
client = discord.Client()

client = commands.Bot(command_prefix = '!cute ', help_command=None) 

ping_cycle = cycle(['fuck off','leave me alone','i said leave me alone','what do you want','am busy'])
status = cycle(['with Python','fortnight','ur mom', 'TF2', 'the other TF2'])
#@client.event
#async def on_ready():
#	change_status.start()
#	if not os.getenv("editor"):
#		user = await client.fetch_user(280116994622357506)
#		await user.send('master updated successfully')
@client.event 
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.reply('dumbass')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.reply("Missing a required argument.")
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.reply('{} is not based enough to do that'.format(ctx.message.author.name))
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.message.reply('1984')
    else:
        print(error) 
@tasks.loop(seconds=10)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

@client.command()
async def ping(ctx):
      await ctx.message.reply(next(ping_cycle))

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason = None):
  if ctx.message.author == user:
	  await ctx.message.reply('you cant kick yourself dumbass')
  elif not reason:
    await user.kick()
    await ctx.message.reply(f"**{user}** has been kicked.")
  else:
    await user.kick(reason=reason)
    await ctx.message.reply(f"**{user}** has been kicked for **{reason}**.")

@client.command()
async def test_me(ctx,):
  test_rng = random.randint(1, 3)
  if test_rng == 1:
    await ctx.message.reply('{} is really shit'.format(ctx.message.author.name))
  elif test_rng == 2:
    await ctx.message.reply('{} is really cute'.format(ctx.message.author.name))
  elif test_rng == 3:
    await ctx.message.reply('{} is pretty cool'.format(ctx.message.author.name))

@client.command()
async def mind_control(ctx, arg1, arg2):
	channel = await client.fetch_channel(arg2)
	await channel.send(arg1)	

@client.command()
@commands.has_permissions(manage_nicknames=True)
async def bot_nick(ctx, *, arg=None):
  try:
      if not arg:
        await ctx.message.guild.me.edit(nick='cute tester')
        await ctx.message.reply('my nickname has been reset')
      else:
        await ctx.message.guild.me.edit(nick=arg)
        await ctx.message.reply(f'nickname changed to {arg}')
  except: 
      await ctx.message.reply('i cant change my own nickname, 1984')

@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.message.reply('{} messages Cleared by {}'.format(limit, ctx.author.mention))

@client.command()
async def FF(ctx):
  await ctx.message.reply(random.choice(final_fantasy_list))

@client.command()
async def smile(ctx):
  await ctx.message.reply(file=discord.File('Sonrie.mp4'))

@client.command()
async def am_lonely(ctx):
  await ctx.message.author.send('ha loser')
  
@client.command()
async def memes(ctx):
  await ctx.message.reply(random.choice(memeslist))

@client.command()
async def impact(ctx):
  if random.randint(0, 1) == 0:
    await ctx.message.reply('hey {} go back to your country'.format(ctx.message.author.name))
  else: 
    await ctx.message.reply('https://tenor.com/view/chainsaw-man-among-us-ass-gif-19571544')

@client.command()
async def help(ctx):
  await ctx.message.reply('look at this nerd they dont know the commands')
  await ctx.message.reply('<:toffsmug:835669251243114526>')

@client.command()
async def cars(ctx):
  await ctx.message.reply(random.choice(carslist))

@client.command()
@commands.has_permissions(manage_emojis=True)
async def create_emote(ctx, url: str, *, name):
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

client.run(os.getenv("TOKEN"))