from django.shortcuts import render
from django import template
import requests
import math

def score_view(request):
    return render(request, 'score/score_view.html')

def search_result(request):
    if request.method == "GET":
        summoner_name = request.GET.get('search_text')
        summoner_exist = False
        sum_result = {}
        solo_tier = {}
        team_tier = {}
        store_list = []
        gameid_list = {}
        matchid_list = {}
        spectator = False
        encryptedsummonerid = {}
        gametype_list = []
        win = 0
        alpha = 0
        participantid = 0
        win_list = []
        mykda_list = []
        mytotaldamage_list = []
        myconkill_list = []
        mychampionid_list = []
        myavgkda_list = []
        gametime_list = []
        nickname_list = [[0 for col in range(5)] for row in range(10)] #우리팀 닉네임
        damage_list = [[0 for col in range(5)] for row in range(10)] #우리팀 딜량
        championid_list = [[0 for col in range(10)] for row in range(10)]
        kill_list = [[0 for col in range(10)] for row in range(10)]
        death_list = [[0 for col in range(10)] for row in range(10)]
        assist_list = [[0 for col in range(10)] for row in range(10)]
        totaldamage_list = [[0 for col in range(10)] for row in range(10)]
        conkill_list = [[0 for col in range(10)] for row in range(10)]
        kda_list = [[0 for col in range(10)] for row in range(10)]
        api_key = 'RGAPI-7779da7e-95bf-4647-b59e-f01da5480141'

        summoner_url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(summoner_name)
        params = {'api_key': api_key}
        res = requests.get(summoner_url, params=params)
        if res.status_code == requests.codes.ok:
            summoner_exist = True
            summoners_result = res.json()
            if summoners_result:
                sum_result['name'] = summoners_result['name']
                sum_result['level'] = summoners_result['summonerLevel']
                sum_result['profileIconId'] = summoners_result['profileIconId']
                sum_result['accountId'] = summoners_result['accountId']
                account = summoners_result['accountId']

                gameid_url = "https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/" + summoners_result['accountId']
                game_info = requests.get(gameid_url, params=params)
                game_info = game_info.json()

                for i in range(0, 10):
                    gameid_list[i] = game_info['matches'][i]['gameId']

                for i in range(0, 10):
                    gametype_list.append(game_info['matches'][i]['queue'])

                for i in range(0, 10):
                    if gametype_list[i] == 450:
                        gametype_list[i] = '칼바람'
                    elif gametype_list[i] == 420:
                        gametype_list[i] = '솔랭'
                    elif gametype_list[i] == 430:
                        gametype_list[i] = '일반'
                    elif gametype_list[i] == 440:
                        gametype_list[i] = '자랭'
                    elif gametype_list[i] == 830:
                        gametype_list[i] = '봇전'
                    elif gametype_list[i] == 840:
                        gametype_list[i] = '봇전'
                    elif gametype_list[i] == 850:
                        gametype_list[i] = '봇전'
                    elif gametype_list[i] == 900:
                        gametype_list[i] = '우르프'
                    elif gametype_list[i] == 920:
                        gametype_list[i] = '포로왕'

                for i in range(0, 10):
                    match_url = "https://kr.api.riotgames.com/lol/match/v4/matches/" + str(gameid_list[i]) + "?api_key=" + str(api_key)
                    match_info = requests.get(match_url, params=params)
                    match_info = match_info.json()

                    gametime_url = "https://kr.api.riotgames.com/lol/match/v4/timelines/by-match/" + str(gameid_list[i])
                    gametime_info = requests.get(gametime_url, params=params)
                    gametime_info = gametime_info.json()
                    gametimelen = len(gametime_info['frames'])
                    gametimelen2 = round((gametime_info["frames"][gametimelen-1]['timestamp']/60000), 2)
                    gametime_list.append(gametimelen2)
                    for j in range(0, 10):
                        if account == match_info["participantIdentities"][j]["player"]["accountId"]:
                            participantid = j

                    if participantid >= 0 and participantid < 5:
                        index = 0
                        for l in range(0, 5):
                            nickname_list[i][index] = (match_info["participantIdentities"][l]["player"]["summonerName"])
                            damage_list[i][index] = (match_info["participants"][l]["stats"]["totalDamageDealtToChampions"])
                            index+=1
                    else:
                        index = 0
                        for l in range(5, 10):
                            nickname_list[i][index] = (match_info["participantIdentities"][l]["player"]["summonerName"])
                            damage_list[i][index] = (match_info["participants"][l]["stats"]["totalDamageDealtToChampions"])
                            index+=1

                    mykill = match_info["participants"][participantid]["stats"]["kills"]
                    mydeath = match_info["participants"][participantid]["stats"]["deaths"]
                    myassist = match_info["participants"][participantid]["stats"]["assists"]

                    if(mydeath == 0):
                        if mykill == 0 and myassist == 0:
                            myavgkda_list.append(0.1)
                        else:
                            myavgkda_list.append(mykill+myassist)
                    else:
                        myavgkda_list.append(round(((mykill+myassist)/mydeath),2))

                    mykda_list.append(str(mykill)+'/'+str(mydeath)+'/'+str(myassist))

                    totaldamage = match_info["participants"][participantid]["stats"]["totalDamageDealtToChampions"]
                    mytotaldamage_list.append(totaldamage)

                    mychampionid = match_info["participants"][participantid]["championId"]
                    mychampionid_list.append(mychampionid)

                    if match_info["participants"][participantid]["stats"]["pentaKills"] > 0:
                        myconkill_list.append('펜타킬')
                    elif match_info["participants"][participantid]["stats"]["quadraKills"] > 0:
                        myconkill_list.append('쿼드라킬')
                    elif match_info["participants"][participantid]["stats"]["tripleKills"] > 0:
                        myconkill_list.append('트리플킬')
                    elif match_info["participants"][participantid]["stats"]["doubleKills"] > 0:
                        myconkill_list.append('더블킬')
                    else:
                        myconkill_list.append(0)

                    if(match_info['teams'][0]['win']=="Win"):
                        if(participantid >= 5):
                            win_list.append(0)
                        else:
                            win_list.append(1)
                    else:
                        if(participantid >= 5):
                            win_list.append(1)
                        else:
                            win_list.append(0)

                    for k in range(0, 10):
                        championid_list[i][k] = match_info["participants"][k]["championId"]
                        kill_list[i][k] = match_info["participants"][k]["stats"]["kills"]
                        death_list[i][k] = match_info["participants"][k]["stats"]["deaths"]
                        assist_list[i][k] = match_info["participants"][k]["stats"]["assists"]
                        totaldamage_list[i][k] = match_info["participants"][k]["stats"]["totalDamageDealtToChampions"]
                        if match_info["participants"][k]["stats"]["pentaKills"] > 0:
                            conkill_list[i][k] = '펜타킬'
                        elif match_info["participants"][k]["stats"]["quadraKills"] > 0:
                            conkill_list[i][k] = '쿼드라킬'
                        elif match_info["participants"][k]["stats"]["tripleKills"] > 0:
                            conkill_list[i][k] = '트리플킬'
                        elif match_info["participants"][k]["stats"]["doubleKills"] > 0:
                            conkill_list[i][k] = '더블킬'
                        else:
                            conkill_list[i][k] = 0

                for i in range(0, 10):
                    for j in range(0, 10):
                        kda_list[i][j] = str(kill_list[i][j])+'/'+str(death_list[i][j])+'/'+str(assist_list[i][j])

                tier_url = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + summoners_result['id']
                tier_info = requests.get(tier_url, params=params)
                tier_info = tier_info.json()

                spectator_url = "https://kr.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/" + summoners_result['id']
                spectator_info = requests.get(spectator_url, params=params)
                spectator_info = spectator_info.json()

                if len(spectator_info) == 11:
                    spectator = True

                if len(tier_info) == 1:
                    tier_info = tier_info.pop()
                    if tier_info['queueType'] == 'RANKED_FLEX_SR':
                        team_tier['rank_type'] = '자유랭크 5:5'
                        team_tier['tier'] = tier_info['tier']
                        team_tier['rank'] = tier_info['rank']
                        team_tier['points'] = tier_info['leaguePoints']
                        team_tier['wins'] = tier_info['wins']
                        team_tier['losses'] = tier_info['losses']
                    else:
                        solo_tier['rank_type'] = '솔로랭크 5:5'
                        solo_tier['tier'] = tier_info['tier']
                        solo_tier['rank'] = tier_info['rank']
                        solo_tier['points'] = tier_info['leaguePoints']
                        solo_tier['wins'] = tier_info['wins']
                        solo_tier['losses'] = tier_info['losses']
                if len(tier_info) == 2:
                    for item in tier_info:
                        store_list.append(item)
                    solo_tier['rank_type'] = '솔로랭크 5:5'
                    solo_tier['tier'] = store_list[0]['tier']
                    solo_tier['rank'] = store_list[0]['rank']
                    solo_tier['points'] = store_list[0]['leaguePoints']
                    solo_tier['wins'] = store_list[0]['wins']
                    solo_tier['losses'] = store_list[0]['losses']

                    team_tier['rank_type'] = '자유랭크 5:5'
                    team_tier['tier'] = store_list[1]['tier']
                    team_tier['rank'] = store_list[1]['rank']
                    team_tier['points'] = store_list[1]['leaguePoints']
                    team_tier['wins'] = store_list[1]['wins']
                    team_tier['losses'] = store_list[1]['losses']

        return render(request, 'score/search_result.html',
                      {'summoner_exist': summoner_exist, 'summoners_result': sum_result, 'solo_tier': solo_tier,
                       'team_tier': team_tier, 'spectator': spectator, 'win': win, 'win_list': win_list,
                       'gametype_list': gametype_list, 'alpha': alpha, 'championid_list': championid_list,
                       'kill_list': kill_list, 'death_list': death_list, 'assist_list': assist_list,
                       'totaldamage_list': totaldamage_list, 'conkill_list': conkill_list, 'mykda_list': mykda_list,
                       'mytotaldamage_list': mytotaldamage_list, 'myconkill_list': myconkill_list, 'mychampionid_list': mychampionid_list,
                       'myavgkda_list': myavgkda_list, 'gametime_list': gametime_list, 'nickname_list': nickname_list,
                       'damage_list': damage_list})

