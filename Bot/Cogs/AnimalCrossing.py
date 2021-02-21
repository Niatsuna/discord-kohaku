''' ANIMALCROSSING.py '''
# > ---------------------------------------------------------------------------
# > Imports
import calendar
import discord
from discord.ext import commands
import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
from concurrent.futures import ThreadPoolExecutor

ALIASES = ['ac', 'acnh']

# > ---------------------------------------------------------------------------
class AnimalCrossing(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.sternis = utils.load_emote('ac-sternis')
        self.resource_list = ['art', 'bugs', 'fishes', 'fossils', 'sea_creatures', 'songs', 'villagers']
        self.instant_map = {
            'art' : (lambda ctx : self.instant_art(ctx)),
            'fossil' : (lambda ctx : self.instant_fossil(ctx)),
            'song' : (lambda ctx : self.instant_song(ctx))
        }
        self.instant_embeds = {}
        self.functions = [self.search_art, self.search_bug, self.search_fish, self.search_fossil, self.search_month, self.search_seaCreature, self.search_song, self.search_villager]
        self.resource = None
        self.critter_month_footer = {'text' : '❆ North | ☀ South'}
        self.months = [None, ['Januar', 'Jan'], ['Februar', 'Feb'], ['März', 'Mrz'], ['April', 'Apr'], ['Mai', 'Mai'], ['Juni', 'Jun'], ['Juli', 'Jul'], ['August', 'Aug'], ['September', 'Sep'], ['Oktober', 'Okt'], ['November', 'Nov'], ['Dezember', 'Dez']]
        self.months_react = { 'ARRIVING' : '\N{AIRPLANE ARRIVING}', 'ALL' : '\N{DESERT ISLAND}', 'LEAVING' : '\N{AIRPLANE DEPARTURE}'}
        self.month_embeds = {}

    def help(self, footer):
        title = 'Help Info: {}animalcrossing'.format(constants.INVOKE)
        if ALIASES != None and ALIASES != []:
            alias = '**Aliases: ** {}\n'.format(' '.join(['`{}`'.format(x) for x in ALIASES]))
        else:
            alias = ''
        possibilities = ['art - Shows a list of all artworks', 'fossil - Shows a list of all fossil', 'song - Shows a list of all songs', '<fish>/<bug>/<sea creature> - Looks up a specific critter', '<month> - Shows all critter for the month', '<song> - Looks up a specific song', '<fossil> - Looks up a specific fossil', '<villager> - Looks up a specific villager.']
        description = 'This command is connected to the game \'Animal Crossing : New Horizons\' and can show information regarding this game.\n\n{}**Usage: ** \n{}'.format(
            alias, '\n'.join(['`{}animalcrossing` {}'.format(constants.INVOKE, x) for x in possibilities]))
        return utils.embed_create(title=title, description=description, footer=footer)

    def isSecret(self):
        return False

    @commands.command(pass_context=True, aliases=ALIASES)
    async def animalcrossing(self, ctx, *, param):
        param = param.lower().strip()
        if self.resource == None:
            await self.update()

        if param in self.instant_map.keys():
            await self.instant_map[param](ctx)
            return

        with ThreadPoolExecutor(max_workers=len(self.functions)) as executor:
            _bool = [await executor.submit(utils.map_function_async, [func, ctx, param]).result() for func in self.functions]
        if True not in _bool:
            await utils.embed_send(ctx, constants.ERROR_SEARCH_FAIL)

    @animalcrossing.error
    async def animalcrossing_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.embed_send(ctx, constants.ERROR_MISSING_PARAM)
            return

    async def update(self):
        result = {}
        for r in self.resource_list:
            result[r] = utils.json_load_url('{}/api/ac/{}.json'.format(constants.API_URL, r))
        utils.json_store('Bot/Resources/json/animal_crossing.json', result)
        self.instant_embeds = {}
        self.resource = result

    async def search_by_exact_name_en_n_de(self, object_list, param):
        result = {'en' : None, 'de' : None}
        for obj in object_list:
            if result['en'] == None and param.lower().strip() == obj['name']['en'].lower().strip() :
                result['en'] = obj
            if result['de'] == None and param.lower().strip() == obj['name']['de'].lower().strip() :
                result['de'] = obj
            if result['en'] != None and result['de'] != None:
                break
        return result

    async def search_by_part_name_en_n_de(self, object_list, param):
        result = {'en' : None, 'de' : None}
        if len(param.lower().strip()) >= 3:
            for obj in object_list:
                if result['en'] == None and param.lower().strip() in obj['name']['en'].lower().strip() :
                    result['en'] = obj
                if result['de'] == None and param.lower().strip() in obj['name']['de'].lower().strip() :
                    result['de'] = obj
                if result['en'] != None and result['de'] != None:
                    break
        return result

    async def instant_art(self, ctx):
        if 'art' in self.instant_embeds.keys():
            embed = self.instant_embeds['art']
        else:
            art = self.resource['art']
            title = 'Artworks'
            description = 'There are currently {} artworks in the game.\n\n**English Name**\nGerman Name\n'.format(len(art))
            fields = []
            for a in art:
                fields.append([a['name']['en'], a['name']['de'], True])
            embed = utils.embed_create(title=title, description=description, fields=fields)
            self.instant_embeds['art'] = embed
        await utils.embed_send(ctx, embed)

    async def instant_fossil(self, ctx):
        if 'fossil' in self.instant_embeds.keys():
            embed = self.instant_embeds['fossil']
        else:
            fossil = self.resource['fossils']
            title = 'Fossils'
            description = 'There are currently {} fossils in the game.\n\n**English Name**\nGerman Name\n'.format(len(fossil))
            fields = []
            for f in fossil:
                fields.append([f['name']['en'], f['name']['de'], True])
            embed = utils.embed_create(title=title, description=description, fields=fields)
            self.instant_embeds['fossil'] = embed
        await utils.embed_send(ctx, embed)

    async def instant_song(self, ctx):
        if 'song' in self.instant_embeds.keys():
            embed = self.instant_embeds['song']
        else:
            song = self.resource['songs']
            title = 'Songs'
            description = 'There are currently {} songs in the game.\n\n**English Name**\nGerman Name\n'.format(len(song))
            fields = []
            for s in song:
                fields.append([s['name']['en'], s['name']['de'], True])
            embed = utils.embed_create(title=title, description=description, fields=fields)
            self.instant_embeds['song'] = embed
        await utils.embed_send(ctx, embed)

    async def search_art(self, ctx, param):
        arts = self.resource['art']
        data = await self.search_by_exact_name_en_n_de(arts, param)
        if data == {'en' : None, 'de' : None}:
            return False

        if data['de'] != None:
            data = utils.json_load_url(data['de']['url'])
        else:
            data = utils.json_load_url(data['en']['url'])
        
        if data == None:
            await utils.embed_send(ctx, constants.ERROR_WHOOPS)
            return True

        t = data['name']['en']
        d = ':flag_de: _{}_\n{}'.format(data['name']['de'], data['difference'])

        await utils.embed_send(ctx, utils.embed_create(title=t, description=d, image=data['image']))
        return True

    async def search_bug(self, ctx, param):
        bugs = self.resource['bugs']
        data = await self.search_by_exact_name_en_n_de(bugs, param)
        if data == {'en' : None, 'de' : None}:
            data = await self.search_by_part_name_en_n_de(bugs, param)
            if data == {'en' : None, 'de' : None}:
                return False
        
        if data['de'] != None:
            data = utils.json_load_url(data['de']['url'])
        else:
            data = utils.json_load_url(data['en']['url'])
        
        if data == None:
            await utils.embed_send(ctx, constants.ERROR_WHOOPS)
            return True
        
        t = ':flag_us: {}'.format(data['name']['en'])
        d = ':flag_de: _{}_\n{} {}'.format(data['name']['de'], data['price'], self.sternis)
        north = 'ALL YEAR' if data['availability']['months-northern'] == [x for x in range(1,13)] else ' '.join([calendar.month_abbr[x].upper() for x in data['availability']['months-northern']])
        south = 'ALL YEAR' if data['availability']['months-southern'] == [x for x in range(1,13)] else ' '.join([calendar.month_abbr[x].upper() for x in data['availability']['months-southern']])
        fields = [
            ['Location', '**Place:** {}\n**Times:** {}\n**Rarity:** {}'.format(data['availability']['location'],data['availability']['time'],data['availability']['rarity'] ), False],
            ['Months', ':snowflake: :high_brightness: {}'.format(north) if north == south else ':snowflake: {}\n:high_brightness: {}'.format(north, south), False],
            ['Catchphrase', data['catch-phrase'], False],
            ['Blathers\' phrase', data['museums-phrase'], False]
        ]
        await utils.embed_send(ctx, utils.embed_create(title=t, description=d, fields=fields, footer=self.critter_month_footer, thumbnail=data['icon']))
        return True

    async def search_fish(self, ctx, param):
        fishes = self.resource['fishes']
        data = await self.search_by_exact_name_en_n_de(fishes, param)
        if data == {'en' : None, 'de' : None}:
            data = await self.search_by_part_name_en_n_de(fishes, param)
            if data == {'en' : None, 'de' : None}:
                return False
        
        if data['de'] != None:
            data = utils.json_load_url(data['de']['url'])
        else:
            data = utils.json_load_url(data['en']['url'])
        
        if data == None:
            await utils.embed_send(ctx, constants.ERROR_WHOOPS)
            return True
        
        t = ':flag_us: {}'.format(data['name']['en'])
        d = ':flag_de: _{}_\n{} {}'.format(data['name']['de'], data['price'], self.sternis)
        north = 'ALL YEAR' if data['availability']['months-northern'] == [x for x in range(1,13)] else ' '.join([calendar.month_abbr[x].upper() for x in data['availability']['months-northern']])
        south = 'ALL YEAR' if data['availability']['months-southern'] == [x for x in range(1,13)] else ' '.join([calendar.month_abbr[x].upper() for x in data['availability']['months-southern']])
        fields = [
            ['Location', '**Place:** {}\n**Times:** {}\n **Shadow:** {}\n**Rarity:** {}'.format(data['availability']['location'],data['availability']['time'],data['shadow'], data['availability']['rarity'] ), False],
            ['Months', ':snowflake: :high_brightness: {}'.format(north) if north == south else ':snowflake: {}\n:high_brightness: {}'.format(north, south), False],
            ['Catchphrase', data['catch-phrase'], False],
            ['Blathers\' phrase', data['museums-phrase'], False]
        ]
        await utils.embed_send(ctx, utils.embed_create(title=t, description=d, fields=fields, footer=self.critter_month_footer, thumbnail=data['icon']))
        return True

    async def search_fossil(self, ctx, param):
        fossils = self.resource['fossils']
        data = await self.search_by_exact_name_en_n_de(fossils, param)
        if data == {'en' : None, 'de' : None}:
            data = await self.search_by_part_name_en_n_de(fossils, param)
            if data == {'en' : None, 'de' : None}:
                return False
        
        if data['de'] != None:
            data = utils.json_load_url(data['de']['url'])
        else:
            data = utils.json_load_url(data['en']['url'])
        
        if data == None:
            await utils.embed_send(ctx, constants.ERROR_WHOOPS)
            return True
        
        t = ':flag_us: {}'.format(data['name']['en'])
        d = ':flag_de: _{}_\n{} {}'.format(data['name']['de'], data['price'], self.sternis)
        fields = [
            ['Set', data['group'].capitalize(), False],
            ['Blathers\' phrase', data['museums-phrase'], False],
        ]
        await utils.embed_send(ctx, utils.embed_create(title=t, description=d, fields=fields, thumbnail=data['image']))
        return True

    async def search_month(self, ctx, param):
        param = param.lower().strip()
        isNorth = True
        keyword = None
        message = None
        if param == 'all year':
            param = 0
        else:
            param = param.split(' ')
            if len(param) > 1 and param[1].lower() == 'south':
                isNorth = False
            param = param[0]

            try:
                param = int(param)
            except:
                for i in range(1, 13):
                    if param == calendar.month_name[i].lower() or param == calendar.month_abbr[i].lower() or param == self.months[i][0].lower() or param == self.months[i][1].lower():
                        param = i
                        break

            if type(param) != int or param > 12 or param < 0:
                if param == 1337 or param == 42:
                    await utils.embed_send(ctx, utils.embed_create(description='Nice try (⌐■_■)'))
                    return True
                return False

            if param != 0:
                author = ctx.message.author.id
                title = calendar.month_name[param] if param != 0 else 'All year'
                description = '{}\n<@{}>, please select one of the following options and react to this message with the given reaction.\n**You have 30 seconds.**\nIf you react not in this 30 seconds this message will be deleted. If you react i will delete this message and send the result.\n\n · {} New arriving catchables (Were not catchable the month before)\n · {} All catchables this month (**WARNING: Big Message Overload**)\n · {} Leaving catchables (Not catchable after this month)\n\nPlease note that the different hemispheres existing.\nDefault: Northern hemisphere. To change to southern add `south` at the end of the command.\nExample: `{}ac april south`'.format(
                    ('❆ North' if isNorth else '☀ South'), author, self.months_react['ARRIVING'], self.months_react['ALL'], self.months_react['LEAVING'], constants.INVOKE
                )

                message = await utils.embed_send(ctx, utils.embed_create(title=title, description=description))
                await message.add_reaction(self.months_react['ARRIVING'])
                await message.add_reaction(self.months_react['ALL'])
                await message.add_reaction(self.months_react['LEAVING'])

                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=30, check=lambda reaction, user: user.id == author and str(reaction.emoji) in list(self.months_react.values()))
                except:
                    await message.edit(embed=constants.ERROR_TIMEOUT)
                    return False
                
                for (k, v) in self.months_react.items():
                    if str(reaction.emoji) == v:
                        keyword = k
                        break
                if keyword == None:
                    return False
                await message.edit(embed=utils.embed_create(description='Please wait ...'))

        embeds = []
        if param == 0 and param in self.month_embeds.keys():
            embeds = self.month_embeds[0]
        elif param > 0 and param in self.month_embeds.keys():
            dict_embeds = self.month_embeds[param]
            if keyword != None and keyword in dict_embeds.keys():
                embeds = dict_embeds[keyword]

        if embeds == []:
            if message == None:
                message = await utils.embed_send(ctx, utils.embed_create(description='Please wait ...'))
            bugs = self.resource['bugs']
            fishes = self.resource['fishes']
            sea = self.resource['sea_creatures']
            combined_data = {'Bugs' : bugs, 'Fish': fishes, 'Sea Creatures' : sea}

            for category in combined_data.keys():
                critters = []
                for obj in combined_data[category]:
                    obj_set = obj['months']['north'] if isNorth else obj['months']['south']
                    if param == 0 and obj_set == list(range(1,13)):
                        critters.append(utils.json_load_url(obj['url']))
                    elif param in obj_set:
                        prev_ = param - 1 if param > 1 else 12
                        next_ = param + 1 if param < 12 else 1

                        if keyword is 'ALL' or (keyword is 'ARRIVING' and prev_ not in obj_set) or (keyword is 'LEAVING' and next_ not in obj_set):
                            critters.append(utils.json_load_url(obj['url']))
                t = '{} | {} : {}'.format(calendar.month_name[param].upper(), keyword, category) if param != 0 else 'ALL YEAR | {} : {}'.format(keyword, category)
                description = '{}\nThere are currently {} catchables in the category \'{}\' for the selected option.'.format(('❆ North' if isNorth else '☀ South'),len(critters), category)
                fields = []
                for crit in critters:
                    fields.append(['Price: {} {}'.format(crit['price'], self.sternis), '**Name:** {} | {}\n**Time:** {}\n'.format(crit['name']['en'], crit['name']['de'], crit['availability']['time']) if category == 'Sea Creatures' else '**Name:** {} | {}\n**Location:** {}\n({})'.format(crit['name']['en'], crit['name']['de'], crit['availability']['location'], crit['availability']['time']), True])
                em = utils.embed_create(title=t, description=description, fields=fields, footer=self.critter_month_footer)

                if isinstance(em, list):
                    embeds += em
                else:
                    embeds += [em]
            if param == 0:
                self.month_embeds[0] = embeds
            else:
                if param not in self.month_embeds.keys():
                    self.month_embeds[param] = {}
                self.month_embeds[param][keyword] = embeds

        if message != None:
            await message.delete()

        await utils.embed_send(ctx, embeds)
        return True
            

    async def search_seaCreature(self, ctx, param):
        seaCs = self.resource['sea_creatures']
        data = await self.search_by_exact_name_en_n_de(seaCs, param)
        if data == {'en' : None, 'de' : None}:
            data = await self.search_by_part_name_en_n_de(seaCs, param)
            if data == {'en' : None, 'de' : None}:
                return False
        
        if data['de'] != None:
            data = utils.json_load_url(data['de']['url'])
        else:
            data = utils.json_load_url(data['en']['url'])
        
        if data == None:
            await utils.embed_send(ctx, constants.ERROR_WHOOPS)
            return True
        
        t = ':flag_us: {}'.format(data['name']['en'])
        d = ':flag_de: _{}_\n{} {}'.format(data['name']['de'], data['price'], self.sternis)
        north = 'ALL YEAR' if data['availability']['months-northern'] == [x for x in range(1,13)] else ' '.join([calendar.month_abbr[x].upper() for x in data['availability']['months-northern']])
        south = 'ALL YEAR' if data['availability']['months-southern'] == [x for x in range(1,13)] else ' '.join([calendar.month_abbr[x].upper() for x in data['availability']['months-southern']])
        fields = [
            ['Location', '**Times:** {}\n **Shadow:** {}\n**Speed:** {}'.format(data['availability']['time'],data['shadow'], data['speed'] ), False],
            ['Months', ':snowflake: :high_brightness: {}'.format(north) if north == south else ':snowflake: {}\n:high_brightness: {}'.format(north, south), False],
            ['Catchphrase', data['catch-phrase'], False],
            ['Blathers\' phrase', data['museums-phrase'], False]
        ]
        await utils.embed_send(ctx, utils.embed_create(title=t, description=d, fields=fields, footer=self.critter_month_footer, thumbnail=data['icon']))
        return True

    async def search_song(self, ctx, param):
        songs = self.resource['songs'] 
        data = await self.search_by_exact_name_en_n_de(songs, param)
        if data == {'en' : None, 'de' : None}:
            data = await self.search_by_part_name_en_n_de(songs, param)
            if data == {'en' : None, 'de' : None}:
                return False
        
        if data['de'] != None:
            data = utils.json_load_url(data['de']['url'])
        else:
            data = utils.json_load_url(data['en']['url'])
        
        if data == None:
            await utils.embed_send(ctx, constants.ERROR_WHOOPS)
            return True

        t = ':flag_us: {}'.format(data['name']['en'])
        d = ':flag_de: _{}_\n[MP3]({})'.format(data['name']['de'], data['music'])
        await utils.embed_send(ctx, utils.embed_create(title=t, description=d, image=data['image']))
        return True

    async def search_villager(self, ctx, param):
        villagers = self.resource['villagers'] 
        data = await self.search_by_exact_name_en_n_de(villagers, param)
        if data == {'en' : None, 'de' : None}:
            data = await self.search_by_part_name_en_n_de(villagers, param)
            if data == {'en' : None, 'de' : None}:
                return False
        
        if data['de'] != None:
            data = utils.json_load_url(data['de']['url'])
        else:
            data = utils.json_load_url(data['en']['url'])
        
        if data == None:
            await utils.embed_send(ctx, constants.ERROR_WHOOPS)
            return True

        t = ':flag_us: {}'.format(data['name']['en'])
        d = ':flag_jp: {} | :flag_kr: {} | :flag_cn: {}\n:flag_de: {} | :flag_fr: {} | :flag_es: {} \n :flag_it: {} | :flag_nl: {} | :flag_ru: {}'.format(data['name']['jp'], data['name']['kr'], data['name']['cn'],data['name']['de'],  data['name']['fr'], data['name']['es'], data['name']['it'], data['name']['nl'], data['name']['ru'])
        fields = [  
            ['Personality', data['personality'], True], 
            ['Species', data['species'], True], 
            ['Gender', data['gender'], True], 
            ['Birthday', data['birthday'], True], 
            ['Catchphrase', '{} ({})'.format(data['catch-phrase']['en'], data['catch-phrase']['de']), False], 
            ['Saying', data['saying'], False]]
        await utils.embed_send(ctx, utils.embed_create(title=t, description=d, fields=fields, image=data['image'], thumbnail=data['icon']))
        return True

# > ---------------------------------------------------------------------------
def setup(client):
    client.add_cog(AnimalCrossing(client))