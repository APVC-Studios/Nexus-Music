from multiprocessing.connection import Listener
import discord
from discord.ext import commands


class CogName(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.Listener()
    async def on_command_error(ctx, error):
        print(error)

        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title="Command not found", description=f"```{error}```")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="You don't have permission to do that!", description=f"```{error}```")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="You are missing a required argument!", description=f"```{error}```")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="Invalid argument!", description=f"```{error}```")
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandError) or isinstance(error,commands.CommandInvokeError):
            await ctx.message.add_reaction('❌')
            try:
                embed = discord.Embed(title="An error has occured!", description=f"```{error}```")
                await ctx.send(embed=embed)
            except:
                await ctx.send("An error has occured!")
        else: 
            await ctx.send("An unknown error has occured!")


def setup(bot:commands.Bot):
    bot.add_cog(CogName(bot))