#!/usr/bin/env python
import json


def show_room(room):
    # nazov a opis miestnosti
    print(f'Nachádzaš sa v miestnosti {room["name"]}.')
    print(room['description'])

    # vypis vychodov z miestnosti
    if room['exits']['east'] == None and room['exits']['west'] == None and room['exits']['south'] == None and room['exits']['north'] == None:
        print('Z miestnosti neexistujú žiadne východy.')
    else:
        print('Možné východy z miestnosti:')
        if room['exits']['east'] != None:
            print('  vychod')
        if room['exits']['west'] != None:
            print('  zapad')
        if room['exits']['south'] != None:
            print('  juh')
        if room['exits']['north'] != None:
            print('  sever')

    # vypis predmetov v miestnosti
    if len(room['items']) == 0:
        print('Nevidíš tu nič zaujímavé.')
    else:
        print('Vidíš:')
        for item in room['items']:
            print(f'  {item["name"]}')


def cmd_about():
    print('(c)2021 by mirek na mocnom Pythoňáckom kurze spáchal.')
    print('Táto mocná hra je o...')


def cmd_inventory(backpack):
    if len(backpack) == 0:
        print('Batoh je prázdny.')
    else:
        print('V batohu máš:')
        for item in backpack:
            print(f'  {item["name"]}')


def cmd_commands():
    print('Zoznam akutálne dostupných príkazov:')
    print('o hre - zobrazí informácie o hre')
    print('koniec - ukončí hru')
    print('prikazy - zobrazi zoznam prikazov')
    print('zapad - prejdeš na západ')
    print('rozhliadni sa - zobrazí opis aktuálnej miestnosti')


def cmd_look_around(current_room):
    show_room(current_room)


def cmd_explore(backpack, current_room, line):
    cmd = line.split(maxsplit=1)
    if len(cmd) == 1:
        print('Čo chceš preskúmať?')
    else:
        name = cmd[1]

        found = False
        for item in current_room['items'] + backpack:
            if item['name'] == name:
                print(item['description'])
                found = True
                break

        if found == False:
            print('Taký predmet tu nikde nevidím.')


def cmd_drop(backpack, current_room, line):
    cmd = line.split(maxsplit=1)
    if len(cmd) == 1:
        print('Neviem, čo chceš položiť.')
    else:
        name = cmd[1]
        found = False
        for item in backpack:
            if item['name'] == name:
                backpack.remove(item)
                current_room['items'].append(item)
                print(f'Do miestnosti si položil {item["name"]}.')
                found = True
                break
        if found == False:
            print('Taký predmet u seba nemáš.')


def cmd_take(backpack, current_room, line):
    cmd = line.split(maxsplit=1)
    if len(cmd) == 1:
        print('Neviem, čo chceš zobrať.')
    else:
        name = cmd[1]
        found = False
        for item in current_room['items']:

            if item['name'] == name:
                if 'movable' in item['features']:
                    current_room['items'].remove(item)
                    backpack.append(item)
                    print(f'Do batohu si vložil {item["name"]}.')
                else:
                    print('Tento predmet sa nedá zobrať.')

                found = True
                break

        if found == False:
            print(
                f'Taký predmet v miestnosti {current_room["name"]} nevidím.')


def cmd_use(backpack, current_room, line):
    cmd = line.split(maxsplit=1)
    if len(cmd) == 1:
        print('Co chces pouzit?')
    else:
        name = cmd[1]
        found = False
        for item in current_room['items'] + backpack:
            if item['name'] == name:
                if 'usable' in item['features']:
                    print(f'Pouzivam predmet {item["name"]}')
                else:
                    print((f'{item["name"]} sa neda pouzit.').capitalize())

                found = True
                break
        if found == False:
            print('Taky predmet tu nikde nevidim.')


def cmd_east(room, world):
    name = room['exits']['east']
    if name != None:
        room = world[name]
        show_room(room)
    else:
        print('Tam sa nedá ísť.')

    return room


def cmd_west(current_room, world):
    name = current_room['exits']['west']
    if name != None:
        current_room = world[name]
        show_room(current_room)
    else:
        print('Tam sa nedá ísť.')

    return current_room


def cmd_north(current_room, world):
    name = current_room['exits']['north']
    if name != None:
        current_room = world[name]
        show_room(current_room)
    else:
        print('Tam sa nedá ísť.')

    return current_room


def cmd_south(current_room, world):
    name = current_room['exits']['south']
    if name != None:
        current_room = world[name]
        show_room(current_room)
    else:
        print('Tam sa nedá ísť.')

    return current_room


line = None

"""
+-------+     +-------------+
|  hall |-----| living room |
+-------+     +-------------+          N
    |                                  ^
    |                              W < o > E
+---------+                            v
| dungeon |                            S
+---------+
"""

# nacitanie sveta z json suboru
file = open('world.json', 'r', encoding='utf-8')
world = json.load(file)
file.close()

# rozmiestnenie veci do sveta
teplaky = {
    'name': 'teplaky',
    'description': 'Parádne tepláky ružovej farby. Asi pána domáceho. Súdiac podľa veľkosti.',
    'features': ['movable', ]
}

kanister = {
    'name': 'kanister',
    'description': 'Vojenský kanister na 20l. Odštroboval si zátku, čuchol si a rovno si ju zašroboval naspäť. Fuj benzín. Ešte že nie som fajčiar.',
    'features': ['movable', 'usable']
}

dvere = {
    'name': 'vchodove dvere',
    'description': 'Masívne dubové vchodové dvere s dvoma zámkami. Toto asi nebude len tak obyčaný bytík nejakého študentíka.',
    'features': []
}

world['chodba']['items'].append(dvere)

# world['chodba']['items'].append(teplaky)
# world['chodba']['items'].append(kanister)


# game init
current_room = world['chodba']
backpack = []
backpack.append(kanister)
backpack.append(teplaky)


print(' _____                            ____                       ')
print('| ____|___  ___ __ _ _ __   ___  |  _ \ ___   ___  _ __ ___  ')
print('|  _| / __|/ __/ _` | \'_ \\ / _ \\ | |_) / _ \\ / _ \\| \'_ ` _ \\ ')
print('| |___\__ \ (_| (_| | |_) |  __/ |  _ < (_) | (_) | | | | | |')
print('|_____|___/\___\__,_| .__/ \___| |_| \_\___/ \___/|_| |_| |_|')
print('                    |_|                                      ')
print('                                   (c)2021 Python 101 Version')
print()

show_room(current_room)

while line != 'koniec':
    line = input('> ').strip().lower()

    if line == 'o hre':
        cmd_about()

    elif line == 'prikazy':
        cmd_commands()

    elif line == 'vychod':
        current_room = cmd_east(current_room, world)

    elif line == 'zapad':
        current_room = cmd_west(current_room, world)

    elif line == 'juh':
        current_room = cmd_south(current_room, world)

    elif line == 'sever':
        current_room = cmd_north(current_room, world)

    elif line == 'rozhliadni sa':
        cmd_look_around(current_room)

    elif line == 'inventar':
        cmd_inventory(backpack)

    elif line.startswith('preskumaj'):
        cmd_explore(backpack, current_room, line)

    elif line.startswith('poloz'):
        cmd_drop(backpack, current_room, line)

    elif line.startswith('vezmi'):
        cmd_take(backpack, current_room, line)

    elif line.startswith('pouzi'):
        cmd_use(backpack, current_room, line)

    elif line == 'koniec':
        break

    else:
        print("Tento príkaz nepoznám.")

print('Toto je koniec. Díky, že si si zahral.')
