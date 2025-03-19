"""
This file contains functions that acually handle the creation of the
raw audio samples. They return a buffer's worth of audio, as defined
by BUFFER_SAMPLES.

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
from math import cos, sin, sqrt, pi, tau

cdef int BUFFER_SAMPLES = 256
cdef int SAMPLE_RATE = 44100

def envelope(int start_at_sample, float sustain_value, bint releasing,
             int attack_ms, int decay_ms, float sustain_percent, int release_ms):
    cdef float samples_per_ms = (SAMPLE_RATE / 1000)
    cdef int attack_samples = int(attack_ms * samples_per_ms)
    cdef int decay_samples = int(decay_ms * samples_per_ms)
    cdef int release_samples = int(release_ms * samples_per_ms)
    if sustain_percent == 0 or (releasing and release_samples == 0):
        return [0. for _ in range(BUFFER_SAMPLES)]

    cdef double[256] samples
    cdef double expo, num, percent
    cdef int s, sample
    for sample in range(BUFFER_SAMPLES):
        s = sample + start_at_sample
        percent = 0.0
        if not releasing:
            if attack_samples != 0 and s < attack_samples:
                expo = 2.56 * (s / attack_samples)
                percent = (2 ** expo - 1) / 4.8971
            elif decay_samples != 0  and s < (attack_samples + decay_samples):
                expo = (-5.12) * (s / decay_samples)
                num = (2 ** expo - 1) / (-0.9712)
                percent = 1 - num * (1 - sustain_percent)
            else:
                percent = sustain_percent
        elif s < release_samples:
            percent = 256 ** (-s / release_samples) * sustain_percent
        else:
            samples[sample] = 0.0
            continue
        samples[sample] = percent / sustain_percent * sustain_value

    cdef audio_sample
    return [audio_sample for audio_sample in samples]

def lpfilter(input_samples, cutoff_freq_values, prev_in_hist, prev_out_hist):
    q_factor = 1 / sqrt(2)

    input_history = prev_in_hist
    output_history = prev_out_hist

    samples = [0 for _ in range(BUFFER_SAMPLES)]
    for j, s in enumerate(input_samples):
        w0 = tau * cutoff_freq_values[j] / SAMPLE_RATE
        _sin = sin(w0)
        _cos = cos(w0)
        alpha = _sin / (2 * q_factor)

        b0 = (1 - _cos) / 2
        b1 = 1 - _cos

        a0 = 1 + alpha
        a1 = -2 * _cos
        a2 = 1 - alpha

        a_coeffs = [a0, a1, a2]
        b_coeffs = [b0, b1, b0]

        sample = s * 2 - 1
        result = 0.0

        # Start at index 1 and do index 0 at the end.
        for i in range(1, 2 + 1): # Filter order + 1
            result += (
                    b_coeffs[i] * input_history[i - 1]
                    - a_coeffs[i] * output_history[i - 1]
            )

        result = (result + b_coeffs[0] * sample) / a_coeffs[0]

        input_history[1:] = input_history[:-1]
        output_history[1:] = output_history[:-1]

        input_history[0] = sample
        output_history[0] = result

        samples[j] = (result + 1) / 2

    return samples, input_history, output_history

def lfosc(double start_at_percent, int speed_hz,
          double amp, double percent_effect):
    if speed_hz == 0 or percent_effect == 0 or amp == 0:
        return [1 for _ in range(BUFFER_SAMPLES)], start_at_percent

    cdef double[256] samples
    cdef double change_per_step = speed_hz / SAMPLE_RATE
    cdef double s = start_at_percent
    cdef double wave
    cdef int sample
    for sample in range(BUFFER_SAMPLES):
        s = (s + change_per_step) % 1
        wave = cos(2 * pi * s)
        samples[sample] = (wave * amp + amp) / 2 * percent_effect

    cdef audio_sample
    return [audio_sample for audio_sample in samples], s+change_per_step

cdef double change_per_sample(int note, float shift, double modulator):
    cdef double note_step = note + shift * modulator
    cdef double hertz = 440 * pow(2, (note_step / 12))
    return hertz / SAMPLE_RATE

def sine_osc(double start_at_percent, int note, float shift,
             amp_values, pitch_shift_values):
    cdef double[256] samples
    cdef double s
    cdef double change_per_step
    cdef int sample
    for sample in range(BUFFER_SAMPLES):
        change_per_step = change_per_sample(note, shift,
                                            pitch_shift_values[sample])
        s = (sample * change_per_step + start_at_percent) % 1
        samples[sample] = sin(2 * pi * s) * amp_values[sample]

    cdef audio_sample
    return [audio_sample for audio_sample in samples], s+change_per_step

def square_osc(double start_at_percent, int note, float shift,
               amp_values, pitch_shift_values):
    cdef double[256] samples
    cdef double s
    cdef double change_per_step
    cdef int sample
    for sample in range(BUFFER_SAMPLES):
        change_per_step = change_per_sample(note, shift,
                                            pitch_shift_values[sample])
        s = (sample * change_per_step + start_at_percent) % 1
        if sin(2 * pi * s) > 0:
            samples[sample] = amp_values[sample]
        else:
            samples[sample] = -amp_values[sample]

    cdef audio_sample
    return [audio_sample for audio_sample in samples], s+change_per_step

def sawtooth_osc(double start_at_percent, int note, float shift,
                 amp_values, pitch_shift_values):
    cdef double[256] samples
    cdef double s
    cdef double change_per_step
    cdef int sample
    for sample in range(BUFFER_SAMPLES):
        change_per_step = change_per_sample(note, shift,
                                            pitch_shift_values[sample])
        s = (sample * change_per_step + start_at_percent) % 1
        samples[sample] = (2 * s - 1) * amp_values[sample]

    cdef audio_sample
    return [audio_sample for audio_sample in samples], s+change_per_step

def triangle_osc(double start_at_percent, int note, float shift,
                 amp_values, pitch_shift_values):
    cdef double[256] samples
    cdef double s
    cdef double change_per_step
    cdef int sample
    for sample in range(BUFFER_SAMPLES):
        change_per_step = change_per_sample(note, shift,
                                            pitch_shift_values[sample])
        s = (sample * change_per_step + start_at_percent) % 1
        if s < 0.5:
            samples[sample] = (4 * s - 1) * amp_values[sample]
        else:
            samples[sample] = (3 - 4 * s) * amp_values[sample]

    cdef audio_sample
    return [audio_sample for audio_sample in samples], s+change_per_step
