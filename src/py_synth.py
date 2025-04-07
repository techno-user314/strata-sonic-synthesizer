"""
Python/ctypes decleration of C structs used in synthesis.c and control.c.

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
import ctypes

class Envelope(ctypes.Structure):
    _fields_ = [("releasing", ctypes.c_int),
                ("sustain_value", ctypes.POINTER(ctypes.c_float)),
                ("attack_ms", ctypes.POINTER(ctypes.c_int)),
                ("decay_ms", ctypes.POINTER(ctypes.c_int)),
                ("sustain_percent", ctypes.POINTER(ctypes.c_float)),
                ("release_ms", ctypes.POINTER(ctypes.c_int))]

class LFO(ctypes.Structure):
    _fields_ = [("lfoAt", ctypes.c_double),
                ("speed_hz", ctypes.POINTER(ctypes.c_int)),
                ("amp", ctypes.POINTER(ctypes.c_double)),
                ("percent_effect", ctypes.POINTER(ctypes.c_double))]

class LPF(ctypes.Structure):
    _fields_ = [("in_history", (ctypes.c_double * 3)),
                ("out_history", (ctypes.c_double * 3))]

class Osc(ctypes.Structure):
    _fields_ = [("type", ctypes.c_int),
                ("oscAt", ctypes.c_double),
                ("note", ctypes.c_int),
                ("shift", ctypes.POINTER(ctypes.c_float))]


class Note(ctypes.Structure):
    _fields_ = [("note", ctypes.c_int),
                ("ampEnv", ctypes.POINTER(Envelope)),
                ("ampLFO", ctypes.POINTER(LFO)),
                ("pitchEnv", ctypes.POINTER(Envelope)),
                ("pitchLFO", ctypes.POINTER(LFO)),
                ("lpfilter", ctypes.POINTER(LPF)),
                ("filterEnv", ctypes.POINTER(Envelope)),
                ("osc", ctypes.POINTER(Osc)),
                ("releasing", ctypes.c_int),
                ("isdone", ctypes.c_int)]

class Oscillator(ctypes.Structure):
    _fields_ = [("noteCount", ctypes.c_int),
                ("notes", (ctypes.POINTER(Note) * 25)),
                ("releasingNotes", (ctypes.POINTER(Note) * 25)),
                ("input_map", (ctypes.c_int * 25)),
                ("oscType", ctypes.c_int),
                ("selectedMod", ctypes.c_int),
                ("amp", ctypes.c_float),
                ("ampEnv", ctypes.POINTER(Envelope)),
                ("ampLFO", ctypes.POINTER(LFO)),
                ("pitchOctave", ctypes.c_int),
                ("pitchSteps", ctypes.c_int),
                ("pitchCents", ctypes.c_float),
                ("pitch", ctypes.c_float),
                ("pitchEnv", ctypes.POINTER(Envelope)),
                ("pitchLFO", ctypes.POINTER(LFO)),
                ("filter", ctypes.c_float),
                ("filterEnv", ctypes.POINTER(LPF))]

class Page(ctypes.Structure):
    _fields_ = [("amp", ctypes.c_float),
                ("oscs", (ctypes.POINTER(Oscillator) * 4)),
                ("unmuted", (ctypes.c_int * 4)),
                ("selectedOsc", ctypes.c_int)]

class Synth(ctypes.Structure):
    _fields_ = [("layers", (ctypes.POINTER(Page) * 4)),
                ("selectedLayer", ctypes.c_int),
                ("amp", ctypes.c_float)]
