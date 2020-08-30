import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
import requests
import json
from bs4 import BeautifulSoup
from copy import deepcopy
import re
from concurrent.futures import ThreadPoolExecutor

PATH = 'Bot/Resources/json/deadbydaylight.json'

API = {}
DATA_URL = 'https://dbd-stats.info/data/Public/'
LOCAL = utils.json_load('Bot/Backend/update_scripts/local_resources/dbd.json')


def cleanup(s):
    if not isinstance(s, str):
        return s
    to_delete = ['<b>', '</b>', '<B>', '</B>', '<span class=\"FlavorText\">', '</span>', '<li>', '</li>', '<i>', '</i>', '<span class=\"Highlight1\">', '<span class=\"Highlight2\">', '<span class=\"Highlight3\">', '<span class=\"Highlight4\">']
    t = s.strip().replace('<BR>', '\n').replace('<br>', '\n').replace('’','\'')
    for d in to_delete:
        t = t.replace(d, '')
    return t

# >> Get Information
def json_killer(api):
    killer = deepcopy(LOCAL['default-killer'])
    killer['displayName'] = api['displayName'].replace('The ', '')
    if killer['displayName'] in LOCAL['killers'].keys():
        killer['alias'] = LOCAL['killers'][killer['displayName']]['Aliases']
        killer['displayName_de'] = LOCAL['killers'][killer['displayName']]['German'] if killer['displayName'] != LOCAL['killers'][killer['displayName']]['German'] else None
    url = constants.DBD_WIKI_URL + killer['displayName']
    try:
        response = requests.get(url)
        page = BeautifulSoup(response.content, 'lxml')
    except:
        page = None
    if page != None:
        killer['url'] = url
        infobox = page.find('table', class_='infoboxtable').find_all('tr')
        killer['fullName'] = infobox[2].find_all('td')[1].text.replace('\n', ' ').strip()
        for k in killer.keys():
            for row in infobox[3:]:
                cols = row.find_all('td')
                if k.replace('_', ' ') in cols[0].text.lower():
                    killer[k] = cols[1].text.replace('\n', ' ').strip()
                    break
        if killer['dlc'] == '(?)':
            killer['dlc'] = 'Base Game'
        perks = page.find('span', id='Overview').parent.findNext(string=re.compile('personal Perks')).parent.find_all('a')
        result_perks = []
        for i in range(0,len(perks)//2):
            result_perks.append('[{}]({})'.format(perks[i*2]['title'],constants.DBD_WIKI_URL[:-1] + perks[i*2]['href']))
        killer['perks'] = result_perks
    if 'difficulty' in api.keys():
        killer['difficulty'] = api['difficulty'].replace('ECharacterDifficulty::VE_', '').strip()
    if 'biography' in api.keys() and api['biography'] != '' and api['biography'] != None:
        killer['biography'] = cleanup(api['biography'])
    if 'iconPath' in api.keys() and api['iconPath'] != '' and api['iconPath'] != None:
        killer['image'] = DATA_URL + api['iconPath']
    return killer

def json_survivor(api):
    url_diff = {'https://deadbydaylight.gamepedia.com/Ashley_J._Williams' : 'https://deadbydaylight.gamepedia.com/Ash_J._Williams'}
    survivor = deepcopy(LOCAL['default-survivor'])
    survivor['fullName'] = api['displayName']
    url = constants.DBD_WIKI_URL + survivor['fullName'].replace(' ','_')
    if url in url_diff.keys():
        url = url_diff[url]
    try:
        response = requests.get(url)
        page = BeautifulSoup(response.content, 'lxml')
    except:
        page = None
    if page != None:
        survivor['url'] = url
        infobox = page.find('table', class_='infoboxtable').find_all('tr')
        survivor['displayName'] = infobox[0].text.replace('\n', ' ').strip()
        if survivor['displayName'] == survivor['fullName']:
            survivor['fullName'] = None
        for k in survivor.keys():
            for row in infobox[2:]:
                cols = row.find_all('td')
                if cols[0].text.lower() == 'Alt. Name' and survivor['fullName'] == None:
                    survivor['fullName'] = cols[1].text.replace('\n', ' ').strip() # Laurie Strode == Cynthia Myers
                elif k in cols[0].text.lower():
                    survivor[k] = cols[1].text.replace('\n', ' ').strip()
                    break
        if survivor['dlc'] == '(?)':
            survivor['dlc'] = 'Base Game'
        perks = page.find('span', id='Overview').parent.findNext(string=re.compile('personal Perks')).parent.find_all('a')
        result_perks = []
        for i in range(0,len(perks)//2):
            result_perks.append('[{}]({})'.format(perks[i*2]['title'],constants.DBD_WIKI_URL[:-1] + perks[i*2]['href']))
        survivor['perks'] = result_perks
    if 'difficulty' in api.keys():
        survivor['difficulty'] = api['difficulty'].replace('ECharacterDifficulty::VE_', '').strip()
    if 'biography' in api.keys() and api['biography'] != '' and api['biography'] != None:
        survivor['biography'] = cleanup(api['biography'])
    if 'iconPath' in api.keys() and api['iconPath'] != '' and api['iconPath'] != None:
        survivor['image'] = DATA_URL + api['iconPath']
    return survivor

def json_characters(result):
    result_survivors = []
    result_killers = []
    for v in list(API['characters'].values()):
        if v['role'] == 'EPlayerRole::VE_Camper':
            result_survivors.append(json_survivor(v))
        elif v['role'] == 'EPlayerRole::VE_Slasher':
            result_killers.append(json_killer(v))
    result['survivors'] = result_survivors
    result['killers'] = result_killers

def json_offerings(result):
    key_add = ['',' (Personal)', ' (All Survivors)', ' (All Players)']
    off_result = []
    for v in list(API['offerings'].values()):
        off = deepcopy(LOCAL['default-offering'])
        off['displayName'] = v['displayName']
        off['description'] = cleanup(v['description'])
        for k in key_add:
            if off['displayName'] + k in LOCAL['offerings'].keys():
                off['displayName_de'] = off['displayName'] + k
                break
        if 'iconPathList' in v.keys():
            off['image'] = DATA_URL + v['iconPathList'][0]
        off['url'] = constants.DBD_WIKI_URL + off['displayName'].replace(' ', '_')
        off_result.append(off)
    result['offerings'] = off_result

def json_perks(result):
    perk_result = []
    for v in list(API['perks'].values()):
        perk = deepcopy(LOCAL['default-perk'])
        perk['displayName'] = v['displayName']
        if perk['displayName'] in LOCAL['perks'].keys():
            perk['displayName_de'] = LOCAL['perks'][perk['displayName']]
        desc = cleanup(v['perkDefaultDescription']) if v['perkDefaultDescription'] != '' else cleanup(v['perkLevel3Description'])
        if v['perkLevelTunables'] != []:
            for i in range(0, len(v['perkLevelTunables'][-1])):
                desc = desc.replace('{' + '{}'.format(i) + '}', v['perkLevelTunables'][-1][i])
        perk['description'] = desc
        if v['associatedPlayerIndex'] == -1:
            perk['isTeachable'] = False
        else:
            perk['isTeachable'] = True
            perk['teachableInfo']['character'] = API['characters'][str(v['associatedPlayerIndex'])]['displayName'].replace('The ', '')
            perk['teachableInfo']['lvl'] = v['teachableOnBloodWebLevel']
        if 'iconPathList' in v.keys():
            perk['image'] = DATA_URL + v['iconPathList'][0]
        perk['url'] = constants.DBD_WIKI_URL + perk['displayName'].replace(' ', '_')
        perk_result.append(perk)
    result['perks'] = perk_result

def update():
    result = {}
    api_keys = ['characters', 'perks', 'offerings']
    functions = [json_characters, json_offerings, json_perks]
    for k in api_keys:
        API[k] = utils.json_load_url(constants.DBD_REST_API + '{}?branch=live'.format(k))
    with ThreadPoolExecutor(max_workers=len(functions)) as executor:
        executor.map(utils.map_function, [[func, result] for func in functions])
    utils.json_store(PATH, result)