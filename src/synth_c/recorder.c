#include <stdlib.h>

#include "constants.h"
#include "recorder.h"

void initialize_recorder(Recorder *rec) {
    rec->tick = 0;
    rec->play_tick = 0;
    rec->input_count = 0;
    for (int i=0; i < REC_MAX_INPUTS; i++) {
        rec->inputs[i] = NULL;
    }
}

void clear_recorder(Recorder *rec) {
    rec->tick = 0;
    rec->play_tick = 0;
    rec->input_count = 0;
    for (int i=0; i < REC_MAX_INPUTS; i++) {
        if (rec->inputs[i] != NULL) {
            free(rec->inputs[i]);
            rec->inputs[i] = NULL;
        }
    }
}

void recorder_tick(Recorder *rec, int recording) {
    if (recording) {
        rec->tick += 1;
    } else {
        rec->play_tick += 1;
        if (rec->play_tick == rec->tick){
            rec->play_tick = 0;
        }
    }
}

void recorder_record(Recorder *rec, int in_data1, int in_data2) {
    if (rec->input_count == REC_MAX_INPUTS) {
        return;
    }
    Input *input_ptr;
    input_ptr = malloc(sizeof(Input));
    input_ptr->tick_played = rec->tick;
    input_ptr->value[0] = in_data1;
    input_ptr->value[1] = in_data2;

    rec->inputs[rec->input_count] = input_ptr;
    rec->input_count += 1;
}
