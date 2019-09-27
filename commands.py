from exceptions import ItemNotFound, BackpackMaxCapacityReached
from game_context import GameContext
from items.mixins import Movable, Usable


def show_room(room: dict):
    # show description
    print(room['description'])

    # show exits
    if len(room['exits']) > 0:
        print('Možné východy:')
        for exit in room['exits']:
            print(f"    {exit}")
    else:
        print('Z miestnosti nevedú žiadne východy.')

    # show items
    if len(room['items']) > 0:
        print('Vidíš:')
        for item in room['items']:
            print(f'     {item._name}')
    else:
        print('Nevidíš nič zvláštne.')


class Command:
    def __init__(self, name, description):
        self._name = name
        self._description = description
        self._params = None

    def set_params(self, params):
        self._params = params

    def exec(self, context: GameContext):
        pass

    def __str__(self):
        return f'{self._name} - {self._description}'


class About(Command):
    def __init__(self):
        super().__init__('o hre', 'Túto hru spáchal mirek v roku 2019. Celkom fajnú.')

    def exec(self, context):
        print(self._description)


class LookAround(Command):
    def __init__(self):
        super().__init__('rozhliadni sa', 'Vypíše opis miestnosti.')

    def exec(self, context):
        show_room(context.world[context.current_room])


class Inventory(Command):
    def __init__(self):
        super().__init__('inventar', 'Zobrazí obsah batohu.')

    def exec(self, context):
        items = context.backpack.get_items()
        if len(items) > 0:
            print('V batohu máš:')
            for item in items:
                print(f'     {item}')
        else:
            print('Batoh je prázdny.')


class Help(Command):
    def __init__(self, commands):
        super().__init__('pomoc', 'Zobrazí pomocníka k jednotlivým príkazom')
        self._commands = commands

    def exec(self, context):
        if len(self._params) == 0:
            print('O akom príkaze sa chceš dozvedieť viac?')
            return

        for command in self._commands:
            if command._name == self._params:
                print(command)
                break
        else:
            print('Neznámy príkaz.')


class Commands(Command):
    def __init__(self, commands):
        super().__init__('prikazy', 'Zobrazí zoznam príkazov.')
        self._commands = commands

    def exec(self, context):
        print('Dostupné príkazy:')
        for command in self._commands:
            print(f'    {command._name}')


class Quit(Command):
    def __init__(self):
        super().__init__('koniec', 'Ukončí hru.')

    def exec(self, context):
        print('ta diky ze si si zahral tuto mocnu hru, lebo je fakt mocna.')
        context.state = 'quit'


class East(Command):
    def __init__(self):
        super().__init__("vychod", "Presunie sa na vychod.")

    def exec(self, context):
        """
        Enter the room on east from current room.
        If there is no exit to the east, then no change. The new room will be returned from the function.
        :param world: the world the player is in
        :param current_room: the name of current room player is in
        :return: the name of new room on the east
        """
        room = context.world[context.current_room]

        if 'vychod' in room['exits']:
            context.current_room = room['exits']['vychod']
            show_room(context.world[context.current_room])
        else:
            print('tam sa neda ist')


class West(Command):
    def __init__(self):
        super().__init__("zapad", "Presunie sa na západ.")

    def exec(self, context):
        room = context.world[context.current_room]

        if 'zapad' in room['exits']:
            context.current_room = room['exits']['zapad']
            show_room(context.world[context.current_room])
        else:
            print('tam sa neda ist')


class North(Command):
    def __init__(self):
        super().__init__("sever", "Presunie sa na sever.")

    def exec(self, context):
        room = context.world[context.current_room]

        if 'sever' in room['exits']:
            context.current_room = room['exits']['sever']
            show_room(context.world[context.current_room])
        else:
            print('tam sa neda ist')


class South(Command):
    def __init__(self):
        super().__init__("juh", "Presunie sa na juh.")

    def exec(self, context):
        room = context.world[context.current_room]

        if 'juh' in room['exits']:
            context.current_room = room['exits']['juh']
            show_room(context.world[context.current_room])
        else:
            print('tam sa neda ist')


class Down(Command):
    def __init__(self):
        super().__init__("dolu", "Presunie sa dolu.")

    def exec(self, context):
        room = context.world[context.current_room]

        if 'dolu' in room['exits']:
            context.current_room = room['exits']['dolu']
            show_room(context.world[context.current_room])
        else:
            print('tam sa neda ist')


class DropItem(Command):
    def __init__(self):
        super().__init__("poloz", "Položí predmet v miestnosti.")

    def exec(self, context):
        try:
            item = context.backpack.remove(self._params)
            room = context.get_current_room()
            room['items'].append(item)
            print(f'{item._name} si vyložil z batohu.')

        except ItemNotFound as ex:
            print('Taký predmet u seba nemáš.')

        except BaseException as ex:
            print('Dajaka neznama chyba sa stala')
            print(ex)


class TakeItem(Command):
    def __init__(self):
        super().__init__("vezmi", "Vezme predmet z miestnosti.")

    def exec(self, context:GameContext):
        room = context.get_current_room()
        for item in room['items']:
            if item._name == self._params:
                if not isinstance(item, Movable):
                    print('Tento predmet sa nedá vziať.')
                else:
                    try:
                        context.backpack.add(item)
                        room['items'].remove(item)
                        print(f'{item._name} si vložil do batohu.')

                    except BackpackMaxCapacityReached:
                        print('Batoh je plný.')

                    except BaseException as ex:
                        print("Dačo nedobre")
                        print(ex)

                break  # return
        else:
            print('Taký predmet tu nikde nevidím.')


class ExamineItem(Command):
    def __init__(self):
        super().__init__("preskumaj", "Preskúma zvolený predmet.")

    def exec(self, context):
        room = context.get_current_room()
        items = room['items'] + context.backpack

        for item in items:
            if item._name == self._params:
                print(item._description)
                return

        print('Taký predmet tu nikde nevidím.')


class UseItem(Command):
    def __init__(self):
        super().__init__("pouzi", "Použije zvolený predmet.")

    def exec(self, context):
        room = context.world[context.current_room]
        items = room['items'] + context.backpack

        for item in items:
            if item._name == self._params:
                if not isinstance(item, Usable):
                    print('Tento predmet sa nedá použiť')
                    return

                item.use(context)
                return

        print('Taký predmet tu nikde nevidím.')
