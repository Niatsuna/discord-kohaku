import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
import requests
import json

PATH = 'Bot/Resources/json/animalcrossing.json'
API = constants.AC_REST_API

def fishs(result, api):
    fish_result = []
    for v in list(api.values()):
        fish = {}
        fish['name'] = v['name']['name-USen'].capitalize()
        fish['name_de'] = v['name']['name-EUde'].capitalize()
        availability = {}
        availability['north'] = v['availability']['month-array-northern']
        availability['south'] = v['availability']['month-array-southern']
        availability['time'] = 'ALL DAY' if v['availability']['isAllDay'] else v['availability']['time']
        availability['location'] = v['availability']['location']
        availability['rarity'] = v['availability']['rarity']
        availability['shadow_size'] = ' '.join(v['shadow'].split(' ')[:-1])
        fish['availability'] = availability
        fish['price'] = v['price']
        fish['catch-phrase'] = v['catch-phrase']
        fish['museum-phrase'] = v['museum-phrase']
        fish['image'] = v['image_uri']
        fish['icon'] = v['icon_uri']
        fish_result.append(fish)
    result['fish'] = fish_result

def sea(result, api):
    sea_result = []
    for v in list(api.values()):
        sea = {}
        sea['name'] = v['name']['name-USen'].capitalize()
        sea['name_de'] = v['name']['name-EUde'].capitalize()
        availability = {}
        availability['north'] = v['availability']['month-array-northern']
        availability['south'] = v['availability']['month-array-southern']
        availability['time'] = 'ALL DAY' if v['availability']['isAllDay'] else v['availability']['time']
        availability['speed'] = v['speed']
        availability['shadow_size'] = ' '.join(v['shadow'].split(' ')[:-1])
        sea['availability'] = availability
        sea['price'] = v['price']
        sea['catch-phrase'] = v['catch-phrase']
        sea['museum-phrase'] = v['museum-phrase']
        sea['image'] = v['image_uri']
        sea['icon'] = v['icon_uri']
        sea_result.append(sea)
    result['sea creatures'] = sea_result

def bugs(result, api):
    bug_result = []
    for v in list(api.values()):
        bug = {}
        bug['name'] = v['name']['name-USen'].capitalize()
        bug['name_de'] = v['name']['name-EUde'].capitalize()
        availability = {}
        availability['north'] = v['availability']['month-array-northern']
        availability['south'] = v['availability']['month-array-southern']
        availability['time'] = 'ALL DAY' if v['availability']['isAllDay'] else v['availability']['time']
        availability['location'] = v['availability']['location']
        availability['rarity'] = v['availability']['rarity']
        bug['availability'] = availability
        bug['price'] = v['price']
        bug['catch-phrase'] = v['catch-phrase']
        bug['museum-phrase'] = v['museum-phrase']
        bug['image'] = v['image_uri']
        bug['icon'] = v['icon_uri']
        bug_result.append(bug)
    result['bugs'] = bug_result

def fossils(result, api):
    fossil_result= []
    for v in list(api.values()):
        foss = {}
        foss['name'] = v['name']['name-USen'].capitalize()
        foss['name_de'] = v['name']['name-EUde'].capitalize()
        foss['price'] = v['price']
        foss['part-of'] = v['part-of']
        foss['museum-phrase'] = v['museum-phrase']
        foss['image'] = v['image_uri']
        fossil_result.append(foss)
    result['fossils'] = fossil_result

def villagers(result, api):
    villager_result = []
    for v in list(api.values()):
        vill = {}
        vill['name'] = v['name']['name-USen']
        vill['name_de'] = v['name']['name-EUde']
        languages = {}
        languages['jp'] = v['name']['name-JPja']
        languages['kr'] = v['name']['name-KRko']
        languages['cn'] = v['name']['name-CNzh']
        languages['fr'] = v['name']['name-EUfr']
        languages['es'] = v['name']['name-EUes']
        languages['it'] = v['name']['name-EUit']
        languages['nl'] = v['name']['name-EUnl']
        languages['ru'] = v['name']['name-EUru']
        vill['languages'] = languages
        vill['personality'] = v['personality']
        vill['birthday'] = v['birthday-string']
        vill['species'] = v['species']
        vill['gender'] = v['gender']
        vill['catch-phrase'] = v['catch-phrase'] + '({})'.format(v['catch-translations']['catch-EUde'])
        vill['saying'] = v['saying']
        vill['image'] = v['image_uri']
        vill['icon'] = v['icon_uri']
        villager_result.append(vill)
    result['villagers'] = villager_result

def song(result, api):
    song_result = []
    for v in list(api.values()):
        song = {}
        song['name'] = v['name']['name-USen'].capitalize()
        song['name_de'] = v['name']['name-EUde'].capitalize()
        song['image'] = v['image_uri']
        song['music'] = v['music_uri']
        song_result.append(song)
    result['songs'] = song_result

def items(result, local, api_hw, api_wm, api_mc):
    items_result = []
    for v in (list(api_hw.values()) + list(api_wm.values()) + list(api_mc.values())):
        item = {}
        item['variants'] = len(v)
        v = v[0]
        item['name'] = v['name']['name-USen'].capitalize()
        item['name_de'] = v['name']['name-EUde'].capitalize()
        item['size'] = v['size']
        item['price'] = [v['buy-price'], v['sell-price']]
        if v['isDIY']:
            if item['name'].lower() in local['diy'].keys():
                diy = local['diy'][item['name'].lower()]
            else:
                diy = local['default-diy']
        else:
            diy = []
        item['DIY'] = diy
        item['image'] = v['image_uri']
        items_result.append(item)
    result['items'] = items_result

def update():
    api = {'fishs' : utils.json_load_url(API + 'fish'), 'sea creatures' : utils.json_load_url(API + 'sea'), 'bugs' : utils.json_load_url(API + 'bugs'),
    'fossils' : utils.json_load_url(API + 'fossils'), 'villagers' : utils.json_load_url(API + 'villagers'), 'song' : utils.json_load_url(API + 'songs'),
    'items-houseware' : utils.json_load_url(API + 'houseware'), 'items-wallmounted' : utils.json_load_url(API + 'wallmounted'), 'items-misc' : utils.json_load_url(API + 'misc')}
    local = utils.json_load('Bot/Backend/update_scripts/local_resources/ac.json')
    j = {}
    fishs(j, api['fishs'])
    sea(j, api['sea creatures'])
    bugs(j, api['bugs'])
    fossils(j, api['fossils'])
    villagers(j, api['villagers'])
    song(j, api['song'])
    items(j, local, api['items-houseware'], api['items-wallmounted'], api['items-misc'])
    j['art'] = local['art']
    utils.json_store(PATH, j)
