''' SERVER.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.checks as checks
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils

ALIASES = ['srv']

# > ---------------------------------------------------------------------------
class Server(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, footer):
        title = 'Help Info: {}server'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        description = 'Shows a quick information sheet about the server.\nNot available in DMs!\n\n{}\n**Usage: ** `{}server`'.format(alias, constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.check(not checks.check_is_dm)
    @commands.command(pass_context=True, aliases=ALIASES)
    async def server(self, ctx, *, param):
        if ctx.message.channel.type == discord.ChannelType.private:
            return
        s = ctx.message.channel.guild
        title = 'Server: {}'.format(s.name)
        thumbnail = s.icon_url
        fields = [
            ['Owner', '<@{}>'.format(s.owner_id), False],
            ['Created', s.created_at.strftime('%d.%m.%Y, (%H:%M)'), True], ['Members', str(len(s.members)), True],
            ['Channels', str(len(s.channels)), True], ['Roles', str(len(s.roles)), True], ['Emojis', str(len(s.emojis)), True], [None, True],
            ['Description', s.description, False]
        ]
        footer = { 'text' : 'ID: {}'.format(s.id) }
        await utils.embed_send(ctx, utils.embed_create(title=title, fields=fields, thumbnail=thumbnail, footer=footer))

    @server.error
    async def server_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.server(ctx, param=str(ctx.message.author.id))
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(Server(client))