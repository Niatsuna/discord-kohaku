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

    @commands.check(checks.check_is_guild)
    @commands.command(pass_context=True, aliases=ALIASES)
    async def server(self, ctx, *, param):
        s = ctx.message.channel.guild
        title = 'Server: {}'.format(s.name)
        thumbnail = s.icon_url
        leaderboard = self.leaderboard(s)
        fields = [
            ['Owner', '<@{}>'.format(s.owner_id), False],
            ['Created', s.created_at.strftime('%d.%m.%Y, (%H:%M)'), True], ['Members', str(len(s.members)), True],
            ['Channels', str(len(s.channels)), True], ['Roles', str(len(s.roles)), True], ['Emojis', str(len(s.emojis)), True], [None, True],
            ['Top 5 | Rank', '\n'.join(leaderboard[0]), True], ['Top 5 | XP', '\n'.join(leaderboard[1]), True]
        ]
        footer = { 'text' : 'ID: {}'.format(s.id) }
        await utils.embed_send(ctx, utils.embed_create(title=title, fields=fields, thumbnail=thumbnail, footer=footer))

    def leaderboard(self, guild):
        members = []
        for mem in guild.members:
            if not mem.bot:
                db_path = 'users/{}'.format(mem.id)
                data = constants.FIRE_CON.get(db_path)
                if data == None:
                    data = constants.EMPTY_USER
                members.append([mem, data])
        members_rank = sorted(members, key=(lambda x: x[1]['rank']), reverse=True)
        members_xp = sorted(members, key=(lambda x: x[1]['xp']), reverse=True)
        leaderboard = [[],[]]
        for i in range(0, min(5,len(members_rank))):
            entry = members_rank[i]
            leaderboard[0].append('{} ({})'.format(entry[0].mention, constants.RANK_MAP[entry[1]['rank']]))
        for i in range(0, min(5,len(members_xp))):
            entry = members_xp[i]
            leaderboard[1].append('{} (Lvl {})'.format(entry[0].mention, utils.level(entry[1]['xp'])))
        return leaderboard

    @server.error
    async def server_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.server(ctx, param=str(ctx.message.author.id))
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(Server(client))