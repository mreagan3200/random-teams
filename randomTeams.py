import requests
from itertools import combinations
import random

API_KEY = '' #API key goes here

tier_map = {'IRON':0, 'BRONZE': 400, 'SILVER':800, 'GOLD':1200, 'PLATINUM':1600, 
            'DIAMOND':2000, 'MASTER':2400, 'GRANDMASTER':2400, 'CHALLENGER':2400}
rank_map = {'IV': 0, 'III':100, 'II':200, 'I':300}

def getRankBySummonerName(summoner):
    query = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'+summoner+'?api_key='+API_KEY
    s = requests.get(query)
    query = 'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/'+s.json()['id']+'?api_key='+API_KEY
    s = requests.get(query)
    j = s.json()
    if len(j) > 0:
        return j[0]['tier'] + ' ' + j[0]['rank']
    else:
        return None

def getScore(summoner):
    summoner = summoner.replace(' ', '%20')
    rank = getRankBySummonerName(summoner)
    if rank is None:
        return 0
    temp = rank.split(' ')
    return tier_map[temp[0]] + rank_map[temp[1]]

def createTeams(summoner_list):
    l = [0,1,2,3,4,5,6,7,8,9]
    comb = combinations(l, 5)
    bestDivision = []
    lowest_delta = 10000
    for c in list(comb):
        team1average = 0
        team2average = 0
        for i in range(0,10):
            if i in c:
                team1average += summoner_list[i][1]
            else:
                team2average += summoner_list[i][1]
        delta = abs(team1average//5 - team2average//5)
        if delta == lowest_delta:
            bestDivision.append(list(c))
        elif delta < lowest_delta:
            lowest_delta = delta
            bestDivision = [list(c)]
    return random.choice(bestDivision), lowest_delta

def main():
    input_file = open('input.txt', 'r')
    summoner_list = []
    for line in input_file:
        line = line.replace('\n', '')
        score = getScore(line)
        summoner_list.append([line, score])
    input_file.close()
    teams,delta = createTeams(summoner_list)
    red_side = [0,1,2,3,4,5,6,7,8,9]
    output_file = open('output.txt', 'w')
    debug_file = open('debug.txt', 'w')
    output_file.write('Blue Side:\n')
    debug_file.write('Blue Side:\n')
    blueTotal = 0
    redTotal = 0
    for item in teams:
        output_file.write(summoner_list[item][0]+'\n')
        format_string = '{:<20}'+ str(summoner_list[item][1])+'\n'
        debug_file.write(format_string.format(summoner_list[item][0]))
        blueTotal += summoner_list[item][1]
        red_side.remove(item)
    output_file.write('\nRed Side:\n')
    debug_file.write('Blue Average='+str(blueTotal//5)+'\n')
    debug_file.write('\nRed Side:\n')
    for item in red_side:
        output_file.write(summoner_list[item][0] +'\n')
        format_string = '{:<20}'+ str(summoner_list[item][1])+'\n'
        debug_file.write(format_string.format(summoner_list[item][0]))
        redTotal += summoner_list[item][1]
    debug_file.write('Red Average='+str(redTotal//5)+'\n')
    debug_file.write('\nDelta='+str(delta))
    output_file.close()
    debug_file.close()

if __name__ == '__main__':
    main()
