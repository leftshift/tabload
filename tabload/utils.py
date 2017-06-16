import os
import importlib
from . import g


def export(tab):
    out_dir = os.path.expanduser(g.out_dir)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    exporter = importlib.import_module('tabload.formats.' + g.export_format)
    contents = exporter.generate(tab)
    suffix = exporter.suffix
    path = os.path.join(out_dir, g.name_scheme.format(tab=tab, suffix=suffix))
    with open(path, 'w') as f:
        f.write(contents)
