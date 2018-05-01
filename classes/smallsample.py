"""
SmallSample class

author: JD Arthur
date: 7 April 2018
"""

import math
import numpy as np

BASE_DB = -26

def a_weight(frequency):
    """
    perform a-weighting operation to fix subjective loudness
    based on frequency
    """
    f_squared = math.pow(frequency, 2)
    numerator = math.pow(12194, 2) * math.pow(f_squared, 2)
    denominator = ((f_squared + math.pow(20.6, 2)) *
                   (math.sqrt((f_squared + math.pow(107.7, 2)) *
                              (f_squared + math.pow(737.9, 2)))) *
                   (f_squared + math.pow(12194, 2)))
    ra_f = numerator / denominator
    adjusted = 20 * math.log10(ra_f) + 2.00
    return adjusted

def scale_factor(db_a):
    """
    get the amplitude scale factor from our dbA
    to calculate what we need to multiply by to
    """
    g_db = BASE_DB - db_a
    scalefac = math.pow(10, g_db / 20)
    return scalefac

class SmallSample:
    """
    this creates a sample of 1 note.
    """
    def __init__(self, frequency, length, articulation='regular', rate=20000):
        """ampl_arr = articulations.get(length, None)
        if ampl_arr == None:
            articulations[length] = {}
            articulations[length][articulation] = create_ampl_array(length, rate, .7)

        ampl_arr = articulations[length][articulation]
        """
        self.sample = (np.sin(2 * np.pi * np.arange(rate * length) *
                              frequency / rate)).astype(np.float32)
        self.adjusted_db = a_weight(frequency)
        self.deamplify(scale_factor(self.adjusted_db))

    def deamplify(self, scale_factor):
        """
        lower average amplitude by scale factor to even out perceived sound levels
        """
        self.sample = np.multiply(self.sample, scale_factor)

    def create_attackdecay(self, start_decibels, end_decibels, length):
        """
        create a smaller array to control attack/decay in
        the complete amplitude array.

        It will smoothly ramp decibels which correlated to a
        logarithmic increase/decrease in amplitude I believe.
        """

        inc = (start_decibels - end_decibels) * (1 / int(length))
        decibels = start_decibels
        arr = []
        for i in range(0, length):
            decibels = decibels - inc
            vol = math.pow(10, decibels/20)
            arr.append(vol)
        return arr

    def create_ampl_array(self, leng, rate, decayfactor):
        """
        Create an array to control amplitude in the sample

        This will use a fixed attack length (1/64 of leng * rate).
            Might rework this part if it matters
        Decay is variable based on decayfactor [0.0: 1.0)
        I'm using this decay to do different articulations
            i.e. staccato has a decay factor of about .8
        """
        amplitude_array = []
        high_db = 0
        inaudible_db = -200

        #attack phase
        attack_length = int(leng * rate / 64)
        att = self.create_attackdecay(inaudible_db, high_db, attack_length)

        #decay phase
        decay_length = int(leng * rate * decayfactor)
        dec = self.create_attackdecay(high_db, inaudible_db, decay_length)

        for i in range(0, int(leng * rate)):
            if i < attack_length:
                amplitude_array.append(att[i])
            elif leng * rate - i < decay_length:
                amplitude_array.append(dec[decay_length - int(leng * rate) + i])
            else:
                amplitude_array.append(math.pow(10, high_db))
        return amplitude_array
