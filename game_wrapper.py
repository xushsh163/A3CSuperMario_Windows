import os
import re
import signal
import tempfile
import subprocess
import multiprocessing
import threading
import time

import numpy as np
import cv2

import config
import win32pipe, win32file, win32api, win32con, win32job, pywintypes, msvcrt

def is_int16(str):
    try:
        int(str, 16)
        return True
    except ValueError:
        return False

class Wrapper:
    ACTION_MAP = [
            [0, 0, 0, 0, 0, 0],  # 0.  NoAction
            [1, 0, 0, 0, 0, 0],  # 1.  Up
            [0, 0, 1, 0, 0, 0],  # 2.  Down
            [0, 1, 0, 0, 0, 0],  # 3.  Left
            [0, 1, 0, 0, 1, 0],  # 4.  Left + A
            [0, 1, 0, 0, 0, 1],  # 5.  Left + B
            [0, 1, 0, 0, 1, 1],  # 6.  Left + A + B
            [0, 0, 0, 1, 0, 0],  # 7.  Right
            [0, 0, 0, 1, 1, 0],  # 8.  Right + A
            [0, 0, 0, 1, 0, 1],  # 9.  Right + B
            [0, 0, 0, 1, 1, 1],  # 10. Right + A + B
            [0, 0, 0, 0, 1, 0],  # 11. A
            [0, 0, 0, 0, 0, 1],  # 12. B
            [0, 0, 0, 0, 1, 1],  # 13. A + B
    ]
    LEVEL_DISTANCE = [
        3266, 3298, 3298, 3698, 3282, 3106, 2962, 6114,
        3266, 3266, 3442, 3266, 3298, 3554, 3266, 3554,
        2514, 3682, 2498, 2434, 2514, 2754, 3682, 3554,
        2430, 2430, 2430, 2942, 2429, 2429, 3453, 4989
    ]
    SCREEN_HEIGHT = 224
    SCREEN_WIDTH = 256
    TILE_HEIGHT = 13
    TILE_WIDTH = 16

    def __init__(self, name, frame_gap, draw_tiles=False):
        self.name = name
        self.frame_gap = frame_gap
        self.draw_tiles = draw_tiles
        self.listener = None
        self.subprocess = None
        self.locker = threading.Lock()
        self.stop_request = False
        self._reset_params()
        self.connected = False

    def _reset_params(self):
        self.score = 0.0
        self.time = 400
        self.level = 0
        self.life = 3
        self.max_distance = 40
        self.prev_distance = 40
        self.not_advance = 0
        self.status = 0
        
        self.last_frame = 0
        self.info = {'distance': 0, 'life': 0, 'score': 0, 'coins': 0, 'time': 0, 'player_status': 0}
        self.over = False
        
        self.screen = np.zeros(shape=(self.SCREEN_HEIGHT, self.SCREEN_WIDTH, 3), dtype=np.uint8)
        if self.draw_tiles:
            self.tiles = np.zeros(shape=(self.TILE_HEIGHT, self.TILE_WIDTH), dtype=np.uint8)

    def init(self):
        self.frame_gap = int(self.frame_gap)
        assert(self.frame_gap > 0)

        tmpdir = tempfile.mkdtemp()
        self.pipe_out_file = '\\\\.\\pipe\\super_mario_out_' + self.name # os.path.join(tmpdir, "out")
        self.pipe_in_file = '\\\\.\\pipe\\super_mario_in_' + self.name # os.path.join(tmpdir, "in")

        self.pipe_out_s = win32pipe.CreateNamedPipe(self.pipe_out_file,
                        win32pipe.PIPE_ACCESS_DUPLEX,
                        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT,
                        1,655360,655360,300,None)

        self.write_fd = msvcrt.open_osfhandle(self.pipe_out_s, os.O_WRONLY)
        self.pipe_out = open(self.write_fd, "w")
        self.pipe_in_s = win32pipe.CreateNamedPipe(self.pipe_in_file, win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT,
            1, 655360, 655360, 300, None)
            
        self.read_fd = msvcrt.open_osfhandle(self.pipe_in_s, os.O_RDONLY)
        self.pipe_in = open(self.read_fd, "r")
        def listen_pipe_in():
            win32pipe.ConnectNamedPipe(self.pipe_in_s, None)
            buffer = ""
            while not self.stop_request:
                #with open(self.read_fd, "r") as reader:
                message = self.pipe_in.readline().rstrip()
                if len(message) > 0:
                    buffer += message
                    if message[-1:-2:-1] == '!':
                        try:
                            parts = buffer[:-1].split('#')
                            header = parts[0] if len(parts) > 0 else ''
                            # print('receive {}'.format(header))
                            data = parts[1] if len(parts) > 1 else ''
                            parts = header.split('_')
                            message_type = parts[0] if len(parts) > 0 else ''
                            frame_number = self._parse_frame_number(parts)
                            if frame_number is None:
                                return

                            if 'info' == message_type:
                                # print(message) 
                                if frame_number > self.last_frame:
                                    self._process_info_data(data)

                            elif 'screen' == message_type:
                                if frame_number > self.last_frame:
                                    self._process_screen_data(data)

                            elif 'tiles' == message_type:
                                if frame_number > self.last_frame:
                                    self._process_tiles_data(data)

                            elif 'ready' == message_type:
                                # print(message)
                                if self.last_frame == 0:
                                    self.last_frame = frame_number
                            elif 'done' == message_type:
                                # print(message)
                                if frame_number > self.last_frame:
                                    self.last_frame = frame_number
                            elif 'reset' == message_type:
                                # print(message)
                                self.last_frame = 0
                                self.screen = np.zeros(shape=(self.SCREEN_HEIGHT, self.SCREEN_WIDTH, 3), dtype=np.uint8)
                                if self.draw_tiles:
                                    self.tiles = np.zeros(shape=(self.TILE_HEIGHT, self.TILE_WIDTH), dtype=np.uint8)
                            elif 'exit' == message_type:
                                self.close()
                            else:
                                print(message)
                        except:
                            pass
                        if 'exit' == buffer[-5:-1]:
                            break
                        buffer = ''
            self.pipe_in.close()
            self.pipe_in = None

        self.listener = threading.Thread(target=listen_pipe_in)
        self.listener.start()

        tmp_file = os.path.join(tmpdir, "plugin.lua")
        with open(tmp_file, "w") as f:
            f.write("pipe_in_file = \"{}\"; pipe_out_file = \"{}\"; target = \"111\"; draw_tiles = {}; frame_gap = {};"
                    "foo = assert (loadfile (\"{}\")); foo ();"
                    .format(self.pipe_in_file.replace('\\','\\\\'), self.pipe_out_file.replace('\\','\\\\'),
                            "true" if self.draw_tiles else "false", self.frame_gap,
                            os.path.abspath(config.PLUGIN_FILE).replace('\\','\\\\'))
                    ) 
        
        

        args = [config.FCEUX_PATH, '--xscale 2', '--yscale 2', '-f 0', "--sound 0", "--nogui 1",
                '-lua', tmp_file, config.ROM_FILE]

        print(' '.join(args))
        self.subprocess = subprocess.Popen(' '.join(args), shell=True, stdout=subprocess.PIPE)

    def close(self):
        self.stop_request = True
        if self.listener is not None:
            self.listener.join(1.0)
            self.listener = None
        
        if self.subprocess is not None:
            try:
                # os.kill(self.fecux_pid, signal.SIGKILL)
                pass 
            except:
                pass
            self.subprocess.kill()
            self.subprocess = None
        if self.pipe_out is not None:
            self.pipe_out.close()
        if self.pipe_in is not None:
            self.pipe_in.close()
        self.over = True
        self.stop_request = False

    def reset(self):
        self._reset_params()

    def set_level(self, level):
        self.reset()
        self.level = level
        self.notify('changelevel#' + str(self.level))

    def step(self, action):
        wait = 0
        while 0 == self.last_frame:
            wait += 1
            time.sleep(0.001)
            if wait > config.EMULATOR_LOST_DELAY:
                print("{}: Launch Failed after waiting {}".format(self.name, wait))
                #self.close()
                #time.sleep(1)
                #self.init()
                #self.set_level(self.level)
                #time.sleep(3)
                raise ValueError("Failed to communiate with emulator")

        current_frame = self.last_frame

        self.notify('commands_%d#%s' % (current_frame, ','.join([str(i) for i in action])))
        # print("current", current_frame)

        wait = 0
        while self.last_frame <= current_frame:
            wait += 1
            time.sleep(0.001)
            if wait > config.EMULATOR_LOST_DELAY:
                print("{}: Unrespond after waiting {} at frame {}".format(self.name, wait, current_frame))
                self.close()
                #time.sleep(1)
                #self.init()
                #self.set_level(self.level)
                #return self.step(action)
                raise ValueError("Failed to receive responds from emulator")

        delta_dist = self.info["distance"] - self.prev_distance
        if delta_dist > 0 or delta_dist < -100:
            self.not_advance = 0
        else:
            self.not_advance += 1

        if self.over: # or self.not_advance > 250:
            over = True
        else:
            over = False

        if over:
            if self.info["distance"] > 0.97 * self.LEVEL_DISTANCE[self.level]:
                reward = 1    # 1
                self.level += 1
            else:
                reward = -1 # -2
        else:
            if delta_dist < -100:               # enter secret regions
                reward = 0.75
            elif delta_dist > 100:              # leave secret regions
                reward = 0.75
            else:
                if self.info['distance'] - self.max_distance > 0:
                    reward = 0.055 * (self.info['distance'] - self.max_distance)
                elif self.info['distance'] - self.prev_distance < 0:
                    reward = 0.025 * (self.info['distance'] - self.prev_distance)
                else:
                    reward = 0
                reward /= self.frame_gap  # should at most move 1.75 per frame
            
            # 1000 for status improvement, 200 for coins, 100 for monsters, 50 for bricks
            reward += min(0.5, 0.001 * (self.info["score"] - self.score))
            # reward += 0.1 * (self.info["time"] - self.time)
            reward += min((self.info["player_status"] - self.status), 0)
            reward += self.info["life"] - self.life

        self.score = self.info["score"]
        self.time = self.info["time"]
        self.max_distance = max(self.max_distance, self.info["distance"])
        self.prev_distance = self.info["distance"]
        self.status = self.info["player_status"]
        self.life = self.info["life"]

        return self.screen.copy(), reward, over, self.info

    def _process_info_data(self, data):
        parts = data.split('|')
        for part in parts:
            if part.find(':') == -1:
                continue
            parts_2 = part.split(':')
            name = parts_2[0]
            value = int(parts_2[1])
            if 'over' == name:
                self.over = bool(value)
            else:
                self.info[name] = value

    def _process_screen_data(self, data):
        parts = data.split('|')
        for part in parts:
            if 6 == len(part) and is_int16(part[0:2]) and is_int16(part[2:4]):
                x = int(part[0:2], 16)
                y = int(part[2:4], 16)
                self.screen[y][x] = self._hex2rgb(part[4:6])


    def _process_tiles_message(self, frame_number, data):
        parts = data.split('|')
        for part in parts:
            if 3 == len(part) and is_int16(part[0:1]) and is_int16(part[1:2]) and is_int16(part[2:3]):
                x = int(part[0:1], 16)
                y = int(part[1:2], 16)
                v = int(part[2:3], 16)
                self.tiles[y][x] = v
                if v == 0: self.screen[y][x] = self._hex2rgb('0D')
                if v == 1: self.screen[y][x] = self._hex2rgb('30')
                if v == 2: self.screen[y][x] = self._hex2rgb('27')
                if v == 3: self.screen[y][x] = self._hex2rgb('05')

    def _parse_frame_number(self, parts):
        # Parsing frame number
        try:
            frame_number = int(parts[1]) if len(parts) > 1 else 0
            return frame_number
        except:
            pass
        # Sometimes beginning of message is sent twice (screen_70screen_707#)
        if len(parts) > 2 and parts[2].isdigit():
            tentative_frame = int(parts[2])
            if self.last_frame - 10 < tentative_frame < self.last_frame + 10:
                return tentative_frame
        # Otherwise trying to make sense of digits
        else:
            digits = ''.join(c for c in ''.join(parts[1:]) if c.isdigit())
            tentative_frame = int(digits) if len(digits) > 1 else 0
            if self.last_frame - 10 < tentative_frame < self.last_frame + 10:
                return tentative_frame
        # Unable to parse - Likely an invalid message
        return None

    def _hex2rgb(self, palette):
        rgb = {
            '00': (116, 116, 116),
            '01': (36, 24, 140),
            '02': (0, 0, 168),
            '03': (68, 0, 156),
            '04': (140, 0, 116),
            '05': (168, 0, 16),
            '06': (164, 0, 0),
            '07': (124, 8, 0),
            '08': (64, 44, 0),
            '09': (0, 68, 0),
            '0A': (0, 80, 0),
            '0B': (0, 60, 20),
            '0C': (24, 60, 92),
            '0D': (0, 0, 0),
            '0E': (0, 0, 0),
            '0F': (0, 0, 0),
            '10': (188, 188, 188),
            '11': (0, 112, 236),
            '12': (32, 56, 236),
            '13': (128, 0, 240),
            '14': (188, 0, 188),
            '15': (228, 0, 88),
            '16': (216, 40, 0),
            '17': (200, 76, 12),
            '18': (136, 112, 0),
            '19': (0, 148, 0),
            '1A': (0, 168, 0),
            '1B': (0, 144, 56),
            '1C': (0, 128, 136),
            '1D': (0, 0, 0),
            '1E': (0, 0, 0),
            '1F': (0, 0, 0),
            '20': (252, 252, 252),
            '21': (60, 188, 252),
            '22': (92, 148, 252),
            '23': (204, 136, 252),
            '24': (244, 120, 252),
            '25': (252, 116, 180),
            '26': (252, 116, 96),
            '27': (252, 152, 56),
            '28': (240, 188, 60),
            '29': (128, 208, 16),
            '2A': (76, 220, 72),
            '2B': (88, 248, 152),
            '2C': (0, 232, 216),
            '2D': (120, 120, 120),
            '2E': (0, 0, 0),
            '2F': (0, 0, 0),
            '30': (252, 252, 252),
            '31': (168, 228, 252),
            '32': (196, 212, 252),
            '33': (212, 200, 252),
            '34': (252, 196, 252),
            '35': (252, 196, 216),
            '36': (252, 188, 176),
            '37': (252, 216, 168),
            '38': (252, 228, 160),
            '39': (224, 252, 160),
            '3A': (168, 240, 188),
            '3B': (176, 252, 204),
            '3C': (156, 252, 240),
            '3D': (196, 196, 196),
            '3E': (0, 0, 0),
            '3F': (0, 0, 0),
            '40': (87, 87, 87),
            '41': (27, 18, 105),
            '42': (0, 0, 126),
            '43': (51, 0, 117),
            '44': (105, 0, 87),
            '45': (126, 0, 12),
            '46': (123, 0, 0),
            '47': (93, 6, 0),
            '48': (48, 33, 0),
            '49': (0, 51, 0),
            '4A': (0, 60, 0),
            '4B': (0, 45, 15),
            '4C': (18, 45, 69),
            '4D': (0, 0, 0),
            '4E': (0, 0, 0),
            '4F': (0, 0, 0),
            '50': (141, 141, 141),
            '51': (0, 84, 177),
            '52': (24, 42, 177),
            '53': (96, 0, 180),
            '54': (141, 0, 141),
            '55': (171, 0, 66),
            '56': (162, 30, 0),
            '57': (150, 57, 9),
            '58': (102, 84, 0),
            '59': (0, 111, 0),
            '5A': (0, 126, 0),
            '5B': (0, 108, 42),
            '5C': (0, 96, 102),
            '5D': (0, 0, 0),
            '5E': (0, 0, 0),
            '5F': (0, 0, 0),
            '60': (189, 189, 189),
            '61': (45, 141, 189),
            '62': (69, 111, 189),
            '63': (153, 102, 189),
            '64': (183, 90, 189),
            '65': (189, 87, 135),
            '66': (189, 87, 72),
            '67': (189, 114, 42),
            '68': (180, 141, 45),
            '69': (96, 156, 12),
            '6A': (57, 165, 54),
            '6B': (66, 186, 114),
            '6C': (0, 174, 162),
            '6D': (90, 90, 90),
            '6E': (0, 0, 0),
            '6F': (0, 0, 0),
            '70': (189, 189, 189),
            '71': (126, 171, 189),
            '72': (147, 159, 189),
            '73': (159, 150, 189),
            '74': (189, 147, 189),
            '75': (189, 147, 162),
            '76': (189, 141, 132),
            '77': (189, 162, 126),
            '78': (189, 171, 120),
            '79': (168, 189, 120),
            '7A': (126, 180, 141),
            '7B': (132, 189, 153),
            '7C': (117, 189, 180),
            '7D': (147, 147, 147),
            '7E': (0, 0, 0),
            '7F': (0, 0, 0),
        }
        if palette.upper() in rgb:
            return rgb[palette.upper()]
        else:
            return 0, 0, 0

    def notify(self, message):
        if not self.connected:
            win32pipe.ConnectNamedPipe(self.pipe_out_s, None)
            self.connected = True
        with self.locker:       
            # get a file descriptor to write to     
            self.pipe_out.write(message + '\n')
            self.pipe_out.flush()
            # print('send {}'.format(message))

if __name__=='__main__':
    import random
    game = Wrapper('worker_0', config.FRAME_GAP)
    game.init()
    game.set_level(0)
    over = False
    while(not over):
        frame, reward, over, info = game.step(game.ACTION_MAP[random.randrange(len(game.ACTION_MAP))])
        #time.sleep(0.2)