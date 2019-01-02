import multiprocessing

# Game Environment
FRAME_GAP = 8 # grame gap for one command

# Fceux
import os
from distutils import spawn
CONFIG_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
#FCEUX_SEARCH_PATH = os.pathsep.join([os.environ['PATH'], '/usr/games', '/usr/local/games'])
#FCEUX_PATH = spawn.find_executable('fceux', FCEUX_SEARCH_PATH)
FCEUX_PATH = 'D:\\fceux-2.2.3-win32\\fceux.exe'
ROM_FILE = os.path.join(CONFIG_FILE_DIR, "SuperMarioBros/super-mario.nes")
PLUGIN_FILE = os.path.join(CONFIG_FILE_DIR, "SuperMarioBros/super-mario-bros.lua")
EMULATOR_LOST_DELAY = 50000 # ms
