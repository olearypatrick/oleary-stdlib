"""
stdaudio.py

The stdaudio module defines functions related to audio.
"""

import os
import sys
import numpy
import stdio

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

# ----------------------------------------------------------------------------------------------------------------------

_SAMPLES_PER_SECOND = 44100
_SAMPLE_SIZE = -16            # Each sample is a signed 16-bit int
_CHANNEL_COUNT = 1            # 1 => mono, 2 => stereo
_AUDIO_BUFFER_SIZE = 1024     # In number of samples
_CHECK_RATE = 44100           # How often to check the queue

_myBuffer = []
_MY_BUFFER_MAX_LENGTH = 4096  # Determined experimentally.


# ----------------------------------------------------------------------------------------------------------------------

def wait():
    """
    Wait for the sound queue to become empty.  Informally, wait for the currently playing sound to finish.
    """
    global _channel

    clock = pygame.time.Clock()
    while _channel.get_queue() is not None:
        clock.tick(_CHECK_RATE)


# ----------------------------------------------------------------------------------------------------------------------

def play_sample(s):
    """
    Play sound sample s.
    """
    global _myBuffer
    global _channel

    _myBuffer.append(s)
    if len(_myBuffer) > _MY_BUFFER_MAX_LENGTH:
        temp = []
        for sample in _myBuffer:
            temp.append(numpy.int16(sample * float(0x7fff)))
        samples = numpy.array(temp, numpy.int16)
        sound = pygame.sndarray.make_sound(samples)
        wait()
        _channel.queue(sound)
        _myBuffer = []


# ----------------------------------------------------------------------------------------------------------------------

def play_samples(a):
    """
    Play all sound samples in array a.
    """
    for sample in a:
        play_sample(sample)


# ----------------------------------------------------------------------------------------------------------------------

def play_array(a):
    """
    This function is deprecated. It has the same behavior as stdaudio.play_samples(). Please call 
    stdaudio.play_samples() instead.
    """
    play_samples(a)


# ----------------------------------------------------------------------------------------------------------------------

def play_file(f):
    """
    Play all sound samples in the file whose name is f.wav.
    """
    a = read(f)
    play_samples(a)


# ----------------------------------------------------------------------------------------------------------------------

def save(f, a):
    """
    Save all samples in array a to the WAVE file whose name is f.wav.
    """
    import wave

    filename = f + '.wav'
    temp = []
    for sample in a:
        temp.append(int(sample * float(0x7fff)))
    samples = numpy.array(temp, numpy.int16)
    file = wave.open(filename, 'w')
    file.setnchannels(_CHANNEL_COUNT)
    file.setsampwidth(2)
    file.setframerate(_SAMPLES_PER_SECOND)
    file.setnframes(len(samples))
    file.setcomptype('NONE', 'descrip')
    file.writeframes(samples.tostring())
    file.close()


# ----------------------------------------------------------------------------------------------------------------------

def read(f):
    """
    Read all samples from the WAVE file whose names is f.wav. Store the samples in an array, and return the array.
    """
    filename = f + '.wav'
    sound = pygame.mixer.Sound(filename)
    samples = pygame.sndarray.samples(sound)
    temp = []
    for i in range(len(samples)):
        temp.append(float(samples[i]) / float(0x7fff))
    return temp


# ----------------------------------------------------------------------------------------------------------------------

# Initialize PyGame to handle audio.

try:
    pygame.mixer.init(
        _SAMPLES_PER_SECOND,
        _SAMPLE_SIZE,
        _CHANNEL_COUNT,
        _AUDIO_BUFFER_SIZE)
    _channel = pygame.mixer.Channel(0)
except pygame.error:
    stdio.writeln('Could not initialize PyGame')
    sys.exit(1)


# ----------------------------------------------------------------------------------------------------------------------

def _create_text_audio_file():
    """
    For testing. Create a text audio file.
    """
    import outstream

    notes = [
        7, .270,
        5, .090,
        3, .180,
        5, .180,
        7, .180,
        6, .180,
        7, .180,
        3, .180,
        5, .180,
        5, .180,
        5, .180,
        5, .900,

        5, .325,
        3, .125,
        2, .180,
        3, .180,
        5, .180,
        4, .180,
        5, .180,
        2, .180,
        3, .180,
        3, .180,
        3, .180,
        3, .900,
        ]

    _outstream = outstream.OutStream('looney.txt')
    for note in notes:
        _outstream.writeln(note)


def _main():
    """
    For testing.
    """
    import math
    import instream

    _create_text_audio_file()

    stdio.writeln('Creating and playing in small chunks...')
    sps = _SAMPLES_PER_SECOND
    _instream = instream.InStream('looney.txt')
    while not _instream.is_empty():
        pitch = _instream.read_int
        duration = _instream.read_float()
        hz = 440 * math.pow(2, pitch / 12.0)
        n = int(sps * duration)
        notes = []
        for i in range(n+1):
            notes.append(math.sin(2*math.pi * i * hz / sps))
        play_samples(notes)
    wait()

    stdio.writeln('Creating and playing in one large chunk...')
    sps = _SAMPLES_PER_SECOND
    notes = []
    _instream = instream.InStream('looney.txt')
    while not _instream.is_empty():
        pitch = _instream.read_int
        duration = _instream.read_float()
        hz = 440 * math.pow(2, pitch / 12.0)
        n = int(sps * duration)
        for i in range(n+1):
            notes.append(math.sin(2*math.pi * i * hz / sps))
    play_samples(notes)
    wait()

    stdio.writeln('Saving...')
    save('looney', notes)

    stdio.writeln('Reading...')
    notes = read('looney')

    stdio.writeln('Playing an array...')
    play_samples(notes)
    wait()

    stdio.writeln('Playing a file...')
    play_file('looney')
    wait()

    os.remove('looney.wav')
    os.remove('looney.txt')


if __name__ == '__main__':
    _main()
