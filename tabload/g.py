"""Manages some global settings and variables"""
import re

# Matches chords.
# Group 1: The whole chord (like "Bbm7")
# Group 2: Just the base note (Like "Bb")
r_chord = re.compile("\s(([ABCDEFG](?:#{1,2}|b{1,2}))?[1-9]?(?:M|maj|major|m|min|minor|dim|sus|dom|aug|\+|-|add)?[1-9]?)\s")

export_format = "text"
instruments = ['guitar', 'ukulele', 'bass']
services = ["ukutabs", "ultimate_guitar"]

name_scheme = "{tab.artist} – {tab.title}.{suffix}"
out_dir = "./out"
