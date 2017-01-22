#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from telegram.ext import Updater
import MySQLdb
import requests, time
from TBcred import *
import pytz
local_tz = pytz.timezone('Europe/Brussels')

teams={0: 'No team', 1: 'Mystic', 2: 'Valor', 3: 'Instinct'}
symbols={0: '', 1: '💙', 2: '♥️', 3: '💛'}

mons ={1: 'Bulbasaur',2: 'Ivysaur',3: 'Venusaur',4: 'Charmander',5: 'Charmeleon',6: 'Charizard',
       7: 'Squirtle',8: 'Wartortle',9: 'Blastoise',10: 'Caterpie',11: 'Metapod',12: 'Butterfree',
       13: 'Weedle',14: 'Kakuna',15: 'Beedrill',16: 'Pidgey',17: 'Pidgeotto',18: 'Pidgeot',
       19: 'Rattata',20: 'Raticate',21: 'Spearow',22: 'Fearow',23: 'Ekans',24: 'Arbok',
       25: 'Pikachu',26: 'Raichu',27: 'Sandshrew',28: 'Sandslash',
       29: 'Nidoran, F', 30: 'Nidorina',31: 'Nidoqueen',32: 'Nidoran, M', 33: 'Nidorino',34: 'Nidoking',
       35: 'Clefairy',36: 'Clefable',37: 'Vulpix',38: 'Ninetales',39: 'Jigglypuff',40: 'Wigglytuff',
       41: 'Zubat', 42: 'Golbat',43: 'Oddish',44: 'Gloom',45: 'Vileplume',46: 'Paras',47: 'Parasect',
       48: 'Venonat',49: 'Venomoth',50: 'Diglett',51: 'Dugtrio',52: 'Meowth',53: 'Persian',
       54: 'Psyduck',55: 'Golduck',56: 'Mankey',57: 'Primeape',58: 'Growlithe',59: 'Arcanine',
       60: 'Poliwag',61: 'Poliwhirl',62: 'Poliwrath',63: 'Abra',64: 'Kadabra',65: 'Alakazam',
       66: 'Machop',67: 'Machoke',68: 'Machamp',69: 'Bellsprout',70: 'Weepinbell',71: 'Victreebel',
       72: 'Tentacool',73: 'Tentacruel',74: 'Geodude',75: 'Graveler',76: 'Golem',
       77: 'Ponyta',78: 'Rapidash',79: 'Slowpoke',80: 'Slowbro',81: 'Magnemite',82: 'Magneton',
       83: "Farfetch'd",84: 'Doduo',85: 'Dodrio',86: 'Seel',87: 'Dewgong',
       88: 'Grimer',89: 'Muk',90: 'Shellder',91: 'Cloyster',92: 'Gastly',93: 'Haunter',
       94: 'Gengar',95: 'Onix',96: 'Drowzee',97: 'Hypno',98: 'Krabby',
       99: 'Kingler',100: 'Voltorb',101: 'Electrode',102: 'Exeggcute',103: 'Exeggutor',
       104: 'Cubone',105: 'Marowak',106: 'Hitmonlee',107: 'Hitmonchan',
       108: 'Lickitung',109: 'Koffing',110: 'Weezing',111: 'Rhyhorn',112: 'Rhydon',
       113: 'Chansey',114: 'Tangela',115: 'Kangaskhan',116: 'Horsea',117: 'Seadra',
       118: 'Goldeen',119: 'Seaking',120: 'Staryu',121: 'Starmie',
       122: 'Mr. Mime',123: 'Scyther',124: 'Jynx',125: 'Electabuzz',
       126: 'Magmar',127: 'Pinsir',128: 'Tauros',129: 'Magikarp',130: 'Gyarados',
       131: 'Lapras',132: 'Ditto',133: 'Eevee',134: 'Vaporeon',135: 'Jolteon',136: 'Flareon',
       137: 'Porygon',138: 'Omanyte',139: 'Omastar',140: 'Kabuto',141: 'Kabutops',
       142: 'Aerodactyl',143: 'Snorlax',144: 'Articuno',145: 'Zapdos',146: 'Moltres',
       147: 'Dratini',148: 'Dragonair',149: 'Dragonite',
       150: 'Mewtwo',151: 'Mew',
       169: 'Crobat', 182: 'Bellossom', 186: 'Politoed',
       230: 'Kingdra', 154: 'Meganium', 155: 'Cyndaquil',
       156: 'Quilava', 157: 'Typhlosion', 158: 'Totodile',
       159: 'Croconaw', 160: 'Feraligatr', 161: 'Sentret',
       162: 'Furret', 163: 'Hoothoot', 164: 'Noctowl',
       165: 'Ledyba', 166: 'Ledian', 167: 'Spinarak',
       168: 'Ariados', 170: 'Chinchou', 171: 'Lanturn',
       172: 'Pichu', 173: 'Cleffa', 174: 'Igglybuff',
       175: 'Togepi', 176: 'Togetic', 177: 'Natu',
       178: 'Xatu', 179: 'Mareep', 180: 'Flaaffy',
       181: 'Ampharos', 183: 'Marill', 184: 'Azumarill',
       185: 'Sudowoodo', 187: 'Hoppip', 188: 'Skiploom',
       189: 'Jumpluff', 190: 'Aipom', 191: 'Sunkern',
       192: 'Sunflora', 193: 'Yanma', 194: 'Wooper',
       195: 'Quagsire', 198: 'Murkrow', 200: 'Misdreavus',
       201: 'Unown', 202: 'Wobbuffet', 203: 'Girafarig',
       204: 'Pineco', 205: 'Forretress', 206: 'Dunsparce',
       207: 'Gligar', 209: 'Snubbull', 210: 'Granbull',
       211: 'Qwilfish', 213: 'Shuckle', 214: 'Heracross',
       215: 'Sneasel', 216: 'Teddiursa', 217: 'Ursaring',
       218: 'Slugma', 219: 'Magcargo', 220: 'Swinub',
       221: 'Piloswine', 222: 'Corsola', 223: 'Remoraid',
       224: 'Octillery', 225: 'Delibird', 226: 'Mantine',
       227: 'Skarmory', 228: 'Houndour', 229: 'Houndoom',
       231: 'Phanpy', 232: 'Donphan', 234: 'Stantler',
       235: 'Smeargle', 236: 'Tyrogue', 237: 'Hitmontop',
       238: 'Smoochum', 239: 'Elekid', 240: 'Magby',
       241: 'Miltank', 243: 'Raikou', 244: 'Entei',
       245: 'Suicune', 246: 'Larvitar', 247: 'Pupitar',
       248: 'Tyranitar', 249: 'Lugia', 250: 'Ho-Oh',
       251: 'Celebi'}

