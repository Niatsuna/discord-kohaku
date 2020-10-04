''' RELOAD.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.checks as checks
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from math import ceil

ALIASES = ['r', 'rl']

# > ---------------------------------------------------------------------------
class Reload(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cmds = {}

    def help(self, footer):
        title = 'Help Info: {}reload'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        description = 'Reloads a command / module\nSending with the keyword `all` will reload all commands / modules.\n Can only be used by admins or higher!\n\n{}**Usage: ** `{}reload` `[<cmd/module>]`'.format(alias, constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.check(checks.check_is_admin)
    @commands.command(pass_context=True, aliases=ALIASES)
    async def reload(self, ctx, *, param):
        param = param.lower().split(' ')
        if self.cmds == {}:
            self.load_cmd_meta()
        if param[0].lower() == 'all':
            param = self.cmds.keys()
        success = []
        failed = []
        for p in param:
            if p in self.cmds.keys():
                cog = 'Bot.Cogs.' + type(self.cmds[p]).__name__
                try:
                    self.client.reload_extension(cog)
                    utils.log('> [Reload] Reloaded extension with key \'{}\''.format(p))
                    success.append(p)
                except commands.ExtensionNotLoaded:
                    try:
                        self.client.load_extension(cog)
                        utils.log('> [Reload] Reloaded extension with key \'{}\''.format(p))
                        success.append(p)
                    except Exception as ex:
                        utils.warn('> [Reload] Failed to reload extension with key {}\n{}'.format(p, type(ex).__name__))
                        failed.append(p)
                except Exception as ex2:
                    utils.warn('> [Reload] Failed to reload extension with key {}\n{}'.format(p, type(ex2).__name__))
                    failed.append(p)
            else:
                utils.warn('> [Reload] Failed to reload extension with key {}\nNo such Extension.'.format(p))
                failed.append(p)
        if len(failed) == 0:
            await utils.embed_send(ctx, utils.embed_create(title='Reload: Success', description='Successfully reloaded modules with following keys:\n{}'.format(', '.join(['`{}`'.format(x) for x in success]))))
            return
        else:
            await utils.embed_send(ctx, utils.embed_create(title='Reload: Failed', description='Failed to reload {} modules ({} succeeded) with following keys:\n{}'.format(len(failed), len(success),', '.join(['`{}`'.format(x) for x in failed]))))

    @reload.error
    async def reload_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSING_PARAM)
            return

    def load_cmd_meta(self):
        for cog in self.client.cogs.values():
            if not checks.check_is_secret(cog) and cog.get_commands() != []:
                cmd = cog.get_commands()[0]
                self.cmds[cmd.name] = cog
                for alias in cmd.aliases:
                    self.cmds[alias] = cog


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(Reload(client))