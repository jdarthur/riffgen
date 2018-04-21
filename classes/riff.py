"""
Riff Class

author: JD Arthur
date: 8 April 2018
"""

import pickle
from .bigsample import BigSample
from .measure import Measure
from .note import Note
from .smallsample import SmallSample
from .scale import Scale


class Riff:
    """
    A riff is a collection of one or more measures.

    It only cares about instances of Hz * Seconds.

    It is readable from and writable to a .riff file.
    This means it can be instantiated via either a list of
    Measure objects or a filename.

    riff_dict is the key data structure. It is composed of
    time : (frequency, duration) pairs.
    Ex:
       .25 : (256, .5) would mean

    256 Hz for .5 seconds, starting at .25 seconds from the beginning of the sample
    """
    def __init__(self, measures=None, filename=None):
        if measures is None:
            if filename is None:
                raise RiffError("Filename not defined!")
            self.measures = self.load_riff(filename)
        else:
            self.measures = measures

        self.riff_dict = {}
        self.runtime = 0
        for item in self.measures:
            for key in item.note_dict:
                note = item.note_dict[key]
                self.riff_dict[key * item.position_length + self.runtime] = (note.frequency, item.to_seconds(note))
            self.runtime += float(item.max_position + 1) * item.position_length
        #print(self.riff_dict)

    def load_riff(self, filename):
        """
        Load riff from filename
        """
        in_list = []
        measures = []
        with open(filename, 'rb+') as file_obj:
            in_list = pickle.load(file_obj)
        for item in in_list:
            sscale = item['key']
            scale = Scale(sscale['base_frequency'], sscale['semitones'],
                          sscale['octaves'], sscale['chromatic'])
            measure = Measure(item['time_signature'], item['tempo'], key=scale)
            for pos in item['notes']:
                snote = item['notes'][pos]
                note = Note(snote["rel_pitch"], scale, snote['abs_duration'])
                measure.add(note, pos)
            measures.append(measure)
        return measures


    def write_riff(self, filename):
        """
        Write riff to file
        """
        out_list = []
        for item in self.measures:
            out_list.append(item.serial())
        print(out_list)
        with open(filename, 'wb+') as file_obj:
            pickle.dump(out_list, file_obj)

    def create_sample(self):
        """
    	Create a sample object from our Riff object
        """
        big = BigSample(self.runtime)
        rate = big.rate

        for key in self.riff_dict:
            freq = self.riff_dict[key][0]
            length = self.riff_dict[key][1]
            samp = SmallSample(freq, length, rate=big.rate).sample

            big.add_inplace2(samp, key * rate)

        return big

class RiffError(Exception):
    """
    Error represention a problem in the Riff class
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)
