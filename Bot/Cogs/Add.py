''' ADD.py - Adds admins, gifs or emotes'''
# -----------------------------------------------------------------------------------------------
# >> Imports
import Bot.Backend.checks as checks
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils

# -----------------------------------------------------------------------------------------------
class Add(commands.Cog):

    def __init__(self, client):
        self.client = client

    def isSecret(self):
        return True

    @commands.check(checks.check_is_admin)
    @commands.command(pass_context=True)
    async def add(self, ctx, *, param):
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
                    u = self.client.get_user(_id)
                    if u == None or admins == None:
                        result.append([user, _id, False])
                    else:
                        if _id not in admins['admins']:
                            admins['admins'] = [*admins['admins'], _id]
                        result.append([user, _id, True, u])
                utils.json_store('Bot/Resources/json/admin.json', admins)
                fail = list(filter(lambda x: not x[2], result))
                succ = len(list(filter(lambda x: x[2], result)))
                if len(fail) == 0:
                    await utils.embed_send(ctx, utils.embed_create(title='Add : Success', description='Successfully added the following users as admins: \n_`{}`_'.format(', '.join([x[-1].display_name for x in result]))))
                else:
                    await utils.embed_send(ctx, utils.embed_create(title='Add : Fail', description='Couldn\'t add the following users as admins: \n_`{}`_ ({} succeeded)'.format(', '.join([x[0] for x in fail]), succ)))
            else:
                await utils.embed_send(ctx, constants.ERROR_PERMISSION_DENIED)
            return
        elif params[0].lower() == 'gif' and len(params) >= 3:
            key = params[1]
            url = params[2]
            if constants.GIFS == None:
                await utils.embed_send(ctx, utils.embed_create(title='Add : Fail', description='Couldn\'t add the requested gif. Please contact an admin.'))
            else:
                constants.GIFS[key] = url
                utils.json_store('Bot/Resources/json/gifs.json', constants.GIFS)
                await utils.embed_send(ctx, utils.embed_create(title='Add : Success', description='Successfully added the requested gif.'))
            return
        elif params[0].lower() == 'emote' and len(params) >= 2:
            key = params[1]
            emote = params[2]
            if constants.EMOTES == None:
                await utils.embed_send(ctx, utils.embed_create(title='Add : Fail', description='Couldn\'t add the requested emote. Please contact an admin.'))
            else:
                constants.EMOTES[key] = emote
                utils.json_store('Bot/Resources/json/emotes.json', constants.EMOTES)
                await utils.embed_send(ctx, utils.embed_create(title='Add : Success', description='Successfully added the requested emote.'))
            return
        await utils.embed_send(ctx, constants.ERROR_MISSIM_PARAM)

    @add.error
    async def error_add(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSIM_PARAM)

# -----------------------------------------------------------------------------------------------
def setup(client):
    client.add_cog(Add(client))