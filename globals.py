import sys
import os

from temps import make_castle_temps

# unfrozen
development_mode = True
root = os.path.dirname(os.path.realpath(__file__))
temps_folder = make_castle_temps()

if getattr(sys, 'frozen', False):
    # frozen
    root = os.path.realpath(os.path.dirname(sys.executable))
    development_mode = False
