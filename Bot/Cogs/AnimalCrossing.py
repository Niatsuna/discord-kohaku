''' ANIMALCROSSING.py - Animal Crossing Game Module '''
# -----------------------------------------------------------------------------------------------
# >> Imports
import calendar
import Bot.Backend.utils as utils
import Bot.Backend.constants as constants
from concurrent.futures import ThreadPoolExecutor
from discord.ext import commands
import requests
import locale

# -----------------------------------------------------------------------------------------------
class AnimalCrossing(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.resources = None
        self.functions = [ self.ac_art, self.ac_bug, self.ac_fish, self.ac_fossil, self.ac_items, self.ac_month, self.ac_sea, self.ac_song, self.ac_villager ]
        self.critter_month_footer = {'text' : '❆ North | ☀ South'}
        self.months = self.load_month_map()
        self.months_react = { 'ARRIVING' : '\N{AIRPLANE ARRIVING}', 'ALL' : '\N{DESERT ISLAND}', 'LEAVING' : '\N{AIRPLANE DEPARTURE}'}

    def shortDescription(self):
        return 'Animal Crossing : New Horizon Module'

    def longDescription(self):
        title = 'Animal Crossing : New Horizon'
        description = 'This module is connected to the game \'Animal Crossing : New Horizons\'\n\n**Invoke:** _`{}ac <parameter>`_\n\n**_Possible parameters:_**\n'.format(constants.INVOKE)
        fields = []
        for func in self.functions:
            doc = func.__doc__.split('|')
            fields.append(['_`{}`_'.format(doc[1].strip()), doc[0].strip(), False])
        return [utils.embed_create(title=title, description=description, fields=fields, thumbnail=constants.AC_ICON_URL), None]

    def isSecret(self):
        return False

    @commands.command(pass_context=True)
    async def ac(self, ctx, *, param):
        param = param.lower()
        with ThreadPoolExecutor(max_workers=len(self.functions)) as executor:
            _bool = [await executor.submit(utils.map_function_async, [func, ctx, param]).result() for func in self.functions]
        if True not in _bool:
            await utils.embed_send(ctx, constants.ERROR_SEARCH_FAIL)

    def ac_resources(self):
        if self.resources == None:
            self.resources = utils.json_load('Bot/Resources/json/animalcrossing.json')
            if self.resources == None:
                return False
        return True

    async def ac_art(self, ctx, name):
        if not self.ac_resources():
            return False
        for v in self.resources['art']:
            if name == v['name'].lower() or name == v['name_de'].lower():
                title = '{} | {}'.format(v['name'], v['name_de'])
                await utils.embed_send(ctx, utils.embed_create(title=title, description=v['difference'], image=v['image']))
                return True
        return False

    async def ac_bug(self, ctx, name):
        if not self.ac_resources():
            return False
        for v in self.resources['bugs']:
            if name == v['name'].lower() or name == v['name_de'].lower():
                title = '{} | {}'.format(v['name'], v['name_de'])
                description = '{} {}'.format(v['price'], utils.emote_load('ac-sternis'))
                north = 'ALL YEAR' if v['availability']['north'] == [x for x in range(1,13)] else ' '.join([calendar.month_abbr[x].upper() for x in v['availability']['north']])
                south = 'ALL YEAR' if v['availability']['south'] == [x for x in range(1,13)] else ' '.join([calendar.month_abbr[x].upper() for x in v['availability']['south']])
                fields = [  ['Location', '**Place:** {}\n**Times:** {}\n**Rarity:** {}'.format(v['availability']['location'], v['availability']['time'], v['availability']['rarity']), False],
                            ['Months', ':snowflake: :high_brightness: {}'.format(north) if north == south else ':snowflake: {}\n:high_brightness: {}'.format(north, south), False],
                            ['Catchphrase', v['catch-phrase'], False],
                            ['Blathers\' phrase', v['museum-phrase'], False]]
                await utils.embed_send(ctx, utils.embed_create(title=title, description=description, fields=fields, footer=self.critter_month_footer, thumbnail=v['icon']))
                return True
        return False

    async def ac_fish(self, ctx, name):
        if not self.ac_resources():
            return False
        for v in self.resources['fish']:
            if name == v['name'].lower() or name == v['name_de'].lower():
                title = '{} | {}'.format(v['name'], v['name_de'])
                description = '{} {}'.format(v['price'], utils.emote_load('ac-sternis'))
                north = 'ALL YEAR' if v['availability']['north'] == [x for x in range(1,13)] else ' '.join([calendar.month_abbr[x].upper() for x in v['availability']['north']])
                south = 'ALL YEAR' if v['availability']['south'] == [x for x in range(1,13)] else ' '.join([calendar.month_abbr[x].upper() for x in v['availability']['south']])
                fields = [  ['Location', '**Place:** {}\n**Times:** {}\n**Size:** {}\n**Rarity:** {}'.format(v['availability']['location'], v['availability']['time'], v['availability']['shadow_size'], v['availability']['rarity']), False],
                            ['Months', ':snowflake: :high_brightness: {}'.format(north) if north == south else ':snowflake: {}\n:high_brightness: {}'.format(north, south), False],
                            ['Catchphrase', v['catch-phrase'], False],
                            ['Blathers\' phrase', v['museum-phrase'], False]]
                await utils.embed_send(ctx, utils.embed_create(title=title, description=description, fields=fields, footer=self.critter_month_footer, thumbnail=v['icon']))
                return True
        return False

    async def ac_fossil(self, ctx, name):
        if not self.ac_resources():
            return False
        for v in self.resources['fossils']:
            if name == v['name'].lower() or name == v['name_de'].lower():
                title = '{} | {}'.format(v['name'], v['name_de'])
                description = '{} {}'.format(v['price'], utils.emote_load('ac-sternis'))
                fields = [ ['Blathers\' phrase', v['museum-phrase'], False]]
                await utils.embed_send(ctx, utils.embed_create(title=title, description=description, fields=fields, thumbnail=v['image']))
                return True
        return False

    async def ac_items(self, ctx, name):
        if not self.ac_resources():
            return False
        for v in self.resources['items']:
            if name == v['name'].lower() or name == v['name_de'].lower():
                title = '{} | {}'.format(v['name'], v['name_de'])
                description = '**Buy:** {} {}\n**Sell:** {} {}'.format(v['price'][0], utils.emote_load('ac-sternis'), v['price'][1], utils.emote_load('ac-sternis')) if v['price'][0] != None else '_Not buyable_\n**Sell:** {} {}'.format(v['price'][1], utils.emote_load('ac-sternis'))
                fields = [ ['Variants', v['variants'], True], ['Size', v['size'], True], ['DIY', '_Not craftable_' if v['DIY'] == [] else '\n'.join(v['DIY']), False] ]
                await utils.embed_send(ctx, utils.embed_create(title=title, description=description, fields=fields, thumbnail=v['image']))
                return True
        return False

    async def ac_month(self, ctx, name):
        if not self.ac_resources():
            return False
        if name.startswith('all year'):
            month_num = 0
            isNorth = True
        else:
            param = name.split(' ')
            if len(param) > 1 and param[1].lower() == 'south':
                isNorth = False
            else:
                isNorth = True
            name = param[0]
            try:
                month_num = int(name) if int(name) <= 12 and int(name) >= 1 else -1
            except:
                month_num = -1
                for i in range(1, 13):
                    if name == calendar.month_name[i].lower() or name == calendar.month_abbr[i].lower() or name == self.months[i][0].lower() or name ==self.months[i][1].lower():
                        month_num = i
                        break
        if month_num == -1:
            return False
        elif month_num == 0:
            keyword = 'ALL YEAR'
        else:
            author = ctx.message.author.id
            title = calendar.month_name[month_num]
            description = '<@{}>, please select one of the following options and react to this message with the given reaction.\n**You have 30 seconds.**\nIf you react not in this 30 seconds this message will be deleted. If you react i will delete this message and send the result.\n\n · {} New arriving catchables (Were not catchable the month before)\n · {} All catchables this month (**WARNING: Big Message Overload**)\n · {} Leaving catchables (Not catchable after this month)\n\nPlease note that the different hemispheres existing.\nDefault: Northern hemisphere. To change to southern add `south` at the end of the command.\nExample: `{}ac april south`'.format(
                author, self.months_react['ARRIVING'], self.months_react['ALL'], self.months_react['LEAVING'], constants.INVOKE
            )
            message = await utils.embed_send(ctx, utils.embed_create(title=title, description=description, thumbnail=constants.AC_ICON_NORTH_URL if isNorth else constants.AC_ICON_SOUTH_URL, footer=self.critter_month_footer))
            await message.add_reaction(self.months_react['ARRIVING'])
            await message.add_reaction(self.months_react['ALL'])
            await message.add_reaction(self.months_react['LEAVING'])
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=lambda reaction, user: user.id == author)
            except:
                await message.delete()
                return False
            await message.delete()
            keyword = None
            for (k, v) in self.months_react.items():
                if reaction.emoji == v:
                    keyword = k
                    break
            if keyword == None:
                return False
        await utils.embed_send(ctx, self._ac_month(month_num, keyword, isNorth))
        return True

    async def ac_sea(self, ctx, name):
        if not self.ac_resources():
            return False
        for v in self.resources['sea creatures']:
            if name == v['name'].lower() or name == v['name_de'].lower():
                title = '{} | {}'.format(v['name'], v['name_de'])
                description = '{} {}'.format(v['price'], utils.emote_load('ac-sternis'))
                north = 'ALL YEAR' if v['availability']['north'] == [x for x in range(1,13)] else ' '.join([calendar.month_abbr[x].upper() for x in v['availability']['north']])
                south = 'ALL YEAR' if v['availability']['south'] == [x for x in range(1,13)] else ' '.join([calendar.month_abbr[x].upper() for x in v['availability']['south']])
                fields = [  ['Location', '**Times:** {}\n**Speed:** {}\n**Size:** {}'.format(v['availability']['time'], v['availability']['speed'], v['availability']['shadow_size']), False],
                            ['Months', ':snowflake: :high_brightness: {}'.format(north) if north == south else ':snowflake: {}\n:high_brightness: {}'.format(north, south), False],
                            ['Catchphrase', v['catch-phrase'], False],
                            ['Blathers\' phrase', v['museum-phrase'], False]]
                await utils.embed_send(ctx, utils.embed_create(title=title, description=description, fields=fields, footer=self.critter_month_footer, thumbnail=v['icon']))
                return True
        return False

    async def ac_song(self, ctx, name):
        if not self.ac_resources():
            return False
        for v in self.resources['songs']:
            if name == v['name'].lower() or name == v['name_de'].lower():
                title = '{} | {}'.format(v['name'], v['name_de'])
                description = '[MP3]({})'.format(v['music'])
                await utils.embed_send(ctx, utils.embed_create(title=title, description=description, image=v['image']))
                return True
        return False

    async def ac_villager(self, ctx, name):
        if not self.ac_resources():
            return False
        for v in self.resources['villagers']:
            if name == v['name'].lower() or name == v['name_de'].lower():
                title = '{} | {}'.format(v['name'], v['name_de'])
                description = ':flag_jp: {} | :flag_kr: {} | :flag_cn: {}\n:flag_fr: {} | :flag_es: {} | :flag_it: {}\n:flag_nl: {} | :flag_ru: {}'.format(v['languages']['jp'], v['languages']['kr'], v['languages']['cn'], v['languages']['fr'], v['languages']['es'], v['languages']['it'], v['languages']['nl'], v['languages']['ru'])
                fields = [  ['Personality', v['personality'], True], ['Species', v['species'], True], ['Gender', v['gender'], True], ['Birthday', v['birthday'], True], ['Catchphrase', v['catch-phrase'], False], ['Saying', v['saying'], False]]
                await utils.embed_send(ctx, utils.embed_create(title=title, description=description, fields=fields, image=v['image'], thumbnail=v['icon']))
                return True
        return False

    def _ac_month(self, month_num, keyword, isNorth):
        hemisphere = 'north' if isNorth else 'south'
        embeds = []
        for category in ['Fish', 'Bugs', 'Sea creatures']:
            critters = []
            for v in self.resources[category.lower()]:
                if keyword == 'ALL YEAR' and v['availability'][hemisphere] == list(range(1,13)):
                    critters.append(v)
                elif month_num in v['availability'][hemisphere] and v['availability'][hemisphere] != list(range(1,13)):
                    next_month = month_num + 1 if month_num < 12 else 1
                    last_month = month_num - 1 if month_num > 1 else 12
                    if (keyword == 'ARRIVING' and last_month not in v['availability'][hemisphere]) or (keyword == 'ALL') or (keyword == 'LEAVING' and next_month not in v['availability'][hemisphere]):
                        critters.append(v)
            title = '{} | {} : {}'.format(calendar.month_name[month_num].upper(), keyword, category) if keyword != 'ALL YEAR' else '{} : {}'.format(keyword, category)
            description = 'There are currently {} catchables in the category \'{}\' for the selected option.'.format(len(critters), category)
            fields = []
            for crit in critters:
                fields.append(['Price: {} {}'.format(crit['price'], utils.emote_load('ac-sternis')), '**Name:** {} | {}\n**Time:** {}\n'.format(crit['name'], crit['name_de'], crit['availability']['time']) if category == 'Sea creatures' else '**Name:** {} | {}\n**Location:** {}\n({})'.format(crit['name'], crit['name_de'], crit['availability']['location'], crit['availability']['time']), True])
            em = utils.embed_create(title=title, description=description, fields=fields, thumbnail=constants.AC_ICON_NORTH_URL if isNorth else constants.AC_ICON_SOUTH_URL, footer=self.critter_month_footer)
            if isinstance(em, list):
                embeds += em
            else:
                embeds += [em]
        return embeds

    def load_month_map(self):
        months = [None]
        with calendar.different_locale('de_DE'):
            for i in range(1, 13):
                german = [calendar.month_name[i], calendar.month_abbr[i]]
                months.append(german)
        return months

# -----------------------------------------------------------------------------------------------
def setup(client):
    client.add_cog(AnimalCrossing(client))