# SoundForge - A Digital Subtractive Synthesizer
<sup>**Version 1.1.0-0**  |  Iteration 1.8.8-e</sup>  
SoundForge is a digital audio synthesizer designed to allow simple music creation without the need for a full DAW. It can run on a headless Raspberry Pi, and is controlled via MIDI input.

## Features
- SoundForge creates sound via subtractive synthesis.
- There are four distinct, toggleable layers. Each layer has it's own customizable oscillators, effectively acting like four synthesizers that can play together, or seperately.
- Each layer has the ability to record and play back inputs. While you are playing live on layer 1, the other layers can each be looping a differant harmony that you have pre-recorded.
- Every one of the 16 oscillators has it's own filter and waveform selection, along with it's own independant envelopes and modulators for amplitude, pitch shifting, and filter cutoff frequancy.
- Oscillators react to setting changes in realtime. Even while a recording is playing!

## Installation
Here are the steps to install and begin using SoundForge:
1. Ensure that both Python and a C compiler are installed on your system.
2. Install the necessary Python libraries with 'pip install rtmidi-python pyaudio'
3. Clone this repo.
4. Compile the files in "src/c_synth" into a shared library called "libcsynth".
    - Using GCC on a Linux system, this command would be: `gcc -shared -o libcsynth.so -fPIC control.c synthesis.c`
5. Run main.py with a Python interperator running Python 3.11+

## Usage
Run main.py with a Python interperater to launch the synthesizer. If you are on a headless Rasperry Pi, it is recommended to have main.py run on startup. SoundForge should automatically interface with any connected MIDI device. SoundForge is setup for usage with a Donner MIDI MK-25 by default, however, all the mappings are adjustable by modifying midi_input.py.
Possible bindings include, but are not limited to:
- Adjust volume
- Play note
- Change selected layer
- Change selected layer's amplitude
- Start recording[^1]
- Playback recording in loop[^2]
- Change selected oscillator
- Mute oscillator
- Change selected oscillator's amplitude
- Change selected oscillators waveform
- Change selected oscillators detune or pitch offset[^3]
- Select a modulator to adjust for the currently selected oscillator
- Change modulator settings[^4]

[^1]: Recording starts when the first note is played, and ends when the recording button is pushed again.  
[^2]: It is also possible to pause the recording playback.  
[^3]: It is possible to adjust the pitch offset in units of cents, steps and octaves.
[^4]: There are several bindings for this that vary by modulator. For example, the low frequancy oscillator two settings: speed and amplitude, but an envelope has four: attack, decay, sustain, release.  

## Coming Soon
- [ ] Better documentation

Approximate Update Roadmap:
- [x] 1.0.0-0 Implement in C for better performance
- [x] 1.0.0-1 Add exit button binding
- [x] 1.1.0-0 Sync the release of pitch/filter with amp's
- [ ] 1.1.1-0 Add ability for multiple voices in an oscillator
- [ ] 1.1.2-0 Add ability to change LFO waveform
- [ ] 1.1.3-1 Add recorder
- [ ] 1.1.4-0 Add noise oscillator
- [ ] 1.1.4-1 Allow for use of decay/sustain in LPF cutoff envelope
- [ ] 1.1.5-0 Add pitch-determined amplitude
