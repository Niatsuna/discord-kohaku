''' STATUS.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from math import floor
from copy import deepcopy

ALIASES = ['s', 'profile', 'pr']

# > ---------------------------------------------------------------------------
class Status(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, footer):
        title = 'Help Info: {}status'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        description = 'Shows the profile(s) of named user(s).\nSending without parameters will show the profile of the author.\n{}\n**Usage: ** `{}status` `([<mention>/<id>])`'.format(alias, constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.command(pass_context=True,  aliases=ALIASES)
    async def status(self, ctx, *, param):
        param = param.split(' ')
        for i in range(0, len(param)):
            param[i] = param[i].replace('<', '').replace('@', '').replace('!', '').replace('>', '')
        for p in param:
            try:
                id_ = int(p)
            except:
                id_ = -1
            user = self.client.get_user(id_)
            if user == None:
                await utils.embed_send(ctx, utils.embed_create(title='Profile not found.', description='Couldn\'t find user with id/mention: `{}`'.format(p)))
            elif not user.bot:
                key = str(id_)
                if key in constants.USER_DATA.keys():
                    data = deepcopy(constants.USER_DATA[key])
                else:
                    data = constants.EMPTY_USER
                    constants.USER_DATA[key] = data
                mem = ctx.message.guild.get_member(id_)
                title = 'Profile: {}'.format(user.display_name if mem == None else mem.display_name)
                thumbnail = user.avatar_url
                lvl = utils.level(data['xp'])
                description = '**Level: ** {} ({}%)'.format(lvl, floor((data['xp']-utils.total_exp(lvl))/utils.total_exp(lvl+1) * 100))
                if data['prestige'] > 0:
                    description += ' | **Prestige: ** {}'.format(data['prestige'])
                description += '\n**Rank: ** {}\n**Created Account: ** {}'.format(constants.RANK_MAP[data['rank']], user.created_at.strftime('%d.%m.%Y, (%H:%M)'))
                fields = []
                if data['description'] != '-':
                    fields.append(['Description', data['description'], False])
                await utils.embed_send(ctx, utils.embed_create(title=title, description=description, fields=fields, thumbnail=thumbnail))

    @status.error
    async def status_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.status(ctx, param=str(ctx.message.author.id))
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(Status(client))