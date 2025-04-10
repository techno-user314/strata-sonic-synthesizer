# SoundForge - A Digital Subtractive Synthesizer
<sup>**Version 1.1.1**  |  Iteration 1.8.9-20 </sup>  
  
SoundForge is a digital audio synthesizer designed to allow simple music creation without the need for a full DAW. It can run on a headless Raspberry Pi, and is controlled via MIDI input.

## Features
- SoundForge creates sound via subtractive synthesis.
- SoundForge currently supports up to 25 voices per layer. In the future, this will be user defined so that it can be customized to the user's computer's architechture capabilities.
- There are four distinct, toggleable layers. Each layer has it's own customizable oscillators, effectively acting like four seperate synthesizers. This feature can be used to toggle between four setting banks and, in future updates, may be able to loop a background harmony.
- Every one of the 16 oscillators has it's own filter and waveform selection, along with it's own independant envelopes and modulators for amplitude, pitch shifting, and filter cutoff frequancy.

## Installation
Here are the steps to install and begin using SoundForge:
1. Ensure that both Python and a C compiler are installed on your system.
2. Install the necessary Python libraries with `pip install rtmidi-python pyaudio`
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
- [x] 1.0.0 Make DSPcmath more efficient
- [x] 1.0.1 Add exit button
- [x] 1.0.1 Sync the release of pitch/filter with amp's
- [x] 1.0.2 Fix page bug
- [x] 1.0.3 Fix what happens when page is changed before note is released
- [x] 1.0.4 Fix pitch octave shift always going super high freq
- [x] 1.0.5 Fix LFO amplitude effect
- [x] 1.1.0 Add unison
- [x] 1.1.1 Clean up input processing method
- [ ] 1.1.2 Make voice numbers a constant, not a magic number
- [ ] 1.2.0 Add recorder
- [ ] 1.3.0 Add noise oscillator
- [ ] 1.3.1 Implement more intuitive input mapping
- [ ] 1.4.0 Add pitch-determined amplitude
- [ ] 1.5.0 Add support for stereo/panning
- [ ] 2.0.0 Allow for multithreading
