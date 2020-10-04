''' ADD.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.checks as checks
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils

ALIASES = []
LISTS = [('gif', 3), ('emote', 3), ('moderator', 2), ('admin', 2), ('owner', 2)]

# > ---------------------------------------------------------------------------
class Add(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, footer):
        title = 'Help Info: {}add'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        description = 'Adds someone / something to a list.\nCan only be used by admins or higher!\nLists are: gif, emote and the specific ranks.\n\n{}**Usage: ** `{}add` `<list>` `(<key>)` `<gif-url/emote/person>`'.format(alias, constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.check(checks.check_is_admin)
    @commands.command(pass_context=True, aliases=ALIASES)
    async def add(self, ctx, *, param):
        param = param.lower().split(' ')
        for (k, amount) in LISTS:
            if param[0] == k and len(param) < amount:
                await utils.embed_send(ctx, constants.ERROR_MISSING_PARAM)
                return
            elif param[0] == k:
                break
        if param[0] == 'gif' or param[0] == 'emote':
            key = param[1]
            constants.FIRE_CON.setValue('{}/{}'.format(param[0], key), param[2])
            await utils.embed_send(ctx, utils.embed_create(title='Added {}'.format(param[0]), description='{}, added a {} with the key `{}`.'.format(ctx.message.author.mention, param[0], param[1])))
            return

        rank = None
        for (i, x) in constants.RANK_MAP.items():
            if x.lower() == param[0]:
                rank = i
                param[0] = x
                break
        if rank == None:
            await utils.embed_send(ctx, utils.embed_create(title='Add : Failed', description='Couldn\'t find list. Please check your spelling or contact an admin!'))
            return
        caller = constants.FIRE_CON.get('users/{}'.format(ctx.message.author.id))
        if caller['rank'] <= rank:
            await utils.embed_send(ctx, constants.ERROR_PERMISSION_DENIED)
            return
        user = self.client.get_user(int(param[1].replace('<', '').replace('@', '').replace('!', '').replace('>', '')))
        if user == None:
            await utils.embed_send(ctx, utils.embed_create(title='User not found.', description='Couldn\'t find user with id/mention: `{}`'.format(param[1])))
            return
        data = constants.FIRE_CON.get('users/{}'.format(user.id))
        if data == None:
            data = {'prestige' : 0, 'xp' : 0}
        data['rank'] = rank
        constants.FIRE_CON.setValue('users/{}'.format(user.id), data)
        await utils.embed_send(ctx, utils.embed_create(title='Added {} to role {}'.format(user.display_name, param[0]), description='{} gave {} the role `{}`.'.format(ctx.message.author.mention, user.mention, param[0]),))

    @add.error
    async def add_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSING_PARAM)
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(Add(client))