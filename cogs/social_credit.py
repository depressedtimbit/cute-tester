import discord
from discord.ext import commands
import sqlite3
from lists import bad_citizen, good_citizen

class social_credit(commands.Cog):
  
    def __init__(self, bot: commands.Bot):
            self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        content = ctx.content.lower()
        if content in bad_citizen:
            await ctx.reply('MESSAGE FROM THE MINISTRY OF STATE\n(我们的) 100 Social Credits have been removed from your account!  Bad work citizen, Do not publicly disclose your opinion which can make our holy state look bad. Glory to the Chinese Communist Party! https://cdn.discordapp.com/attachments/780610992388177920/1032776850503639131/CCP.mp4')
            await self.update_credit(ctx.author, -10000)
        elif content in good_citizen:
            await ctx.reply('MESSAGE FROM THE MINISTRY OF STATE\n(我们的) 15 Social Credits have been added to your account! good work citizen. Glory to the Chinese Communist Party! https://cdn.discordapp.com/attachments/780610992388177920/1032776850503639131/CCP.mp4')
            await self.update_credit(ctx.author, 1500)
        elif  "social_credit" in content: pass
        else:
            await self.update_credit(ctx.author, 100)

    @commands.command()
    async def social_credit(self, ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT credit FROM social_credit WHERE citizen_id = {ctx.author.id}')
        result = cursor.fetchone()
        if result is None:
            cursor.execute(f"INSERT INTO social_credit(citizen_id) VALUES({ctx.author.id})")
        cursor.execute(f'SELECT credit FROM social_credit WHERE citizen_id = {ctx.author.id}')
        result = cursor.fetchone()
        result = str(result[0])
        await ctx.reply(f'MESSAGE FROM THE MINISTRY OF STATE\n(我们的) good work citizen, your Social credit score is currently {result[:-2]}!\n Glory to the Chinese Communist Party!')
        db.commit()
        db.close()
    async def update_credit(self, user, amount): 
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT citizen_id FROM social_credit WHERE citizen_id = {user.id}')
        result = cursor.fetchone()
        if result is None:
            cursor.execute(f"INSERT INTO social_credit(citizen_id) VALUES({user.id})")
            db.commit()
        cursor.execute(f'UPDATE social_credit SET credit = credit + {int(amount)} WHERE citizen_id = {user.id}')
        db.commit()
        db.close()
        
        

def setup(bot):
    bot.add_cog(social_credit(bot))