from .field_background import FieldBackground

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'visualization',
        'require': 'visualization/index'
    }]
