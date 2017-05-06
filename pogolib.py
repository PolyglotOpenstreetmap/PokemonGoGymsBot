#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from telegram.ext import Updater
import MySQLdb
from TBcred import *
import pytz, requests
local_tz = pytz.timezone('Europe/Brussels')

teams={0: 'No team', 1: 'Mystic', 2: 'Valor', 3: 'Instinct'}
symbols={0: '', 1: '💙', 2: '♥️', 3: '💛'}
numbers=['','①','②','③','④','⑤','⑥','⑦','⑧','⑨','⑩','⑪','⑫','⑬','⑭','⑮']

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
       150: 'Mewtwo',151: 'Mew', 152: 'Chikorita', 153: 'Bayleef', 154: 'Meganium',
       155: 'Cyndaquil', 156: 'Quilava', 157: 'Thyphlosion', 158: 'Totodile', 159: 'Croconaw', 160: 'Feraligatr',
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
       195: 'Quagsire', 196: 'Espeon', 197: 'Umbreon',
       198: 'Murkrow', 199: 'Slowking', 200: 'Misdreavus',
       201: 'Unown', 202: 'Wobbuffet', 203: 'Girafarig',
       204: 'Pineco', 205: 'Forretress', 206: 'Dunsparce',
       207: 'Gligar', 208: 'Steelix', 209: 'Snubbull', 210: 'Granbull',
       211: 'Qwilfish', 212: 'Scizor', 213: 'Shuckle', 214: 'Heracross',
       215: 'Sneasel', 216: 'Teddiursa', 217: 'Ursaring',
       218: 'Slugma', 219: 'Magcargo', 220: 'Swinub',
       221: 'Piloswine', 222: 'Corsola', 223: 'Remoraid',
       224: 'Octillery', 225: 'Delibird', 226: 'Mantine',
       227: 'Skarmory', 228: 'Houndour', 229: 'Houndoom',
       231: 'Phanpy', 232: 'Donphan', 233: 'Porygon2', 234: 'Stantler',
       235: 'Smeargle', 236: 'Tyrogue', 237: 'Hitmontop',
       238: 'Smoochum', 239: 'Elekid', 240: 'Magby',
       241: 'Miltank', 242: 'Blissey', 243: 'Raikou', 244: 'Entei',
       245: 'Suicune', 246: 'Larvitar', 247: 'Pupitar',
       248: 'Tyranitar', 249: 'Lugia', 250: 'Ho-Oh',
       251: 'Celebi'}

class Defender:
    def __init__(self, trainer, pokemonid, cp = 0, last_seen=None, team=0, level=0, attack='', defense='', stamina=''):
        self.trainer = trainer
        self.pokemonid = pokemonid
        self.cp = cp
        self.last_seen = str(last_seen.replace(tzinfo=pytz.utc).astimezone(local_tz))[11:19]
        self.team = team
        self.level = level
        self.new = False
        self.attack = int(attack)
        self.defense = int(defense)
        self.stamina = int(stamina)
        self.iv = (self.attack + self.defense + self.stamina) / 45 * 100.0
    def markup(self):
        if self.new:
            return '`{:3.0f} {}{}{}`\t_{}{:>5}_ `{:<10}` *{} {}*👈'.format(self.iv, numbers[self.attack], numbers[self.defense], numbers[self.stamina], symbols[self.team],self.cp,mons.setdefault(self.pokemonid, self.pokemonid), self.level, self.trainer)
        else:
            return '`{:3.0f} {}{}{}`\t_{}{:>5}_ `{:<10}` *{} {}*'.format(self.iv, numbers[self.attack], numbers[self.defense], numbers[self.stamina], symbols[self.team],self.cp,mons.setdefault(self.pokemonid, self.pokemonid), self.level, self.trainer)

class Gym:
    levels=[0, 2000, 4000, 8000, 12000, 16000, 20000, 30000, 40000, 50000]

    def __init__(self, name = '', prestige = 0, team=0, last_scanned=None, location=''):
        self.name = name
        self.prestige = int(prestige)
        self.last_scanned = str(last_scanned.replace(tzinfo=pytz.utc).astimezone(local_tz))[0:19]
        self.defenders = {}
        self.team = team
        self.RIP = []
        self.location = location
    def getLevel(self):
        if self.prestige >= self.levels[-1]: return '10 (0)'
        level = 9; slots = 0
        for l in range(9, 1, -1):
            print (self.prestige, l, self.levels[l], self.levels[l-1])
            if self.prestige < self.levels[l] and self.prestige >= self.levels[l-1]:
                level = l
                slots = level - len(self.defenders)
                #if slots > 0:
                #    if self.prestige+4000 >= self.levels[l-1]: slots += 1
                    #elif self.prestige+2000 >= self.levels[l]: slots += 1
                break
        
        return str(level)# + ' (' + str(slots) + ')'
    def addDefender(self, defender): 
        self.defenders[defender.trainer] = defender
    def getDefenders(self, arg):
        return (arg[1].cp, arg[1].trainer)
    def sortedDefenders(self):
        return sorted(self.defenders.items(), key=self.getDefenders, reverse=True)
    def cpDefenders(self):
        cp = []
        for d in self.defenders:
            cp.append(self.defenders[d].cp)
        return cp
    def compareWithGym(self,prevGym = None):
        if prevGym:
            prevDefenders = prevGym.defenders.copy()
            curDefenders  = self.defenders.copy()
            for d in prevGym.defenders:
                if d in curDefenders:
                    curDefenders.pop(d)
                    prevDefenders.pop(d)
            if prevDefenders:
                print (prevGym.name, ' RIP: ', prevDefenders)
                for d in prevDefenders:
                    self.RIP.append(prevGym.defenders[d])
            for d in curDefenders:
                self.defenders[d].new = True
                print (d)
    def __str__(self):
        markup= '{} *{:<40}*{}\n{}\n`{:<40}`_{:>5}_\n\n'.format(self.getLevel(), self.name, teams[self.team], self.location, str(self.last_scanned), self.prestige)
        for d in self.sortedDefenders():
            markup+=d[1].markup() + '\n'
        markup+='\n'
        for d in self.RIP:
            print (d)
            markup+='💤' + d.markup() + '\n'
        return markup

class Mon:
    def __init__(self, encounterid, pokemonid, lat, lon, disappears,
           attack, defense, stamina, move1, move2, last_modified, timeleft,
           channelid):
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
        try:
            self.iv = (int(self.attack) + int(self.defense) + int(self.stamina)) / 45.0 * 100.0
        except:
            self.iv = 0
        self.channelid = channelid
    def sendToTelegram(self):
        print()
        print(self)
        print()
        markup = '*{} {:.0f} ({}|{}|{}) {}|{} \nAvailable until: {} ({})*'.format(mons[self.pokemonid], self.iv, self.attack, self.defense, self.stamina, self.move1, self.move2, self.disappears, self.timeleft)
        response = requests.post(url='https://api.telegram.org/bot{0}/{1}'.format(token, 'sendMessage'),
                                data={'chat_id': self.channelid, 'text': markup,'parse_mode': 'Markdown'}).json()
        print(response)
        response = requests.post(url='https://api.telegram.org/bot{0}/{1}'.format(token, 'sendLocation'),
                                data={'chat_id': self.channelid, 'latitude': self.lat, 'longitude': self.lon,}).json()
        print(response)
