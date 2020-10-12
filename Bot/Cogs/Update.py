''' UPDATE.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.checks as checks
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
import time

# > Updateable
from Bot.Cogs.AnimalCrossing import AnimalCrossing
from Bot.Cogs.GenshinImpact import GenshinImpact

ALIASES = ['u']

# > ---------------------------------------------------------------------------
class Update(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cmds = {}
        self.types = [AnimalCrossing, GenshinImpact]

    def help(self, footer):
        title = 'Help Info: {}update'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        description = 'Update resources for a module.\nSending the key `all` will update all resources.\nCan only be used by moderators or higher!\n\n{}**Usage: ** `{}update` `<alias/name>`'.format(alias, constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.check(checks.check_is_mod)
    @commands.command(pass_context=True, aliases=ALIASES)
    async def update(self, ctx, *, param):
        param = param.lower().split(' ')
        if self.cmds == {}:
            self.cmds = utils.load_cmd_meta(self.client)

        if param[0] == 'all':
            param = list(filter(lambda x : type(self.cmds[x]) in self.types, utils.load_cmd_meta(self.client, with_aliases=False).keys())) # Please don't update one resource more then one time, thanks <3
        success = []
        failed = []
        message = await utils.embed_send(ctx, utils.embed_create(title='Updating...', description='Updating {} modules.'.format(len(param))))
        start = time.time()
        for arg in param:
            if arg in self.cmds.keys() and type(self.cmds[arg]) in self.types:
                try:
                    await self.cmds[arg].update()
                    success.append(arg)
                except:
                    failed.append(arg)
            else:
                failed.append(arg)
        footer = {'text' : 'Time: {}s'.format(round(time.time() - start, 2))}
        if len(failed) == 0:
            await message.edit(embed=utils.embed_create(title='Update : Success', description='Updated successfully {} modules.'.format(len(success)), footer=footer))
        else:
            await message.edit(embed=utils.embed_create(title='Update : Failed', description='Couldn\'t update {} modules ({} successfull).\nFailed modules were with the following keys:\n{}'.format(
                len(failed), len(success), ', '.join(['`{}`'.format(x) for x in failed])), footer=footer))

    @update.error
    async def update_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_create(ctx, constants.ERROR_MISSING_PARAM)
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(Update(client))