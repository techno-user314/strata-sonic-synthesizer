"""
This file handles converting MIDI input codes into program universal contants
for control of the synth. The 'inpt' parameter is a MIDI code, e.g. [7, 15, 127].

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

from math import e

MIDI_TO_A4 = 57

# Action codes. These should be the same as the ones in constants.h
SET_VOLUME = 1
ADD_NOTE = 2
RM_NOTE = 3
LAYER_SELECT = 4
LAYER_AMP = 5
LAYER_REC = 6
OSC_SELECT = 7
OSC_MUTE = 8
OSC_AMP = 9
OSC_TYPE = 10
OSC_OCTAVE = 11
OSC_PITCH = 12
ENV_ATTACK = 13
ENV_DECAY = 14
ENV_SUSTAIN = 15
ENV_RELEASE = 16
LFO_SPEED = 17
LFO_AMP = 18
FILTER_TYPE = 19
FILTER_FREQ = 20
FILTER_AMP = 21
FILTER_PARAM = 22
MODULATOR_SELECT = 23

# Function to turn raw MIDI codes into action codes
def parse_input(inpt):
    if inpt[0] == 176 and inpt[1] == 1:
        return SET_VOLUME, inpt[1], inpt[2] / 127
    elif inpt[0] == 153 and inpt[1] in [40, 41, 42, 43]:
        return LAYER_SELECT, inpt[1] - 56, inpt[2]
    elif inpt[1] == 7 and inpt[0] in [184, 185, 186, 187]:
        return LAYER_AMP, inpt[0] - 184, inpt[2] / 127
    elif inpt[1] in [18, 19, 20] and inpt[2] == 127:
        return LAYER_REC, inpt[1] - 18, inpt[2]
    elif inpt[1] == 15 and inpt[2] == 127:
        return OSC_TYPE, inpt[1], inpt[2]
    elif inpt[1] in [16, 17] and inpt[2] == 127:
        return OSC_OCTAVE, (inpt[1] - 16) * 2 - 1, inpt[2]
    elif inpt[0] == 153 and inpt[1] in [36, 37, 38, 39]:
        return OSC_MUTE, inpt[1] - 36, inpt[2]
    elif inpt[0] == 153 and inpt[1] in [44, 45, 46, 47]:
        return OSC_SELECT, inpt[1] - 44, inpt[2]
    elif inpt[0] == 176 and inpt[1] in [30, 31, 32, 33]:
        return OSC_AMP, inpt[1] - 30, inpt[2] / 127
    elif inpt[0] == 224 and inpt[2] != 64:
        return OSC_PITCH, -1, int((inpt[2] / 127 - 0.5) * 24)
    elif inpt[0] == 176 and inpt[1] in [34, 35, 36, 37]:
        return OSC_PITCH, inpt[1] - 34, inpt[2]
    elif inpt[0] == 153 and inpt[1] in [49, 50, 51]:
        return MODULATOR_SELECT, inpt[1] - 49, inpt[2]
    elif inpt[0] == 176 and inpt[1] == 7:
        return ENV_ATTACK, inpt[0] - 176, inpt[2] / 127
    elif inpt[0] == 177 and inpt[1] == 7:
        return ENV_DECAY, inpt[0] - 176, inpt[2] / 127
    elif inpt[0] == 178 and inpt[1] == 7:
        return ENV_SUSTAIN, inpt[0] - 176, inpt[2] / 127
    elif inpt[0] == 179 and inpt[1] == 7:
        return ENV_RELEASE, inpt[0] - 176, inpt[2] / 127
    elif inpt[0] == 180 and inpt[1] == 7:
        return LFO_AMP, inpt[0], inpt[2] / 127
    elif inpt[0] == 181 and inpt[1] == 7:
        return LFO_SPEED, inpt[0], inpt[2] * (30 / 127)
    elif inpt[0] == 176 and inpt[1] in [38, 39, 40, 41]:
        return FILTER_FREQ, inpt[1] - 38, (inpt[2] / 127) ** e
    elif inpt[0] == 144:
        return ADD_NOTE, inpt[1] - MIDI_TO_A4, inpt[2]
    elif inpt[0] == 128:
        return RM_NOTE, inpt[1], inpt[2]
    elif inpt[2] != 0 and inpt[0] != 137:
        if not (inpt[0] == 224 and inpt[2] == 64):
            #print(f"No known action for {inpt}")
            return -1, 0, 0
