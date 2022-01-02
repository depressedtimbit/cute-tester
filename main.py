import discord
import os
import discord.ext
from discord.ext import commands, tasks
from itertools import cycle
from dotenv import load_dotenv

load_dotenv()

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
        await ctx.send('dumbass')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing a required argument.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.message.author.name} is not based enough to do that')
    elif isinstance(error, commands.NotOwner):
        await ctx.send(f'{ctx.message.author.name} is not based enough to do that')
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send('1984')
    else:
        ctx.send(error) 

@client.event
async def on_ready():
	change_status.start()

@tasks.loop(seconds=10)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

try:
    client.run(os.environ["TOKEN"])
except KeyError: 
    print("TOKEN does not exist")
