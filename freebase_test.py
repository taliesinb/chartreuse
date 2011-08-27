
from compiler import *
from chart import *
from rules import *
from patterns import *
from utils import *
from freebase import *

batman = movie("/en/batman_1989")
batman_begins = movie("/en/batman_begins")

print batman.directors()
print batman.actors_in_common(batman_begins)
print batman.characters_in_common(batman_begins)
print batman.actors()

kevin_bacon = actor("/en/kevin_bacon")
matt_dillon = actor("/en/matt_dillon")

print kevin_bacon.nth_movie(5)
print kevin_bacon.movies_in_common(matt_dillon)