class Mon:
    def __init__(self, encounterid, pokemonid, lat, lon, disappears,
	   attack, defense, stamina, move1, move2, last_modified, timeleft):
        self.encounterid = encounterid 
        self.pokemonid = pokemonid
        self.lat = lat; self.lon = lon 
        self.disappears = str(disappears.replace(tzinfo=pytz.utc).astimezone(local_tz))[11:19]
        self.timeleft = str(timeleft)[2:]
        self.last_modified = str(last_modified.replace(tzinfo=pytz.utc).astimezone(local_tz))[11:19]
        self.attack = attack 
        self.defense = defense
        self.stamina = stamina
        self.move1 = move1; self.move2 = move2
        self.iv = (self.attack + self.defense + self.stamina) / 45.0 * 100.0   
    def sendToTelegram(self):
        print
        print self
        print
        markup = '*{} {:.0f} ({}|{}|{}) {}|{} \nAvailable until: {} ({})*'.format(mons[self.pokemonid], self.iv, self.attack, self.defense, self.stamina, self.move1, self.move2, self.disappears, self.timeleft)
        response = requests.post(url='https://api.telegram.org/bot{0}/{1}'.format(token, 'sendMessage'),
                                data={'chat_id': channelidmons, 'text': markup,'parse_mode': 'Markdown'}).json()
        print response
        response = requests.post(url='https://api.telegram.org/bot{0}/{1}'.format(token, 'sendLocation'),
                                data={'chat_id': channelidmons, 'latitude': self.lat, 'longitude': self.lon,}).json()
        print response

pokemon = {}

from TBconfig import *
if __name__ == "__main__":
    wantedPokemon = [65,112,113,130,131,143,149]
    comment = 'Scanning DB for: '
    for p in wantedPokemon:
        comment += mons[p] + ', '
    response = requests.post(url='https://api.telegram.org/bot{0}/{1}'.format(token, 'sendMessage'),
                            data={'chat_id': channelidmons, 'text': comment[:-2],'parse_mode': 'Markdown'}).json()
    while 1:
        query = """SELECT encounter_id, pokemon_id, latitude, longitude, disappear_time,
	                  individual_attack, individual_defense, individual_stamina,
                          move_1, move_2, last_modified, TIMEDIFF(disappear_time, NOW()) AS timeleft
                     FROM pokemon
                    WHERE disappear_time > NOW()
                      AND last_modified > NOW() - INTERVAL 30 MINUTE
                      AND latitude BETWEEN {} AND {}
                      AND longitude BETWEEN {} AND {}
                      AND pokemon_id IN ({});""".format(50.84,50.89,4.66,4.77,','.join([str(item) for item in wantedPokemon]))
                       #OR (individual_attack + individual_defense + individual_stamina)>43);"""
        try:
            conn = MySQLdb.connect (host   = DBhost,
                                    user   = DBuser,
                                    passwd = DBpass,
                                    db     = DBname)
        except:
            print 'connection to DB failed'
            time.sleep(60)
            continue
        try:
            cursor = conn.cursor ()
        except:
            print "couldn't get cursor"
            time.sleep(60)
            continue
        print query
        try:
            cursor.execute (query)
        except:
            print "query failed"
            time.sleep(60)
            continue
        for row in cursor.fetchall():
            if not(row[0] in pokemon):
                '''Did we see this pokemon already in a previous query?'''
                thisPokemon = Mon(encounterid=row[0], pokemonid=row[1], lat=row[2], lon=row[3], disappears=row[4], attack=row[5], defense=row[6], stamina=row[7], move1=row[8], move2=row[9], last_modified=row[10], timeleft=row[11])
                thisPokemon.sendToTelegram()
                pokemon[thisPokemon.encounterid] = thisPokemon
        cursor.close ()
        conn.close ()
        time.sleep(20)
        print

