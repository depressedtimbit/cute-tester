import discord
import os
import discord.ext
from discord.ext import commands, tasks
from itertools import cycle
client = discord.Client()

client = commands.Bot(
command_prefix = commands.when_mentioned_or('!cute '),
help_command = None,
allowed_mentions = discord.AllowedMentions(
  users=False, 
  everyone=False, 
  roles=False, 
  replied_user=False
  )
)

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.load_extension(f"cogs.{name}")
        print(f'loaded {name}')

status = cycle(['fortnight','ur mom', 'TF2', 'the other TF2'])

@client.event 
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.reply('dumbass')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.reply("Missing a required argument.")
    elif isinstance(error, commands.MissingPermissions or commands.NotOwner):
        await ctx.message.reply(f'{ctx.message.author.name} is not based enough to do that')
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.message.reply('1984')
    else:
        print(error) 

@client.event
async def on_ready():
	change_status.start()

@client.command()
@commands.is_owner()
async def die(ctx):
  await ctx.send("<:qtdie:878143099430400032>")
  for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.reload_extension(f"cogs.{name}")
        await ctx.send(f'reloaded {name}')

@tasks.loop(seconds=10)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

client.run(os.getenv("TOKEN"))