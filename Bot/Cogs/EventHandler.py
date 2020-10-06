''' EVENTHANDLER.py - Handles bot intern events like on_ready etc. '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
import random
from datetime import datetime

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
        db_path = 'users/{}'.format(message.author.id)
        data = constants.FIRE_CON.get(db_path)
        xp_gain = random.randint(2,10)
        if data == None:
            data = constants.EMPTY_USER
            data['xp'] = xp_gain
            constants.FIRE_CON.setValue(db_path, data)
        else:
            data['xp'] += xp_gain
            if data['xp'] + xp_gain > constants.MAX_EXP:
                data['prestige'] += 1
                data['xp'] += (xp_gain - constants.MAX_EXP)
            constants.FIRE_CON.update(db_path, data)
        now = datetime.utcnow()
        if message.author.id in constants.TIMEOUT.keys() and now < constants.TIMEOUT[message.author.id]:
            return
        elif message.author.id in constants.TIMEOUT.keys(): # now >= constants.TIMEOUT (timeout runned out):
            del (constants.TIMEOUT[message.author.id])
        await self.client.process_commands(message)

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