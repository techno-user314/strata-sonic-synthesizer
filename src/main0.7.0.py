"""
This is SoundForge: A digital subtractive synthesiser program
that is semi-polyphonic, and has built-in audio layering.

Copyright (C) 2025  Zach Harwood

This file is part of SoundForge

SoundForge is a free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import sys
import time
import math

from rtmidi.midiutil import open_midiinput
import pyaudio

import constants
from constants import BUFFER_SAMPLES, SAMPLE_RATE, CHANNELS
from constants import MIDI_TO_A4, MAX_CUTOFF
from synthesizer import Synth

"""
MIDI input -> action code
"""
def parse_input(inpt):
    if inpt[0] == 176 and inpt[1] == 1:
        return constants.SET_VOLUME, inpt[1], inpt[2] / 127
    elif inpt[0] == 153 and inpt[1] in [56, 57, 58, 59]:
        return constants.LAYER_SELECT, inpt[1] - 56, inpt[2]
    elif inpt[1] == 7 and inpt[0] in [184, 185, 186, 187]:
        return constants.LAYER_AMP, inpt[0] - 184, inpt[2] / 127
    elif inpt[1] in [18, 19, 20] and inpt[2] == 127:
        return constants.LAYER_REC, inpt[1] - 18, inpt[2]
    elif inpt[1] == 15 and inpt[2] == 127:
        return constants.OSC_TYPE, inpt[1], inpt[2]
    elif inpt[1] in [16, 17] and inpt[2] == 127:
        return constants.OSC_OCTAVE, (inpt[1] - 16) * 2 - 1, inpt[2]
    elif inpt[0] == 153 and inpt[1] in [36, 37, 38, 39]:
        return constants.OSC_MUTE, inpt[1] - 36, inpt[2]
    elif inpt[0] == 153 and inpt[1] in [44, 45, 46, 47]:
        return constants.OSC_SELECT, inpt[1] - 44, inpt[2]
    elif inpt[0] == 176 and inpt[1] in [30, 31, 32, 33]:
        return constants.OSC_AMP, inpt[1] - 30, inpt[2] / 127
    elif inpt[0] == 224 and inpt[2] != 64:
        return constants.OSC_PITCH, -1, int((inpt[2] / 127 - 0.5) * 24)
    elif inpt[0] == 176 and inpt[1] in [34, 35, 36, 37]:
        return constants.OSC_PITCH, inpt[1] - 34, inpt[2]
    elif inpt[0] == 153 and inpt[1] in [49, 50, 51]:
        return constants.MODULATOR_SELECT, inpt[1] - 49, inpt[2]
    elif inpt[0] == 176 and inpt[1] == 7:
        return constants.ENV_ATTACK, inpt[0] - 176, inpt[2] / 127
    elif inpt[0] == 177 and inpt[1] == 7:
        return constants.ENV_DECAY, inpt[0] - 176, inpt[2] / 127
    elif inpt[0] == 178 and inpt[1] == 7:
        return constants.ENV_SUSTAIN, inpt[0] - 176, inpt[2] / 127
    elif inpt[0] == 179 and inpt[1] == 7:
        return constants.ENV_RELEASE, inpt[0] - 176, inpt[2] / 127
    elif inpt[0] == 180 and inpt[1] == 7:
        return constants.LFO_AMP, inpt[0], inpt[2] / 127
    elif inpt[0] == 181 and inpt[1] == 7:
        return constants.LFO_SPEED, inpt[0], inpt[2] * (30 / 127)
    elif inpt[0] == 176 and inpt[1] in [38, 39, 40, 41]:
        return constants.FILTER_FREQ, inpt[1] - 38, (inpt[2] / 127) ** math.e
    elif inpt[0] == 144:
        return constants.ADD_NOTE, inpt[1] - MIDI_TO_A4, inpt[2]
    elif inpt[0] == 128:
        return constants.RM_NOTE, inpt[1], inpt[2]
    elif inpt[2] != 0 and inpt[0] != 137:
        if not (inpt[0] == 224 and inpt[2] == 64):
            print(f"No known action for {inpt}")
            return -1, 0, 0

"""
Audio and MIDI Callback functions
"""
x1 = Synth()

class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        code, value1, value2 = parse_input(message)
        x1.process_input(code, value1, value2)

def audio_callback(in_data, frame_count, time_info, status):
    data = x1.next_buffer()
    return data, pyaudio.paContinue

'''
Main Loop
'''
try:
    midiin, port_name = open_midiinput(1)
    audio = pyaudio.PyAudio()
except (EOFError, KeyboardInterrupt):
    sys.exit()

print("Attaching MIDI input callback handler...")
midiin.set_callback(MidiInputHandler(port_name))

print("Opening streaming device...")
stream = audio.open(format=pyaudio.paInt16,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    output=True,
                    stream_callback=audio_callback,
                    frames_per_buffer=BUFFER_SAMPLES)

print("Entering main loop - ")
try:
    while stream.is_active():
        time.sleep(1)

except Exception as e:
    print(e)

finally:
    # Disengage RtMidi
    midiin.close_port()
    del midiin
    # Disengage PyAudio
    stream.close()
    audio.terminate()
    print("All callbacks disconnected succesfully.")
