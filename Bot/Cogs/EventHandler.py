''' EVENTHANDLER.py - Handles bot intern events like on_ready etc. '''
# > ---------------------------------------------------------------------------
# > Imports
from copy import deepcopy
import discord
from discord.ext import commands, tasks
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
import random
from datetime import datetime

# > ---------------------------------------------------------------------------
class EventHandler(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.ignore = [commands.errors.MissingRequiredArgument, commands.errors.CommandNotFound]

        constants.USER_DATA = constants.FIRE_CON.get('users')
        if constants.USER_DATA == None:
            constants.FIRE_CON.setValue('users', {})
            constants.USER_DATA = {}

        self.prev_data = deepcopy(constants.USER_DATA)
        self.update_user_data.start()

    def isSecret(self):
        return True

    def cog_unload(self):
        self.update_user_data.cancel()

    @tasks.loop(minutes=10)
    async def update_user_data(self):
        changes = False
        for (k, v) in constants.USER_DATA.items():
            if (k in self.prev_data.keys() and self.prev_data[k] != constants.USER_DATA[k] ) or (k not in self.prev_data.keys()) :
                changes = True
                break
        if changes:
            utils.log('Updated Database!')
            if constants.FIRE_CON.get('users') == None:
                constants.FIRE_CON.setValue('users', constants.USER_DATA)
            else:
                constants.FIRE_CON.update('users', constants.USER_DATA)
            self.prev_data = deepcopy(constants.USER_DATA)

    @update_user_data.before_loop
    async def before_update(self):
        await self.client.wait_until_ready()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        r_mentions = False
        if message.role_mentions != []:
            g = message.guild
            for role in message.role_mentions:
                id_ = role.id
                r = g.get_role(id_)
                if r != None and self.client.user in r.members:
                    r_mentions = True
        if r_mentions or self.client.user.mentioned_in(message):
            await message.channel.send(utils.load_emote('kohaku-ping'))


        key = str(message.author.id)
        xp_gain = random.randint(2,10)
        if key in constants.USER_DATA.keys():
            data = constants.USER_DATA[key]
        else:
            data = deepcopy(constants.EMPTY_USER)
        data['xp'] += xp_gain
        if data['xp'] > constants.MAX_EXP:
            data['prestige'] += 1
            data['xp'] -= constants.MAX_EXP
        constants.USER_DATA[key] = data
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