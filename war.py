from coc import ClashOfClans
from init import params
import json
from pprint import pprint

coc = ClashOfClans(bearer_token = params['API_KEY'])
r = coc.clans('#908PG8L8').currentwar().get()

# pprint (r)

byPlayerResults = []

print ("===== General results =====")
print ("Tag,\tName,\tAttacks,\tStars")

for member in r['clan']['members']:
    stars = sum([attack['stars'] for attack in member['attacks']])
    print ("%s,%s,%s,%s" % (member['tag'], member['name'], len(member['attacks']), stars))
    r0 = {}
    r0['tag'] = member['tag']
    r0['name'] = member['name']
    r0['townhallLevel'] = member['townhallLevel']

    for attack in member['attacks']:
        result = r0.copy()
        result['stars'] = attack['stars']
        result['destructionPercentage'] = attack['destructionPercentage']

        opponent = coc.players(attack['defenderTag']).get()
        result['opponentTownhallLevel'] = opponent['townHallLevel']

        byPlayerResults.append(result)


print ("===== By players results =====")
print ("Tag,\tName,\tTownHall Level,\tStars,\tDesctruction Percentage,\tOpponent TownHall Level")
for result in byPlayerResults:
    print("%s,%s,%s,%s,%s,%s" % (
        result['tag'],
        result['name'],
        result['townhallLevel'],
        result['stars'],
        result['destructionPercentage'],
        result['opponentTownhallLevel']
    ))