''' UPDATE.py - Updates resources.'''
# -----------------------------------------------------------------------------------------------
# >> Imports
import Bot.Backend.checks as checks
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from Bot.Backend.update_scripts import ac, dbd, fgo, pkm

# -----------------------------------------------------------------------------------------------
class Update(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.scripts = {
            'ac' : ac,
            'dbd': dbd,
            'fgo': fgo,
            'pkm': pkm
        }
        self.update_all()

    def isSecret(self):
        return True

    @commands.check(checks.check_is_admin)
    @commands.command(pass_context=True)
    async def update(self, ctx, *, param):
        if param.lower() in self.scripts.keys():
            try:
                self.scripts[param.lower()].update()
                await utils.embed_send(ctx, utils.embed_create(title='Update : Success', description='Successfully updated the resources connected to the command `{}`'.format(param.lower())))
            except Exception as ex:
                utils.warn('> [Update] Error during Update: {}'.format(ex))
                await utils.embed_send(ctx, constants.ERROR_WHOOPS)
        else:
            await utils.embed_send(ctx, constants.ERROR_SEARCH_FAIL)

    def update_all(self):
        for (k,v) in self.scripts.items():
            try:
                if utils.json_load(v.PATH) == None:
                    v.update()
                    utils.log('> [Update] Updated during start: {}'.format(k))
                else:
                    utils.log('> [Update] Skipped updating at start: {}'.format(k))
            except Exception as ex:
                utils.warn('> [Update] Error during Update: {} | {}'.format(k ,ex))

    @update.error
    async def error_update(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSIM_PARAM)

# -----------------------------------------------------------------------------------------------
def setup(client):
    client.add_cog(Update(client))