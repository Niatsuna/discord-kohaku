''' REMOVE.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.checks as checks
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils

ALIASES = ['rem', 'del']
LISTS = ['gif', 'emote', 'moderator', 'admin', 'owner']

# > ---------------------------------------------------------------------------
class Remove(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, footer):
        title = 'Help Info: {}remove'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        description = 'Remove someone / something of a list.\nCan only be used by admins or higher!\nLists are: gif, emote and the specific ranks.\n\n{}**Usage: ** `{}remove` `<list>` `<key/person>`'.format(alias, constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.check(checks.check_is_admin)
    @commands.command(pass_context=True, aliases=ALIASES)
    async def remove(self, ctx, *, param):
        param = param.lower().split(' ')
        if len(param) > 1 and param[0] in LISTS:
            if param[0] == 'gif' or param[0] == 'emote':
                constants.FIRE_CON.delete('{}/{}'.format(param[0], param[1]))
            else:
                id_ = int(param[1].replace('<', '').replace('@', '').replace('!', '').replace('>', ''))
                user = constants.FIRE_CON.get('users/{}'.format(id_))
                if user == None:
                    await utils.embed_send(ctx, utils.embed_create(title='User not found.', description='Couldn\'t find user with id/mention: `{}`'.format(param[1])))
                    return
                caller = constants.FIRE_CON.get('users/{}'.format(ctx.message.author.id))
                if caller['rank'] <= user['rank']:
                    await utils.embed_send(ctx, constants.ERROR_PERMISSION_DENIED)
                    return
                constants.FIRE_CON.update('users/{}'.format(id_), {'rank' : 0})
            await utils.embed_send(ctx, utils.embed_create(title='Removed: {} from {}'.format(param[1] if param[0] == 'gif' or param[0] == 'emote' else self.client.get_user(id_).display_name, param[0])))
            return
        await utils.embed_send(ctx, constants.ERROR_MISSING_PARAM)

    @remove.error
    async def remove_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSING_PARAM)
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(Remove(client))