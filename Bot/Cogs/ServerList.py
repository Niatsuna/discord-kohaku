''' SERVERLIST.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.checks as checks
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from math import ceil

ALIASES = ['sl']

# > ---------------------------------------------------------------------------
class ServerList(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, footer):
        title = 'Help Info: {}server-list'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        description = '**Admin only: ** Shows a list of servers which have access to Kohaku.\n\n{}**Usage: ** `{}server-list`'.format(alias, constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.check(checks.check_is_admin)
    @commands.command(pass_context=True, name='server-list', aliases=ALIASES)
    async def server_list(self, ctx, *, param):
        guilds = self.client.guilds
        title = 'Serverlist'
        description = 'I am currently connected to {} servers.'.format(len(guilds))
        fields = [
            ['Name (Member Count)','ID', False]
        ]
        for i in range(0, len(guilds)):
            guild = guilds[i]
            fields.append(['{} ({})'.format(guild.name, guild.member_count), '_{}_'.format(guild.id), True])
            if i > 0 and i % 2 == 1:
                fields.append([None, True])
        await utils.embed_send(ctx, utils.embed_create(title=title, description=description, fields=fields, thumbnail=self.client.user.avatar_url))

    @server_list.error
    async def server_list_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.server_list(ctx, param='')
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(ServerList(client))