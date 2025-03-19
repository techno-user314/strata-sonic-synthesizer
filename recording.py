"""
A class to handle the recording, timestamping, and playback of
MIDI input codes.

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
from constants import MAX_RECORDING

class InputRecorder:
    def __init__(self):
        self.timestamp = 0
        self.max_time = 0
        self.inputs = {}
        self.active_rec = False
        self.paused = False

    def continue_(self, rec=False):
        if not self.active_rec and rec:
            self.paused = False
            self.timestamp = 0
            self.inputs = {}
        elif self.active_rec and not rec:
            self.max_time = self.timestamp
            self.timestamp = 0
        self.active_rec = rec

        if rec:
            self.timestamp += 1
            return None
        elif not self.paused:
            self.timestamp += 1
            if len(self.inputs) > 0:
                if self.timestamp in self.inputs:
                    return self.inputs[self.timestamp]
                if self.timestamp >= self.max_time:
                    self.timestamp = 0
        return None
        
    def record(self, value):
        if  self.active_rec and value is not None:
            if len(self.inputs) == 0:
                self.timestamp = 1
            if len(self.inputs) < MAX_RECORDING:
                self.inputs.update({self.timestamp:value})

    def pause_toggle(self):
        if not self.active_rec:
            self.paused = not self.paused

    def stop(self):
        self.paused = False
        self.timestamp = 0
        self.inputs = {}
        self.active_rec = False