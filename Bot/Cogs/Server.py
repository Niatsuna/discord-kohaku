''' SERVER.py '''
# > ---------------------------------------------------------------------------
# > Imports
import discord
from discord.ext import commands
import Bot.Backend.checks as checks
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from concurrent.futures import ThreadPoolExecutor
from math import ceil

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
        description = 'Shows a quick information sheet about the server.\nNot available in DMs!\n\n{}\n**Usage: ** `{}server (<id>)`'.format(alias, constants.INVOKE)
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.check(checks.check_is_guild)
    @commands.command(pass_context=True, aliases=ALIASES)
    async def server(self, ctx, *, param):
        param = int(param.replace('<', '').replace('@', '').replace('!', '').replace('>', ''))
        s = self.client.get_guild(param)
        if s == None:
            await utils.embed_send(ctx, constants.ERROR_SEARCH_FAIL)
            return
        title = 'Server: {}'.format(s.name)
        thumbnail = s.icon_url
        fields = [
            ['Owner', '<@{}>'.format(s.owner_id), False],
            ['Created', s.created_at.strftime('%d.%m.%Y, (%H:%M)'), True], ['Members', str(len(s.members)), True],
            ['Channels', str(len(s.channels)), True], ['Roles', str(len(s.roles)), True], ['Emojis', str(len(s.emojis)), True], [None, True],
            ['Top 5 | Rank', 'Please wait ...', True], ['Top 5 | XP', 'Please wait ...', True]
        ]
        footer = { 'text' : 'ID: {}'.format(s.id) }
        message = await utils.embed_send(ctx, utils.embed_create(title=title, fields=fields, thumbnail=thumbnail, footer=footer))
        leaderboard = self.leaderboard(s)

        fields[-2] = ['Top 5 | Rank', '\n'.join(leaderboard[0]), True]
        fields[-1] = ['Top 5 | XP', '\n'.join(leaderboard[1]), True]

        await message.edit(embed=utils.embed_create(title=title, fields=fields, thumbnail=thumbnail, footer=footer))


    def leaderboard_filter(self, result, members):
        data = []
        for mem in members:
            if str(mem.id) in constants.USER_DATA.keys():
                data.append([mem, constants.USER_DATA[str(mem.id)]])
            else:
                data.append([mem, constants.EMPTY_USER])

        members_rank = sorted(data, key=(lambda x: x[1]['rank']), reverse=True)
        members_xp = sorted(data, key=(lambda x: x[1]['xp']), reverse=True)
        if len(members) <= 5:
            result.append([members_rank, members_xp])
        else:
            result.append([members_rank[:5], members_xp[:5]])


    def leaderboard(self, guild):
        ''' 2 Types: #1 Top 5 after Rank ; #2 Top 5 after XP '''
        members = list(filter(lambda x : not x.bot, guild.members))
        result = []
        distribution = ceil(len(members) / 50)
        data = []
        for i in range(0, distribution):
            if i == distribution - 1:
                data.append(members[i*50:])
            else:
                data.append(members[i*50:  (i+1)*50])

        with ThreadPoolExecutor(max_workers=distribution) as executor:
            executor.map(lambda x : self.leaderboard_filter(result, x), data)

        leaderboard_rank = []
        leaderboard_xp = []

        for r in result:
            leaderboard_rank += r[0]
            leaderboard_xp += r[1]

        leaderboard_rank = sorted(leaderboard_rank, key=(lambda x: x[1]['rank']), reverse=True)
        leaderboard_xp = sorted(leaderboard_rank, key=(lambda x: x[1]['xp']), reverse=True)
        leaderboard = [[],[]]
        for i in range(0, min(5, len(members))):
            entry_rk = leaderboard_rank[i]
            entry_xp = leaderboard_xp[i]

            leaderboard[0].append('{} ({})'.format(entry_rk[0].mention, constants.RANK_MAP[entry_rk[1]['rank']]))
            leaderboard[1].append('{} (Lvl {})'.format(entry_xp[0].mention, utils.level(entry_xp[1]['xp'])))
        return leaderboard

    @server.error
    async def server_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await self.server(ctx, param=str(ctx.message.guild.id))
            return


# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(Server(client))