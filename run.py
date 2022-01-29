import os

import discord
from discord.ext import commands
from discord.ext.commands import when_mentioned_or
import statcord
from pretty_help import DefaultMenu, PrettyHelp

from config import config
from musicbot.audiocontroller import AudioController
from musicbot.settings import Settings
from musicbot.utils import guild_to_audiocontroller, guild_to_settings

initial_extensions = ['musicbot.commands.music', 'musicbot.commands.general', 'musicbot.plugins.button', 'musicbot.plugins.error']
bot = commands.Bot(command_prefix=when_mentioned_or(config.BOT_PREFIX),
                   pm_help=True, case_insensitive=True, intents=discord.Intents.all())
api = statcord.Client(bot,config.STATCORD_KEY)
api.start_loop()

if __name__ == '__main__':

    config.ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
    config.COOKIE_PATH = config.ABSOLUTE_PATH + config.COOKIE_PATH

    if config.BOT_TOKEN == "":
        print("Error: No bot token!")
        exit

    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)


@bot.event
async def on_command(ctx):
    api.command_run(ctx)
@bot.event
async def on_ready():
    print(config.STARTUP_MESSAGE)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Music, type {}help".format(config.BOT_PREFIX)))

    for guild in bot.guilds:
        await register(guild)
        print("Joined {0}, owned by {1}#{2}".format(guild.name,guild.owner.name,guild.owner.discriminator))

    menu = DefaultMenu('◀️', '▶️', '❌')
    bot.help_command = PrettyHelp(navigation=menu, color=discord.Colour.green())

    print(config.STARTUP_COMPLETE_MESSAGE)


@bot.event
async def on_guild_join(guild):
    print("Added to {0}, owned by {1}#{2}".format(guild.name,guild.owner.name,guild.owner.discriminator))
    await register(guild)


async def register(guild):

    guild_to_settings[guild] = Settings(guild)
    guild_to_audiocontroller[guild] = AudioController(bot, guild)

    sett = guild_to_settings[guild]

    try:
        await guild.me.edit(nick=sett.get('default_nickname'))
    except:
        pass

    if config.GLOBAL_DISABLE_AUTOJOIN_VC == True:
        return

    vc_channels = guild.voice_channels

    if sett.get('vc_timeout') == False:
        if sett.get('start_voice_channel') == None:
            try:
                await guild_to_audiocontroller[guild].register_voice_channel(guild.voice_channels[0])
            except Exception as e:
                print(e)

        else:
            for vc in vc_channels:
                if vc.id == sett.get('start_voice_channel'):
                    try:
                        await guild_to_audiocontroller[guild].register_voice_channel(vc_channels[vc_channels.index(vc)])
                    except Exception as e:
                        print(e)


bot.run(config.BOT_TOKEN, bot=True, reconnect=True)
