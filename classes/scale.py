"""
Scale module

author: JD Arthur
date: 10 April 2018
"""

import math

class Scale:
    """
    A scale is a range of possible pitches.
    It is used to orient a note such as G#(2) into a specific frequency

    You can specify a base frequency, a number of semitones, and a number of octaves.
    args:
        base_frequency: frequency in Hz of the lowest note in the scale
            64 Hz is low C in 'Verdi tuning'.
        semitones: number of tones in the  chromatic scale
            Anything other than 12 will probably sound weird
        octaves: number of octaves available to scale
            5 is roughly what you've got available on a digital keyboard
    """
    def __init__(self, base_frequency=64.0, semitones=12, octaves=5, chromatic=None):
        self.base_frequency = base_frequency
        self.semitones = semitones
        self.octaves = octaves

        self.freq_list = []
        self.min_pitch = 0
        self.max_pitch = semitones * octaves - 1

        if chromatic is None:
            self.chromatic = ['c', 'c#', 'd', 'd#', 'e', 'f',
                              'f#', 'g', 'g#', 'a', 'a#', 'b']
        else:
            self.chromatic = chromatic

        for i in range(0, octaves * semitones):
            freq = math.pow(2, float(i) / float(semitones)) * base_frequency
            self.freq_list.append(freq)

    def get_frequency(self, abs_pitch):
        """
        Get frequency from abs pitch.

        Useful for Note objects
    	"""
        return self.freq_list[abs_pitch]

    def sub_scale(self, indices):
        """
        get a scale that is a subset of the chromatic scale
        Ex: a Major scale would be
           scale.subscale([0, 2, 4, 5, 7, 9, 11])
        """
        sub_scale = []
        for item in indices:
            if item >= len(self.chromatic):
                pass
            else:
                sub_scale.append(self.chromatic[item])
        return sub_scale


    def serial(self):
        """
        return a minimal version of this object that can be used to reconstruct it
        """
        minimal = {
            "base_frequency" : self.base_frequency,
            "semitones" : self.semitones,
            "octaves" : self.octaves,
            "chromatic" : self.chromatic
        }
        return minimal

"""
s = Scale(base_frequency=65.4064)
print(s.get_frequency(32))
print(s.MIN_PITCH)
print(s.MAX_PITCH)
"""