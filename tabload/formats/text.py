suffix = "txt"
format_string = """Title: {tab.title}
Artist: {tab.artist}
Album: {tab.album}
Difficulty: {tab.difficulty}
Capo: {tab.capo}
Rating: {tab.rating}
Type: {tab.type_}
Url: {tab.url}

Notes:
{tab.notes}

Chords:
{chords}


{tab.text}
"""


def generate(tab, strings=None, chords=None, diff_dict=None):
    diagrams = []
    ch_string = ""
    if strings and chords:
        import chordata
        for chord in chords:
            diagrams.append(chord[0].center(20))
            diagrams.append(chordata.utils.render(chord[1], strings))
        ch_string = '\n'.join(diagrams)

    return format_string.format(tab=tab, chords=ch_string)
