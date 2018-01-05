from jupyter_react import Component


class SpaceWorld(Component):
    module = 'SpaceWorld'
    comm_channel = 'react.components'

    def __init__(self, **kwargs):
        super().__init__(target_name='react.components', **kwargs)
        self.on_msg(self._handle_msg)

    def set(self, world_description):
        fields = parse_space_world(world_description)
        self.send({'method': 'update', 'props': {'fields':  fields}})

    def _handle_msg(self, msg):
        print(msg)


def parse_space_world(description):
    """Transform text describing a SpaceWorld into a 2D array of fields.
    """
    description = ''.join(description.split())  # remove whitspace
    rows = description.split('||')
    tokenized_rows = [row.strip('|').split('|') for row in rows]
    fields = [[parse_field(field) for field in row] for row in tokenized_rows]
    return fields


def parse_field(field):
    """Transform string describing a field into a tuple (background, objects).

    If no color is given, defaults to black.
    """
    background = 'k'
    objects = []
    for letter in field:
        if letter.islower():
            background = letter
        else:
            objects.append(letter)
    return [background, objects]
