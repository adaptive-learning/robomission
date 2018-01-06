from jupyter_react import Component


class SpaceGame(Component):
    module = 'SpaceGame'
    comm_channel = 'react.components'

    def __init__(self, **kwargs):
        super().__init__(target_name='react.components', **kwargs)
        self.on_msg(self._handle_msg)

    def set(self, world_description):
        # TODO: Hoist the component to SpaceGameContainer withing the redux app
        raise NotImplementedError('SpaceGame.set is not yet implemented.')
        #fields = parse_space_world(world_description)
        #self.send({'method': 'update', 'props': {'fields':  fields}})

    def _handle_msg(self, msg):
        print(msg)
