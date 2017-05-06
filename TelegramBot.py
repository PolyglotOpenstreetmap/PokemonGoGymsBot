#!/home/user/polyglot/.venv/bin/python
# -*- coding: utf-8 -*-

from pogolib import *
from telegram.ext import Updater
import MySQLdb
import requests, time
from TBcred import *
import pytz
local_tz = pytz.timezone('Europe/Brussels')

gyms = {}

method='sendMessage'
from TBconfig import *
if __name__ == "__main__":
    prevGymname = ''
    while 1:
        previouslyScannedGyms = []
        for g in gyms.keys():
            previouslyScannedGyms.append(g.replace('"','\\"'))
        query = """SELECT gd.name as name, g.gym_points, g.last_scanned, gp.trainer_name, gp.last_seen,
                   pokemon_id, cp, team_id, t.team, t.level, gp.iv_defense, gp.iv_attack, gp.iv_stamina
            FROM gympokemon gp
            JOIN gymmember gm ON  gp.pokemon_uid = gm.pokemon_uid 
            JOIN gym g ON  gm.gym_id = g.gym_id
            JOIN gymdetails gd ON gd.gym_id = g.gym_id
            JOIN trainer t ON t.name = gp.trainer_name
            WHERE gd.name IN ("{}")
               OR gd.name IN (SELECT gd1.name FROM gympokemon gp1
                                JOIN gymmember gm1 ON  gp1.pokemon_uid = gm1.pokemon_uid
                                JOIN gym g1 ON  gm1.gym_id = g1.gym_id
                                JOIN gymdetails gd1 ON gd1.gym_id = g1.gym_id 
                                WHERE gp1.trainer_name IN ("{}"))
            ORDER BY name;""".format('","'.join(list(set(gymsToScan + previouslyScannedGyms))).replace("'","''"),
                                     '","'.join(trainersOfInterest))
        try:
            conn = MySQLdb.connect (host   = DBhost,
                                    user   = DBuser,
                                    passwd = DBpass,
                                    port   = 21162,
                                    db     = DBname)
        except:
            print('connection to DB failed')
            time.sleep(60)
            continue
        try:
            cursor = conn.cursor ()
        except:
            print("couldn't get cursor")
            time.sleep(60)
            continue
        print(query)
        try:
            cursor.execute (query)
        except:
            print("query failed")
            time.sleep(60)
            continue
        for row in cursor.fetchall():
            if not(prevGymname) or row[0] != prevGymname:
                '''Either first time through loop, or next gym'''
                if prevGymname and row[0] != thisGym.name:
                    '''All defenders were added for current gym'''
                    if row[0] in gyms.keys():
                        '''Did we see this gym already in a previous query?'''
                        if thisGym.name in gyms and id(thisGym) != id(gyms[thisGym.name]):
                            thisGym.compareWithGym(gyms[thisGym.name])
                            cpdifference = sum(gyms[thisGym.name].cpDefenders()) - sum(thisGym.cpDefenders())
                            teamchanged = False
                            if gyms[thisGym.name].team != thisGym.team: teamchanged = True
                            prestigedifference = gyms[thisGym.name].prestige - thisGym.prestige
                            thumbs = ''
                            if teamchanged:
                                if thisGym.team == ownTeam:
                                    thumbs = '👍'
                                else:
                                    thumbs = '👎'
                            else:
                               if prestigedifference < 0:
                                   arrow = '↗' 
                                   if thisGym.team == ownTeam:
                                       thumbs = '👍'
                                   else:
                                       thumbs = '👎'
                               elif prestigedifference == 0:
                                   arrow = '' 
                               else:
                                   arrow = '↘' 
                                   if thisGym.team == ownTeam:
                                       thumbs = '👎'
                                   else:
                                       thumbs = '👍'

                            if cpdifference or thisGym.prestige==0:
                                print ()
                                print (thisGym)
                                print ()
                                response = requests.post(url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
                                data={'chat_id': channelid, 'text': thumbs + arrow + symbols[thisGym.team] + ' ' + str(thisGym),'parse_mode': 'Markdown'}).json()
                    oldgym = None
                    if thisGym.name in gyms:
                        oldGym = gyms[thisGym.name]
                    gyms[thisGym.name]=thisGym
                    if oldgym:
                        del(oldGym)
                thisGym = Gym(name=row[0], prestige=row[1], team=row[7], last_scanned=row[2])
                prevGymname = thisGym.name
            defender = Defender(trainer=row[3], last_seen=row[4], pokemonid=row[5], cp=row[6], team=row[8], level=row[9], attack=row[11], defense=row[10], stamina=row[12])
            thisGym.addDefender(defender)
        cursor.close ()
        conn.close ()
        time.sleep(60)
        print()
