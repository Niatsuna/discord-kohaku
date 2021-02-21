''' TIMEOUT.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.checks as checks
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from datetime import datetime, timedelta
from copy import deepcopy

ALIASES = ['t', 'to']

# > ---------------------------------------------------------------------------
class Timeout(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, footer):
        title = 'Help Info: {}timeout'.format(constants.INVOKE)
        description = 'Timeouts a user from using commands\nCan only be used by moderators or higher!\n\n**Usage: ** `{}timeout` `<mention/id>` `<seconds>`'.format(constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.check(checks.check_is_mod)
    @commands.command(pass_context=True, aliases=ALIASES)
    async def timeout(self, ctx, *, param):
        param = param.split(' ')
        param[0] = param[0].replace('<', '').replace('@', '').replace('!', '').replace('>', '')
        try:
            id_ = int(param[0])
        except:
            id_ = -1
        user = self.client.get_user(id_)
        if user == None:
            await utils.embed_send(ctx, utils.embed_create(title='User not found.', description='Couldn\'t find user with id/mention: `{}`'.format(param[0])))
            return

        caller_key = str(ctx.message.author.id)
        user_key = str(id_)
        user = self.client.get_user(int(user_key))
        if user == None:
            await utils.embed_send(ctx, utils.embed_create(title='User not found.', description='Couldn\'t find user with id/mention: `{}`'.format(param[1])))
            return
        if caller_key not in constants.USER_DATA.keys():
            constants.USER_DATA[caller_key] = deepcopy(constants.EMPTY_USER)
        caller = constants.USER_DATA[caller_key]

        if user_key not in constants.USER_DATA.keys():
            constants.USER_DATA[user_key] = deepcopy(constants.EMPTY_USER)
        data = constants.USER_DATA[user_key]

        if caller['rank'] <= data['rank']:
            await utils.embed_send(ctx, constants.ERROR_PERMISSION_DENIED)
            return
        
        try:
            t = int(param[1])
        except:
            await utils.embed_send(ctx, utils.embed_create(title='Invalid Parameter', description='Please enter a valid amount of seconds!'))
            return
        until = datetime.utcnow() + timedelta(seconds=t)
        constants.TIMEOUT[id_] = until
        await utils.embed_send(ctx, utils.embed_create(title='Timeout: {} - {} UTC'.format(user.display_name, datetime.utcnow().strftime('%d.%m.%Y, (%H:%M:%S)')), description='<@{}> got timeouted by <@{}> for {} seconds!\nTimeout until: {} (UTC)'.format(id_,ctx.message.author.id, t, until.strftime('%d.%m.%Y, (%H:%M:%S)'))))

    @timeout.error
    async def timeout_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSING_PARAM)
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(Timeout(client))