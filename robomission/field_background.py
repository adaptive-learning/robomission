from jupyter_react import Component

class FieldBackground(Component):
    module = 'FieldBackground'
    comm_channel = 'react.components'

    def __init__(self, **kwargs):
        super().__init__(target_name='react.components', **kwargs)
        self.on_msg(self._handle_msg)

    def _handle_msg(self, msg):
        print(msg)
