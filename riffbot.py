"""
Main class to generate a riff
"""

import time
import sounddevice as sd
from classes.note import Note
from classes.measure import Measure
from classes.riff import Riff
from classes.scale import Scale
from lib.utils import choose_weighted


"""
===================================================
                    METHODS
===================================================
"""

def random_measure(notecount, scale=None, subscale=[0, 2, 4, 5, 7, 9, 11], toneweights=None):
    """
    create a bunch of random notes in random locations
    """
    if scale is None:
        scale = Scale()
    measure = Measure(key=scale)
    tonechoices = scale.sub_scale(subscale)
    if toneweights is None:
        toneweights = []
        for choice in tonechoices:
            toneweights.append(10)

    lenchoices = ['quarter', 'eighth', 'sixteenth']
    lenweights = [30, 100, 30]

    pos = 0
    for i in range(0, notecount):
        tone = choose_weighted(tonechoices, toneweights)
        notelength = choose_weighted(lenchoices, lenweights)
        hr_dict = {
            "tone" : tone,
            "notelength" : notelength,
            "octave" : 2
        }
        note = Note(scale=scale, hr_dict=hr_dict)
        pos += note.len
        if pos + note.len <= measure.max_position:
            measure.add(note, pos)
    return measure

#timing. using this to evaluate performance
timer = time.time()

#m = random_measure(12)
#m2 = random_measure(12)

scale = Scale(semitones=7, chromatic=['a', 'b', 'c', 'd', 'e', 'f'])
subscale = scale.sub_scale([0, 2, 4, 6])
m = random_measure(12, scale=scale)
m2 = random_measure(12, scale=scale)

r = Riff(measures=[m, m2])
#r = Riff(filename='test.riff')
#r.write_riff("test.riff")
big = r.create_sample()
bytes1 = big.get_bytes()

#second timer to calculate elapsed time
t2 = time.time() - timer
print("runtime: {0}s".format(t2))

#actually play our sample
sd.play(bytes1, big.rate, blocking=True)
