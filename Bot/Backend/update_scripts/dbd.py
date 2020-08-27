import Bot.Backend.constants as constants
import Bot.Backend.utils as utils
import requests
import json

PATH = 'Bot/Resources/json/deadbydaylight.json'
DATA_URL = 'https://dbd-stats.info/data/Public/'
API_1 = 'https://bridge.buddyweb.fr/api/dbd/'
API_2 = constants.DBD_REST_API

def cleanup(s):
    if not isinstance(s, str):
        return s
    to_delete = ['<b>', '</b>', '<B>', '</B>', '<span class=\"FlavorText\">', '</span>', '<li>', '</li>', '<i>', '</i>', '<span class=\"Highlight1\">', '<span class=\"Highlight2\">', '<span class=\"Highlight3\">', '<span class=\"Highlight4\">']
    t = s.strip().replace('<BR>', '\n').replace('<br>', '\n').replace('’','\'')
    for d in to_delete:
        t = t.replace(d, '')
    return t

def survivors(result, local, api_1, api_2):
    api_diff = {'Detective Tapp' : 'Detective David Tapp', 'Ashley J. Williams' : 'Ashley "Ash" Joanna Williams'}
    to_delete = ['name_tag', 'voice_actor', 'overview', 'lore', 'dlc_id', 'isfree', 'isptb']
    surv_result = []
    for s in api_1:
        surv = {}
        for (k, v) in s.items():
            if k not in to_delete:
                surv[k] = cleanup(v)
        for t in list(api_2.values()):
            if t['displayName'] == surv['name'] or (t['displayName'] in api_diff.keys() and api_diff[t['displayName']] == surv['full_name']):
                surv['image'] = DATA_URL + t['iconPath']
                surv['biography'] = cleanup(t['biography'])
                break
        if 'image' not in surv.keys():
            surv['image'] = local['default-image-surv']
        if 'biography' not in surv.keys():
            surv['biography'] = local['default']
        surv_result.append(surv)
    result['survivors'] = surv_result

def killers(result, local, api_1, api_2):
    api_diff = {'Myers' : 'Shape', 'Freddy' : 'Nightmare'}
    kill_result = []
    to_delete = ['name_tag', 'alias', 'voice_actor', 'overview', 'lore', 'dlc_id', 'isfree', 'isptb']
    for k in api_1:
        kill = {}
        for (i, v) in k.items():
            if i not in to_delete:
                if i == 'name' and v in api_diff.keys():
                    v = api_diff[v]
                elif i == 'name':
                    v = v.replace('The ', '')
                kill[i] = cleanup(v)
        for t in list(api_2.values()):
            if  t['displayName'] == 'The ' + kill['name']:
                kill['image'] = DATA_URL + t['iconPath']
                kill['biography'] = cleanup(t['biography'])
                break
        if kill['name'] in local['killers'].keys():
            kill['name_de'] = local['killers'][kill['name']]['German']
            kill['aliases'] = local['killers'][kill['name']]['Aliases']
        else:
            kill['name_de'] = local['default']
            kill['aliases'] = [local['default']]
        if 'image' not in kill.keys():
            kill['image'] = local['default-image-kill']
        if 'biography' not in kill.keys():
            kill['biography'] = local['default']
        kill_result.append(kill)
    result['killers'] = kill_result

def offerings(result, local, api_1, api_2):
    key_add = ['',' (Personal)', ' (All Survivors)', ' (All Players)']
    off_result = []
    for v in list(api_2.values()):
        off = {}
        off['name'] = cleanup(v['displayName'])
        off['description'] = cleanup(v['description'])
        local_key = None
        for k in key_add:
            if off['name'] + k in local['offerings'].keys():
                local_key = off['name'] + k
                break
        if local_key == None:
            off['name_de'] = local['default']
        else:
            off['name_de'] = local['offerings'][local_key]
        if 'iconPathList' not in v.keys():
            off['Image'] = local['default-image-offering']
        else:
            off['Image'] = DATA_URL + v['iconPathList'][0]
        off_result.append(off)
    result['offerings'] = off_result

def perks(result, local, api_1, api_2):
    api_diff = {'Detective Tapp' : 'Detective David Tapp', 'Ashley J. Williams' : 'Ashley "Ash" Joanna Williams'}
    players = api_2['characters']
    perks = api_2['perks']
    perk_result = []
    for v in list(perks.values()):
        perk = {}
        perk['name'] = v['displayName'].replace('’','\'').replace('\t', '')
        perk['description'] = cleanup(v['perkDefaultDescription'])
        if v['perkLevelTunables'] != []:
            for i in range(0, len(v['perkLevelTunables'][-1])):
                perk['description'] = perk['description'].replace('{' + '{}'.format(i) + '}', v['perkLevelTunables'][-1][i])
        if perk['description'] == '':
            desc_key = ['perkLevel{}Description'.format(i) for i in range(1,4)]
            descs = list(filter(lambda x : x !='', [v[x] for x in desc_key]))
            if descs == []:
                perk['description'] = local['default']
            else:
                perk['description'] = cleanup(descs[-1])
        perk['teachableLevel'] = v['teachableOnBloodWebLevel']
        if perk['teachableLevel'] == -1:
            perk['character'] = None
        else:
            character = players[str(v['associatedPlayerIndex'])]['displayName'].replace('The ', '')
            if character in api_diff.keys():
                character = api_diff[character]
            perk['character'] = character
        if perk['name'] in local['perks'].keys():
            perk['name_de'] = local['perks'][perk['name']]
        else:
            perk['name_de'] = local['default']
        if 'iconPathList' not in v.keys():
            perk['Image'] = local['default-image-perk']
        else:
            perk['Image'] = DATA_URL + v['iconPathList'][0]
        perk_result.append(perk)
    result['perks'] = perk_result

def update():
    local = utils.json_load('Bot/Backend/update_scripts/local_resources/dbd.json')
    api_1 = {'survivors' : utils.json_load_url(API_1 + 'survivors'), 'killers' : utils.json_load_url(API_1 + 'killers')}
    api_2 = {'characters' : utils.json_load_url(API_2 + 'characters?branch=live'), 'perks' : utils.json_load_url(API_2 + 'perks?branch=live'), 'offerings' : utils.json_load_url(API_2 + 'offerings?branch=live')}
    j = {}
    survivors(j, local, api_1['survivors'], api_2['characters'])
    killers(j, local, api_1['killers'], api_2['characters'])
    offerings(j, local, None, api_2['offerings'])
    perks(j, local, None, api_2)
    utils.json_store(PATH, j)
