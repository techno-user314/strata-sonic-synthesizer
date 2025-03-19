"""
This file contains all the classes that handle control of
taking the input, and turning it into an audible note.

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
import math
import struct

import constants
from constants import BUFFER_SAMPLES, SAMPLE_RATE
from constants import MIDI_TO_A4, MAX_CUTOFF
from DSPcmath import sine_osc, square_osc, sawtooth_osc, triangle_osc
from DSPcmath import envelope, lfosc, lpfilter
from recording import InputRecorder

OSC_TYPES = [sine_osc, sawtooth_osc, triangle_osc, square_osc]

class Note:
    def __init__(self, parent_osc, oscillator, note):
        self.parent = parent_osc
        self.note = note

        self.envsAt = 0
        self.alfoAt = 0
        self.plfoAt = 0
        self.lpfState = [[0, 0], [0, 0]]

        self.osc = oscillator
        self.oscAt = 0

        self.releasing = False
        self.isdone = False

    def start_release(self):
        self.releasing = True
        self.envsAt = 0

    def done(self):
        return self.isdone

    def next_buffer(self):
        attack, decay, sustain, release = self.parent.ampEnv
        amp_env = envelope(self.envsAt, self.parent.amp, self.releasing,
                           attack, decay, sustain, release)
        attack, decay, sustain, release = self.parent.pitchEnv
        pitch_env = envelope(self.envsAt, 1, self.releasing,
                             attack, decay, sustain, release)
        attack, decay, sustain, release = self.parent.filterEnv
        filter_env = envelope(self.envsAt, (MAX_CUTOFF - self.parent.filter),
                              self.releasing, attack, decay, 1, release)
        filter_env = [MAX_CUTOFF - delta_cutoff for delta_cutoff in filter_env]

        speed_hz, amp = self.parent.ampLFO
        amp_lfo, at1 = lfosc(self.alfoAt, speed_hz, amp, 1)
        speed_hz, amp = self.parent.pitchLFO
        pitch_lfo, at2 = lfosc(self.plfoAt, speed_hz, amp, 1)

        amp_vals = [x * y for x, y in zip(amp_env, amp_lfo)]
        pitch_vals = [x * y for x, y in zip(pitch_env, pitch_lfo)]

        samples, at0 = self.osc(self.oscAt, self.note, self.parent.pitch,
                                amp_vals, pitch_vals)
        self.oscAt = at0
        self.envsAt += BUFFER_SAMPLES
        self.alfoAt = at1
        self.plfoAt = at2

        if self.releasing and amp_env[-1] == 0:
            self.isdone = True

        final, self.lpfState[0], self.lpfState[1] = lpfilter(
            samples, filter_env,
            self.lpfState[0], self.lpfState[1])
        return final


class Oscillator:
    def __init__(self):
        self.noteCount = 0
        self.notes = [None for _ in range(25)]
        self.releasingNotes = []
        self.input_map = {}

        self.selectedOsc = 0
        self.selectedMod = 0

        self.amp = 1
        self.ampEnv = [0, 0, 1, 0]
        self.ampLFO = [0, 0]

        self.pitchOctave = 0
        self.pitchSteps = 0
        self.pitchCents = 0
        self.pitch = 0
        self.pitchEnv = [0, 0, 1, 0]
        self.pitchLFO = [0, 0]

        self.filter = MAX_CUTOFF  # Filter cutoff frequancy
        self.filterEnv = [0, 0, 1, 0]

    def clear_notes(self):
        self.noteCount = 0
        self.notes = [None for _ in range(25)]
        self.releasingNotes = []
        self.input_map = {}

    def _add_note(self, note):
        for pos in range(len(self.notes)):
            if self.notes[pos] is None:
                self.notes[pos] = Note(self, OSC_TYPES[self.selectedOsc], note)
                self.noteCount += 1
                n = note + MIDI_TO_A4
                self.input_map.update({n: pos})
                break

    def _rm_note(self, in_note):
        note_index = self.input_map.pop(in_note, None)
        if note_index is not None:
            self.notes[note_index].start_release()
            self.releasingNotes.append(self.notes[note_index])
            self.notes[note_index] = None

    def modify_envelope(self, parameter, new_value):
        to_modify = parameter - constants.ENV_ATTACK
        set_to = new_value
        if to_modify != 2:
            # Input: 0-1, equation gives 0-4077 ms, curved exponentially
            set_to = (math.e ** (new_value * 2.85) - 1) / 2 * 500
        match self.selectedMod:
            case 0: self.ampEnv[to_modify] = set_to
            case 1: self.pitchEnv[to_modify] = set_to
            case 2: self.filterEnv[to_modify] = set_to

    def modify_lfo(self, parameter, new_value):
        to_modify = parameter - constants.LFO_SPEED
        match self.selectedMod:
            case 0: self.ampLFO[to_modify] = new_value
            case 1: self.pitchLFO[to_modify] = new_value
            case 2: pass

    def process_input(self, action, button, value):
        match action:
            case constants.ADD_NOTE:
                self._add_note(button)
            case constants.RM_NOTE:
                self._rm_note(button)
            case constants.OSC_TYPE:
                self.selectedOsc += 1
                self.selectedOsc = self.selectedOsc % len(OSC_TYPES)
            case constants.OSC_AMP:
                self.amp = value
            case constants.OSC_OCTAVE:
                self.pitchOctave += button * 12
                self.pitch = self.pitchOctave
                self.pitch += self.pitchSteps + self.pitchCents
            case constants.OSC_PITCH:
                if button == -1:
                    self.pitchSteps = value
                else:
                    self.pitchCents = value / 100
                self.pitch = self.pitchOctave
                self.pitch += self.pitchSteps + self.pitchCents
            case constants.MODULATOR_SELECT:
                self.selectedMod = button
            case constants.ENV_ATTACK:
                self.modify_envelope(constants.ENV_ATTACK, value)
            case constants.ENV_DECAY:
                self.modify_envelope(constants.ENV_DECAY, value)
            case constants.ENV_SUSTAIN:
                self.modify_envelope(constants.ENV_SUSTAIN, value)
            case constants.ENV_RELEASE:
                self.modify_envelope(constants.ENV_RELEASE, value)
            case constants.LFO_SPEED:
                self.modify_lfo(constants.LFO_SPEED, value)
            case constants.LFO_AMP:
                self.modify_lfo(constants.LFO_AMP, value)
            case constants.FILTER_FREQ:
                self.filter = value * (MAX_CUTOFF - 100) + 100

    def next_buffer(self):
        for i in range(len(self.releasingNotes)):
            if self.releasingNotes[i].done():
                self.releasingNotes[i] = None
                self.noteCount -= 1
        self.releasingNotes = [n for n in self.releasingNotes
                               if n is not None]

        if self.noteCount == 0 or self.ampEnv[2] == 0:
            return [0 for _ in range(BUFFER_SAMPLES)]

        buffers = []
        for note in self.notes:
            if note is not None:
                buffers.append(note.next_buffer())
        for note in self.releasingNotes:
            buffers.append(note.next_buffer())

        note_max_amp = 1 / self.ampEnv[2]  # 1 / sustain
        note_weight = 1 / (max(self.noteCount, 4) * note_max_amp)

        all_buffers = zip(*buffers)
        sum_buffers = [sum(buffer) * note_weight for buffer in all_buffers]

        return sum_buffers


class Page:
    def __init__(self):
        self.amp = 1
        self.oscs = [Oscillator(), Oscillator(),
                     Oscillator(), Oscillator()]
        self.unmuted = [1 for _ in range(len(self.oscs))]
        self.selectedOsc = 0

        self.resetCount = 0

        self.recorder = InputRecorder()
        self.recording = False

    def process_input(self, action, button, value):
        if not (action == constants.LAYER_REC and button == 0):
            self.resetCount = 0
        match action:
            case constants.ADD_NOTE:
                if self.recording:
                    self.recorder.record([action, button, value])
                for osc, unmuted in zip(self.oscs, self.unmuted):
                    if unmuted:
                        osc.process_input(action, button, value)
            case constants.RM_NOTE:
                if self.recording:
                    self.recorder.record([action, button, value])
                for osc in self.oscs:
                    osc.process_input(action, button, value)
            case constants.LAYER_AMP:
                self.amp = value
            case constants.LAYER_REC:
                match button:
                    case 0:
                        self.resetCount += 1
                        self.recording = False
                        self.recorder.stop()
                        for osc in self.oscs:
                            osc.clear_notes()
                        if self.resetCount == 2:
                            self.oscs = [Oscillator(), Oscillator(),
                                         Oscillator(), Oscillator()]
                    case 1:
                        self.recorder.pause_toggle()
                    case 2:
                        self.recording = not self.recording
            case constants.OSC_SELECT:
                self.selectedOsc = button
            case constants.OSC_MUTE:
                self.unmuted[button] = not self.unmuted[button]
            case constants.OSC_AMP:
                self.oscs[button].process_input(action, button, value)
            case constants.OSC_PITCH:
                if button != -1:
                    self.oscs[button].process_input(action, button, value)
                else:
                    self.oscs[self.selectedOsc].process_input(
                        action, button, value)
            case constants.FILTER_FREQ:
                self.oscs[button].process_input(action, button, value)
            case _:
                self.oscs[self.selectedOsc].process_input(
                    action, button, value)

    def next_buffer(self):
        playback = self.recorder.continue_(self.recording)
        if not self.recording and playback is not None:
            self.process_input(playback[0], playback[1], playback[2])

        buffer1 = self.oscs[0].next_buffer()
        buffer2 = self.oscs[1].next_buffer()
        buffer3 = self.oscs[2].next_buffer()
        buffer4 = self.oscs[3].next_buffer()

        if sum(self.unmuted) == 0:
            return [0 for _ in range(BUFFER_SAMPLES)]

        samples = [buffer1[i] + buffer2[i] + buffer3[i] + buffer4[i]
                   for i in range(BUFFER_SAMPLES)]
        samples = [sample * self.amp / len(self.unmuted)
                   for sample in samples]

        return samples


class Synth:
    def __init__(self):
        self.layers = [Page(), Page(), Page(), Page()]
        self.selectedLayer = 0
        self.amp = 1

    def process_input(self, action, button, value):
        if action == -1: return
        match action:
            case constants.SET_VOLUME:
                self.amp = value
            case constants.LAYER_SELECT:
                self.selectedLayer = button
            case constants.LAYER_AMP:
                self.layers[button].process_input(
                    action, button, value)
            case _:
                self.layers[self.selectedLayer].process_input(
                    action, button, value)

    def next_buffer(self):
        buffer1 = self.layers[0].next_buffer()
        buffer2 = self.layers[1].next_buffer()
        buffer3 = self.layers[2].next_buffer()
        buffer4 = self.layers[3].next_buffer()

        samples = [buffer1[i] + buffer2[i] + buffer3[i] + buffer4[i]
                   for i in range(BUFFER_SAMPLES)]
        samples = [sample * self.amp / 4
                   for sample in samples]

        # Convert samples to 16-bit signed int
        buffer = [int(max(-1, min(s * self.amp, 1)) * 32767) for s in samples]

        format_str = '<' + str(BUFFER_SAMPLES) + 'h'
        data = bytearray(struct.pack(format_str, *buffer))
        return bytes(data)
