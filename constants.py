"""
All the program-wide constants are stored here.
Note that SAMPLE_RATE and BUFFER_SAMPELS are hardcoded
in DSPcmath.pyx.

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
along with this program.  If not, see <https://www.gnu.org/licenses/
"""

BUFFER_SAMPLES = 256 # Number of samples in audio buffer
SAMPLE_RATE = 44100
CHANNELS = 1

MIDI_TO_A4 = 57  # MIDI input that corrosponds to the A4 note
MAX_CUTOFF = 10000  # Maximum LFO cutoff frequancy
MAX_RECORDING = 5000 # Maximum number of input each layer is allowed to record

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