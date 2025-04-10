# These constants have to match the ones in constants.h
BUFFER_SAMPLES = 256  # Number of samples in one buffer of audio
SAMPLE_RATE = 44100  # Sampling rate of the audio
VOICES = 12  # Max number of voices that a layer can have

MIDI_TO_A4 = 57  # MIDI input that corrosponds to A4
MAX_CUTOFF = 10000  # Maximum filter cutoff frequancy
MIN_CUTOFF = 250  # Minimun filter cutoff frequancy

POWER = 0
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
UNISON = 24
