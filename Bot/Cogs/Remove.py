''' REMOVE.py - Removes admins, gifs or emotes'''
# -----------------------------------------------------------------------------------------------
# >> Imports
import Bot.Backend.checks as checks
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils

# -----------------------------------------------------------------------------------------------
class Remove(commands.Cog):

    def __init__(self, client):
        self.client = client

    def isSecret(self):
        return True

    @commands.check(checks.check_is_admin)
    @commands.command(pass_context=True)
    async def remove(self, ctx, *, param):
        params = param.split(' ')
        if params[0].lower() == 'admin' and len(params) >= 2:
            if checks.check_is_owner(ctx):
                admins = utils.json_load('Bot/Resources/json/admin.json')
                result = []
                for user in params[1:]:
                    try:
                        _id = int(user.replace('<', '').replace('@', '').replace('!','').replace('>', ''))
                    except:
                        _id = -1
                    if _id != -1:
                        try:
                            admins['admins'].remove(_id)
                            result.append([user, True])
                        except:
                            result.append([user, False])
                    else:
                        result.append([user, False])
                utils.json_store('Bot/Resources/json/admin.json', admins)
                fail = list(filter(lambda x: not x[1], result))
                succ = len(list(filter(lambda x: x[1], result)))
                if len(fail) == 0:
                    await utils.embed_send(ctx, utils.embed_create(title='Remove : Success', description='Successfully removed the requested users from their admin position.'))
                else:
                    await utils.embed_send(ctx, utils.embed_create(title='Remove : Fail', description='Couldn\'t remove the following ids from admins: \n_`{}`_ ({} succeeded)'.format(', '.join([x[0] for x in fail]), succ)))
            else:
                await utils.embed_send(ctx, constants.ERROR_PERMISSION_DENIED)
            return
        elif params[0].lower() == 'gif' and len(params) >= 2:
            if params[1] in constants.GIFS.keys():
                del (constants.GIFS[params[1]])
                utils.json_store('Bot/Resources/json/gifs.json', constants.GIFS)
                await utils.embed_send(ctx, utils.embed_create(title='Remove : Success', description='Successfully removed gif from intern list.'))
            else:
                await utils.embed_send(ctx, utils.embed_create(title='Remove : Fail', description='Couldn\'t found gif with given key.'))
            return
        elif params[0].lower() == 'emote' and len(params) >= 2:
            if params[1] in constants.EMOTES.keys():
                del (constants.EMOTES[params[1]])
                utils.json_store('Bot/Resources/json/emotes.json', constants.EMOTES)
                await utils.embed_send(ctx, utils.embed_create(title='Remove : Success', description='Successfully removed emote from intern list.'))
            else:
                await utils.embed_send(ctx, utils.embed_create(title='Remove : Fail', description='Couldn\'t found emote with given key.'))
            return
        await utils.embed_send(ctx, constants.ERROR_MISSIM_PARAM)

    @remove.error
    async def error_remove(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSIM_PARAM)


# -----------------------------------------------------------------------------------------------
def setup(client):
    client.add_cog(Remove(client))