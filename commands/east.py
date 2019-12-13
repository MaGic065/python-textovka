from commands.command import Command


class East(Command):
    def __init__(self):
        super().__init__('vychod', 'Presunie sa do miestnosti na východ.')

    def exec(self, context):
        if 'east' in context.current_room._exits:
            context.current_room = context.current_room._exits['east']
            print(context.current_room)
        else:
            print('tam sa neda ist.')