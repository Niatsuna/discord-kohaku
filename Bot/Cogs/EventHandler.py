''' EVENTHANDLER.py - Handles bot intern events like on_ready etc. '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils

# > ---------------------------------------------------------------------------
class EventHandler(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.ignore = [commands.errors.MissingRequiredArgument, commands.errors.CommandNotFound]

    def isSecret(self):
        return True

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        for (key, gif) in constants.GIFS.items():
            if key in message.content.lower().split(' '):
                await message.channel.send(embed=utils.embed_create(image=gif))

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='{}help'.format(constants.INVOKE)))
        utils.log('[Kohaku] Initialization complete! >>')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        for ign in self.ignore:
            if isinstance(error, ign):
                return
        if isinstance(error, commands.CheckFailure):
            await ctx.message.channel.send(embed=constants.ERROR_PERMISSION_DENIED)
            return
        exc = '{}: {}'.format(type(error).__name__, error)
        raise error

# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(EventHandler(client))