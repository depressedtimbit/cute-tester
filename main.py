import discord
import os
import time
import random
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure, check, CommandNotFound
from itertools import cycle
from lists import carslist
from lists import memes as memeslist
from lists import final_fantasy_list
client = discord.Client()

client = commands.Bot(command_prefix = '!cute ', help_command=None) 

ping_cycle = cycle(['fuck off','leave me alone','i said leave me alone','what do you want','am busy'])
status = cycle(['with Python','fortnight','ur mom', 'TF2', 'the other TF2', 'poland more like pooland'])
@client.event
async def on_ready():
 change_status.start()
 print("connected")
 user = await client.fetch_user(280116994622357506)
 await user.send("bot online")
@client.event 
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('dumbass')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing a required argument.")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('{} is not based enough to do that'.format(ctx.message.author.name))
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send('1984')
    else:
        print(error) 
@tasks.loop(seconds=10)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

@client.command()
async def ping(ctx):
      await ctx.send(next(ping_cycle))

@client.command()
async def test_me(ctx,):
  if ctx.message.author.id == 280116994622357506:
    await ctx.send('{} is really shit'.format(ctx.message.author.name))
  elif ctx.message.author.id == 310824231078330368:
    await ctx.send('{} is really cute'.format(ctx.message.author.name))
  else: await ctx.send('{} is pretty cool'.format(ctx.message.author.name))

@client.command()
async def mind_control(ctx, arg1, arg2):
	channel = await client.fetch_channel(arg2)
	await channel.send(arg1)	

@client.command()
async def bot_nick(ctx, arg):
  if ctx.message.author.id == 280116994622357506:
    try:
        await ctx.message.guild.me.edit(nick=arg)
        await ctx.send('nickname changed to {}'.format(arg))
    except: 
      await ctx.send('i cant change my own nickname, 1984')
  else: 
    raise commands.MissingPermissions
@client.command()
async def bot_nick_reset(ctx):
  if ctx.message.author.id == 280116994622357506:
    try:  
      await ctx.message.guild.me.edit(nick='cute tester')
      await ctx.send('my nickname has been reset') 
    except: 
      await ctx.send('i cant change my own nickname, 1984')
  else: 
     raise commands.MissingPermissions
    
@client.command()
async def FF(ctx):
  await ctx.send(random.choice(final_fantasy_list))

@client.command()
async def smile(ctx):
  await ctx.send(file=discord.File('Sonrie.mp4'))

@client.command()
async def am_lonely(ctx):
  await ctx.message.author.send('ha loser')
  
@client.command()
async def memes(ctx):
  await ctx.send(random.choice(memeslist))

@client.command()
async def impact(ctx):
  if random.randint(0, 1) == 0:
    await ctx.send('hey {} go back to your country'.format(ctx.message.author.name))
  else: 
    await ctx.send('https://tenor.com/view/chainsaw-man-among-us-ass-gif-19571544')

@client.command()
async def help(ctx):
  await ctx.send('look at this nerd they dont know the commands')
  await ctx.send('<:toffsmug:835669251243114526>')

@client.command()
async def cars(ctx):
  await ctx.send(random.choice(carslist))



client.run(os.getenv("TOKEN"))