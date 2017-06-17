import os
import importlib
from . import g

notes = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']

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


def transposer(semitones):
    """Returns a function for re.sub() that transposes all chord matches by
    the given number of semitones."""
    def f(match):
        note = match.group(3)
        prev_note = notes.index(note)
        new_note = notes[(prev_note+12+semitones) % 12]
        return match.expand(r"\1" + new_note + r"\4\5")

    return f
