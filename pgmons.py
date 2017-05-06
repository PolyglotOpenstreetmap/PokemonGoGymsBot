#!/home/user/polyglot/.venv/bin/python

import json,requests,time
from pogolib import *

class Job:
    def __init__(self, name='', selection = {}, coordinates = '', channelid = ''):
        self.name = name
        self.selection = selection
        self.lon1, self.lat1, self.lon2, self.lat2 = coordinates.split(',')
        self.channelid = channelid
        self.seenpokemon = {}
        wantedPokemon = self.selection 
        comment = 'Scanning area: '+ self.name  +' for: '
        self.line = ''
        for l in sorted(list(wantedPokemon)):
            c =  ''
            for p in wantedPokemon[l]:
                c += mons[p] + ', '
            if l != '0':
                self.line += "OR individual_attack + individual_defense + individual_stamina >" + l + " AND pokemon_id in (" + ','.join([str(item) for item in wantedPokemon[l]]) + ")\n"
            comment += '\nAbove ' + str(int(float(l)/45.0*100.0+0.5)) + '%:  ' + c + '\n'
        if not '0' in wantedPokemon:
             wantedPokemon['0'] = [-1]
        print(self.channelid)
        response = requests.post(url='https://api.telegram.org/bot{0}/{1}'.format(token, 'sendMessage'),
                            data={'chat_id': self.channelid, 'text': comment,'parse_mode': 'Markdown'}).json()
        print(response)
        self.query = """SELECT encounter_id, pokemon_id, latitude, longitude, disappear_time,
                               individual_attack, individual_defense, individual_stamina,
                               move_1, move_2, last_modified,
                               TIMEDIFF( DATE_SUB(disappear_time, INTERVAL -2 HOUR), NOW()) AS timeleft
                          FROM pokemon
                         WHERE DATE_SUB(disappear_time, INTERVAL -2 HOUR) > NOW()
                           AND latitude BETWEEN {1} AND {3}
                           AND longitude BETWEEN {0} AND {2}
                           AND (pokemon_id IN ({4})
                           {5}
                            );""".format(self.lon1, self.lat1, self.lon2, self.lat2,
                                         ','.join([str(item) for item in wantedPokemon['0']]),
                                         self.line)
    def performQuery(self):
    
            try:
                conn = MySQLdb.connect (host   = DBhost,
                                        user   = DBuser,
                                        passwd = DBpass,
                                        port   = 21162,
                                        db     = DBname)
            except:
                print('connection to DB failed')
                return
            try:
                cursor = conn.cursor ()
            except:
                print("couldn't get cursor")
                return
            print(self.query)
            try:
                cursor.execute (self.query)
            except:
                print("query failed")
                return
            for row in cursor.fetchall():
                if not(row[0] in self.seenpokemon):
                    '''Did we see this pokemon already in a previous query?'''
                    thisPokemon = Mon(encounterid=row[0], pokemonid=row[1], lat=row[2], lon=row[3], disappears=row[4], attack=row[5], defense=row[6], stamina=row[7], move1=row[8], move2=row[9], last_modified=row[10], timeleft=row[11],channelid = self.channelid)
                    thisPokemon.sendToTelegram()
                    self.seenpokemon[thisPokemon.encounterid] = thisPokemon
            cursor.close ()
            conn.close ()
            print

if __name__ == "__main__":
    channels = {}
    while 1:
        with open('pgm.conf', encoding='utf-8') as json_file:
            data = json.load(json_file)
        for k in data:
            if not(k in channels):
                c = Job(name=k, selection = data[k]['pokemon'], coordinates = data[k]['coordinates'], channelid = data[k]['channel'])
                channels[k] = c
            print (c)
            channels[k].performQuery()
            time.sleep(5)
        print(channels)

