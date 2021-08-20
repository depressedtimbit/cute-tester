import discord
from discord.ext import commands
import random
import asyncio
from lists import carslist
from lists import memes as memeslist
from lists import final_fantasy_list

class fun(commands.Cog):
  
  def __init__(self, bot: commands.Bot):
        self.bot = bot
  
  @commands.command()
  async def cute_test(self, ctx, testname=None):
    if not testname: testname = ctx.message.author.name
    await ctx.message.reply(random.choice(
    [
    f'{testname} is really shit',
    f'{testname} is really cute', 
    f'{testname} is pretty cool'
    ]
    ))

  @commands.command()
  async def FF(self, ctx):
    await ctx.message.reply(random.choice(final_fantasy_list))

  @commands.command()
  async def smile(self, ctx):
   await ctx.message.reply(file=discord.File('Sonrie.mp4'))

  @commands.command()
  async def am_lonely(self, ctx):
   await ctx.message.author.send('ha loser')
   await ctx.message.add_reaction(':jahysmile:871869041709572137')
  
  @commands.command()
  async def memes(self, ctx):
    await ctx.message.reply(random.choice(memeslist))

  @commands.command()
  async def impact(self, ctx):
    if random.randint(0, 5) == 0:
     await ctx.message.reply(f'hey {ctx.message.author.name} go back to your country')
    else: 
      await ctx.message.reply('https://tenor.com/view/chainsaw-man-among-us-ass-gif-19571544')

  @commands.command()
  async def cars(self, ctx):
    await ctx.message.reply(random.choice(carslist))

  @commands.command()
  async def dice(self, ctx, arg="d20"):
    try: 
      arg = arg.lower()
      dieroll,dietype = arg.split("d", 2)
      if not dieroll: dieroll = 1
      dieroll = int(dieroll)
      dietype = int(dietype)
      if dieroll > 10: dieroll = 10
      await ctx.message.reply(f'rolling a {dieroll}d{dietype}...')
      while dieroll > 0:
        dice_rng = random.randint(1, dietype)
        await asyncio.sleep(1)
        await ctx.send(dice_rng)
        dieroll = dieroll - 1
    except:
     await ctx.message.reply('you messed it up bro you gonna do it like dnd style')

def setup(bot):
    bot.add_cog(fun(bot))