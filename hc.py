import requests
import urllib
import json
from happycity import params
from argparse import ArgumentParser


parser = ArgumentParser(description='Selecting players stats for Clan Wars.')
parser.add_argument('division', metavar='division', type=int, help='Division: 1 or 2', default=1, nargs='?')
args = parser.parse_args()


division = 2 if args.division == 2 else 1
th_range = {1: [7, 12], 2: [1, 9]}

headers = {
    "Content-Type": "application/json",
    "authorization": "Bearer " + params['API_KEY']
}

clansUrl = (params['base_url'] + params['urls']['clans']).replace('{clanTag}', urllib.parse.quote(params['clanTag']))
print (clansUrl)

clan_response = requests.get(clansUrl, headers=headers)
print(clan_response)
#print(clan_response.text)


clan = clan_response.json()

playersUrl = params['base_url'] + params['urls']['players']

for member in clan['memberList']:
#    print(member)
#    if member['name'] != 'Vapetsy': continue

    memberTag = urllib.parse.quote(member['tag'])
    member_response = requests.get(playersUrl.replace('{playerTag}', memberTag), headers=headers)
    player = member_response.json()
    

    if (player['townHallLevel'] < th_range[division][0] or player['townHallLevel'] > th_range[division][1]):
        continue

#    print(json.dumps(player, indent=4))
#    print(player['townHallLevel'])
#    print(json.dumps(player['troops'], indent=4))
#    print(json.dumps(player['heroes'], indent=4))
#    print(json.dumps(player['spells'], indent=4))
    troops_level_sum = sum([troop['level'] for troop in player['troops'] if troop['village'] == 'home'])
  
    kl = [hero['level'] for hero in player['heroes'] if hero['name'] == 'Barbarian King']
    king_level = kl[0] if len(kl) else ''
  
    ql = [hero['level'] for hero in player['heroes'] if hero['name'] == 'Archer Queen']
    queen_level = ql[0] if len(ql) else ''
  
    wl = [hero['level'] for hero in player['heroes'] if hero['name'] == 'Grand Warden']
    warden_level = wl[0] if len(wl) else ''
  
    print("%s,%s,%s,%s,%s,%s,,%s,,%s,%s,%s,,,%s,%s" % (
        player['tag'], 
        player['name'], 
        player['role'], 
        player["townHallLevel"], 
        player['trophies'], 
        player['warStars'], 
        troops_level_sum, 
        king_level,
        queen_level,
        warden_level,
        player['donations'], 
        player['donationsReceived']
    ))

#    print ([troop['level'] for troop in player['troops'] if troop['village'] == 'home'])
#    print (troops_level_sum)
    
    

