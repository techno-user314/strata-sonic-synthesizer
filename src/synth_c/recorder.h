#ifndef RECORDER_H
#define RECORDER_H

#include "constants.h"

typedef struct Input {
    int tick_played;
    int value[2];
} Input;

typedef struct Recorder {
    int tick;
    int play_tick;
    int input_count;
    Input *inputs[REC_MAX_INPUTS];
} Recorder;

void initialize_recorder(Recorder *rec);
void clear_recorder(Recorder *rec);
void recorder_tick(Recorder *rec, int recording);
void recorder_record(Recorder *rec, int in_data1, int in_data2);

#endif
