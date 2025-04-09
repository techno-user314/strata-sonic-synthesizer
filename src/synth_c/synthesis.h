/*
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
*/
#ifndef SYNTHESIS_H
#define SYNTHESIS_H

typedef struct Envelope {
    int envAt;
    int releasing;
    float *sustain_value;

    int *attack_ms;
    int *decay_ms;
    float *sustain_percent;
    int *release_ms;
} Envelope;

typedef struct LFO {
    double lfoAt;
    int *speed_hz;
    double *percent_effect;
} LFO;

typedef struct LPF {
    double in_history[3];
    double out_history[3];
} LPF;

typedef struct Osc {
    int type;
    double oscAt;
    int note;
} Osc;

void envelope(Envelope *env_vals, double *samples);

void lfosc(LFO *lfo_vals, double *samples);

void lpfilter(LPF *lpf_vals, double *samples, double *cutoff_freq_vals);

void oscillator(Osc *osc_vals, double *samples,
                double *amp_values, double *pitch_shift_values);

#endif
