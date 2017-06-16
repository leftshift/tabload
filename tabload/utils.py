import importlib
from . import g

def export(tab):
    exporter = importlib.import_module('tabload.formats.' + g.export_format)
    contents = exporter.generate(tab)
    suffix = exporter.suffix
    with open(g.name_scheme.format(tab=tab, suffix=suffix), 'w') as f:
        f.write(contents)
