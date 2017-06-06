format_string = """Title: {tab.title}
Artist: {tab.artist}
Album: {tab.album}
Difficulty: {tab.difficulty}
Capo: {tab.capo}
Rating: {tab.rating}
Type: {tab.type_}

Notes:
{tab.notes}


{tab.text}
"""

def generate(tab):
    return format_string.format(tab=tab)
