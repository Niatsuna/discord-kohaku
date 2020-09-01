''' DEADBYDAYLIGHT.py - Dead by Daylight Game Module '''
# -----------------------------------------------------------------------------------------------
# >> Imports
import Bot.Backend.utils as utils
import Bot.Backend.constants as constants
from concurrent.futures import ThreadPoolExecutor
from discord.ext import commands
import requests

# -----------------------------------------------------------------------------------------------
class DeadByDaylight(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.resources = None
        self.instant = {
            ('shrine', 'schrein', 'sos') : self.dbd_shrine,
            ('survivors', 'überlebende', 'survivor', 'überlebender') : self.dbd_survivors,
            ('killers', 'killer') : self.dbd_killers }
        self.functions = [ self.dbd_survivor, self.dbd_killer, self.dbd_perk, self.dbd_offering ]

    def shortDescription(self):
        return 'Dead by Daylight Module'

    def longDescription(self):
        title = 'Dead by Daylight'
        description = 'Wa'
        return [utils.embed_create(title=title, description=description), None]

    def isSecret(self):
        return False

    @commands.command(pass_context=True)
    async def dbd(self, ctx, *, param):
        param = param.lower()
        for k in self.instant.keys():
            if param in k:
                if not await self.instant[k](ctx):
                    await utils.embed_send(ctx, constants.ERROR_WHOOPS)
                return
        with ThreadPoolExecutor(max_workers=len(self.functions)) as executor:
            _bool = [await executor.submit(utils.map_function_async, [func, ctx, param]).result() for func in self.functions]
        if True not in _bool:
            await utils.embed_send(ctx, constants.ERROR_SEARCH_FAIL)

    def dbd_resources(self):
        if self.resources == None:
            self.resources = utils.json_load('Bot/Resources/json/deadbydaylight.json')
            if self.resources == None:
                return False
        return True

    async def dbd_shrine(self, ctx):
        if not self.dbd_resources():
            return False
        try:
            response = requests.get(constants.DBD_REST_API + 'shrineofsecrets?pretty=true&branch=live')
        except:
            return False
        response = response.content.decode('utf-8').split('|')
        refresh = response[-1].strip()
        shrine = []
        for entry in [x.strip() for x in response[0].split(',')]:
            entry = entry.split(':')
            cost = entry[-1].strip()
            name = ':'.join(entry[:-1]).strip()
            for v in self.resources['perks']:
                if name == v['displayName']:
                    shrine.append([v, cost])
                    break
        title = 'Shrine of Secrets'
        description = '[Wikipage]({})\n\n_**Teachables:**_'.format(constants.DBD_WIKI_URL + 'Shrine_of_Secrets')
        fields = []
        images = []
        for i in range(0,len(shrine)):
            entry = shrine[i]
            desc = '_Cost:_ {} {}\n_From:_ {}'.format(entry[1], utils.emote_load('dbd-shards'), entry[0]['teachableInfo']['character'])
            fields.append([entry[0]['displayName'], desc, True])
            images.append(utils.image_open_url(entry[0]['image']))
            if i % 2 != 0:
                fields.append([None, True])
        img = None
        for i in range(0, len(images)//2):
            dst = utils.image_concat_lr(images[i*2], images[i*2+1])
            img = dst if img == None else utils.image_concat_ud(img, dst)
        img = utils.image_resize_factor(img, 0.5)
        await utils.embed_send(ctx, utils.embed_create(title=title, description=description, fields=fields, footer={'text' : refresh}, image='attachment://image.png'), file=utils.image_to_file(img))
        return True

    async def dbd_survivors(self, ctx):
        if not self.dbd_resources():
            return False
        title = 'Survivors'
        description = 'The survivors task is to try and escape from the realms of the Entity in which they are trapped. In order to do so, survivors must complete the following tasks:\n · Repair 5 generators to power the 2 exit gates.\n · Open at least one of the exit gates and leave the trial grounds or escape through the hatch.\n\nMeanwhile, the killer will be trying to locate, catch and hook survivors in order to sacrifice them to the Entity.\n\n Currently there are {} survivors to choose from. For more information regarding one survivor please check:\n_`{}dbd <survivor-name>`_'.format(
            len(self.resources['survivors']), constants.INVOKE )
        fields = [['<Display Name>', '<Full Name / Alt. writing>', False]]
        for i in range(0, len(self.resources['survivors'])):
            v = self.resources['survivors'][i]
            fields.append([v['displayName'], v['fullName'], True])
            if i % 2 != 0:
                fields.append([None, True])
        await utils.embed_send(ctx, utils.embed_create(title=title, description=description, fields=fields))
        return True

    async def dbd_killers(self, ctx):
        if not self.dbd_resources():
            return False
        title = 'Killers'
        description = 'The killers have been tasked by the Entity to hunt down and sacrifice every survivor before they can escape. In order to achieve this objective, a killer should do the following:\n · Patrol the area and find survivors.\n · Chase, injure and catch survivors before they escape.\n · Carry survivors to a sacrificial hook and hang them there for the Entity to consume.\n\n Currently there are {} killers to choose from. For more information regarding one killer plese check:\n_`{}dbd <killer-name>`_'.format(
            len(self.resources['killers']), constants.INVOKE )
        fields = [['<Display Name> | <Display Name german>', '<Full Name>', False]]
        for i in range(0, len(self.resources['killers'])):
            v = self.resources['killers'][i]
            fields.append(['{} | {}'.format(v['displayName'], v['displayName_de']) if v['displayName_de'] != None else v['displayName'], v['fullName'], True])
            if i % 2 != 0:
                fields.append([None, True])
        await utils.embed_send(ctx, utils.embed_create(title=title, description=description, fields=fields))
        return True

    async def dbd_survivor(self, ctx, name):
        if not self.dbd_resources():
            return False
        for v in self.resources['survivors']:
            if name in v['displayName'].lower().split(' ') or (v['fullName'] != None and name in v['fullName'].lower().split(' ')):
                title = '{} ({})'.format(v['fullName'], v['displayName']) if v['fullName'] != None else v['displayName']
                description = '[Wikipage]({})\n{}\n\n**Gender:** {}\n**Nationality:** {}\n**Role:** {}\n'.format(
                    v['url'], v['biography'], v['gender'], v['nationality'], v['role']
                )
                fields = [['DLC', v['dlc'], True],['Difficulty', v['difficulty'], True],[None, True]]
                for i in range(0,len(v['perks'])):
                    fields.append(['Lvl {}'.format(30 + 5*i), v['perks'][i], True])
                img = utils.image_open_url(v['image'])
                await utils.embed_send(ctx, utils.embed_create(title=title, description=description, fields=fields, thumbnail='attachment://image.png'), file=utils.image_to_file(img))
                return True
        return False

    async def dbd_killer(self, ctx, name):
        if not self.dbd_resources():
            return False
        for v in self.resources['killers']:
            if name in v['displayName'].lower().split(' ') or (v['displayName_de'] != None and name in v['displayName_de'].lower().split(' ')) or name in v['fullName'].lower().split(' ') or (v['alias'] != [] and name in v['alias'].replace('"', '').lower().split('/')):
                title = '{} | {}'.format(v['displayName'], v['displayName_de']) if v['displayName_de'] != None else v['displayName']
                description = '[Wikipage]({})\n{}\n\n**Full Name:** {}\n**Alias:** {}\n**Gender:** {}\n**Nationality:** {}\n**Realm:** {}\n**Height:** {}'.format(
                    v['url'], v['biography'], v['fullName'], v['alias'] if v['alias'] != [] else '-' ,v['gender'], v['nationality'], v['realm'], v['height']
                )
                fields = [  ['Power', v['power'], True], ['Weapon', v['weapon'], True], [None, True],
                            ['Speed', v['speed'], True], ['Terror radius', v['terror_radius'], True], [None, True], [None, False],
                            ['DLC', v['dlc'], True],['Difficulty', v['difficulty'], True],[None, True]]
                for i in range(0,len(v['perks'])):
                    fields.append(['Lvl {}'.format(30 + 5*i), v['perks'][i], True])
                img = utils.image_open_url(v['image'])
                await utils.embed_send(ctx, utils.embed_create(title=title, description=description, fields=fields, thumbnail='attachment://image.png'), file=utils.image_to_file(img))
                return True
        return False

    async def dbd_perk(self, ctx, name):
        if not self.dbd_resources() or self.isCharacter(name):
            return False
        for v in self.resources['perks']:
            if name in v['displayName'].lower() or name in v['displayName_de'].lower():
                title = '{} | {}'.format(v['displayName'], v['displayName_de'])
                description = '[Wikipage]({})\n\n{}'.format(v['url'], v['description'])
                if v['isTeachable']:
                    fields = [['Type', 'Teachable :star: | {} (Lvl {})'.format(v['teachableInfo']['character'], v['teachableInfo']['lvl']), False]]
                else:
                    fields = [['Type', 'Unlockable :lock:', False]]
                img = utils.image_open_url(v['image'])
                await utils.embed_send(ctx, utils.embed_create(title=title, description=description, fields=fields, thumbnail='attachment://image.png'), file=utils.image_to_file(img))
                return True
        return False

    async def dbd_offering(self, ctx, name):
        if not self.dbd_resources() or self.isCharacter(name):
            return False
        for v in self.resources['offerings']:
            if name in v['displayName'].lower() or name in v['displayName_de'].lower():
                title = '{} | {}'.format(v['displayName'], v['displayName_de'])
                description = '[Wikipage]({})\n\n{}'.format(v['url'], v['description'])
                img = utils.image_open_url(v['image'])
                await utils.embed_send(ctx, utils.embed_create(title=title, description=description, thumbnail='attachment://image.png'), file=utils.image_to_file(img))
                return True
        return False

    def isCharacter(self, name):
        for v in self.resources['survivors'] + self.resources['killers']:
            if name in v['displayName'].lower().split(' ') or (v['fullName'] != None and name in v['fullName'].lower().split(' ')) or ('displayName_de' in v.keys() and v['displayName_de'] != None and name == v['displayName_de'].lower().split(' ')):
                return True
        return False

# -----------------------------------------------------------------------------------------------
def setup(client):
    client.add_cog(DeadByDaylight(client))