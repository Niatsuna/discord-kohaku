''' RELOAD.py - Reloads Extensions
    Mainly for testing so that you mustn't restart Kohaku every god damn time.
'''
# -----------------------------------------------------------------------------------------------
# >> Imports
import Bot.Backend.checks as checks
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils

# -----------------------------------------------------------------------------------------------
class Reload(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cmds = {}

    def isSecret(self):
        return True

    @commands.check(checks.check_is_admin)
    @commands.command(pass_context=True)
    async def reload(self, ctx, *, param):
        if self.cmds == {}:
            self.load_cmd_meta()
        success = []
        to_reload = param.lower().replace(',', '').split(' ')
        for tr in to_reload:
            if tr == 'emotes':
                    constants.EMOTES = utils.json_load('Bot/Resources/json/emotes.json')
                    success.append(constants.EMOTES != None)
            elif tr == 'gifs':
                constants.GIFS = utils.json_load('Bot/Resources/json/gifs.json')
                success.append(constants.GIFS != None)
            elif tr == 'all' or tr in self.cmds.keys():
                reload_ = []
                if tr == 'all':
                    for cog in constants.COGS:
                        for (cmd, cog_) in self.cmds.items():
                            if cog == cog_:
                                reload_.append([cog, 'Bot.Cogs.' + cog])
                                break
                elif tr in self.cmds.keys():
                    for cog in constants.COGS:
                        if cog == type(self.cmds[tr]).__name__:
                            reload_.append([cog, 'Bot.Cogs.' + cog])
                            break
                if reload_ == []:
                    success.append(False)
                for r in reload_:
                    try:
                        self.client.reload_extension(r[1])
                        utils.log('> [Reload] Reloaded extension \'{}\''.format(r[0]))
                        success.append(True)
                    except Exception as ex:
                        if isinstance(ex, commands.ExtensionNotLoaded):
                            try:
                                self.client.load_extension(r[1])
                                utils.log('> [Reload] Reloaded extension \'{}\''.format(r[0]))
                                success.append(True)
                            except Exception as ex2:
                                utils.warn('> [Reload] Failed to reload extension {}\n{}'.format(r[0], type(ex2).__name__))
                                success.append(False)
                        else:
                            utils.warn('> [Reload] Failed to reload extension {}\n{}'.format(r[0], type(ex).__name__))
                            success.append(False)
            else:
                utils.warn('> [Reload] Couldn\'t found {}. Maybe it\'s a hidden command.'.format(tr))
                success.append(False)
        fail = len(list(filter(lambda x: not x, success)))
        succ = len(list(filter(lambda x: x, success)))
        if fail == 0:
            await utils.embed_send(ctx, utils.embed_create(title='Reload : Success', description='Successfully reloaded with following parameter(s): \n_`{}`_'.format(', '.join(to_reload))))
        else:
            await utils.embed_send(ctx, utils.embed_create(title='Reload : Fail', description='Couldn\'t reload {} modules ({} succeeded) with following parameter(s) : \n_`{}`_\nPlease check the logs for more information.'.format(fail, succ, ', '.join(to_reload))))


    @reload.error
    async def error_reload(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSIM_PARAM)

    def load_cmd_meta(self):
        for cog in self.client.cogs.values():
            if (not checks.check_is_secret(cog)) and cog.get_commands != []:
                self.cmds[cog.get_commands()[0].name] = cog

# -----------------------------------------------------------------------------------------------
def setup(client):
    client.add_cog(Reload(client))