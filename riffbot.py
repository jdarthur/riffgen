"""
Main class to generate a riff
"""

import time
import sounddevice as sd


from tkinter import *
from classes.note import Note
from classes.measure import Measure
from classes.riff import Riff
from classes.scale import Scale
from lib.utils import choose_weighted, consonance


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

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.create_elements()
        self.riff = None
        self.rate = 0

    def create_elements(self):
        """
        display buttons on the window
        """
        self.master.title("riffbot")
        self.pack(fill=BOTH, expand=1)

        createbutton = Button(self, text="create", command=self.create_riff)
        createbutton.place(relx=0.5, rely=0.33, anchor=CENTER)
        playbutton = Button(self, text="play", command=self.play)
        playbutton.place(relx=0.5, rely=0.66, anchor=CENTER)

    def create_riff(self):
        """
        create a random riff
        """
        
        #timing. using this to evaluate performance
        timer = time.time()

        m = random_measure(12)
        m2 = random_measure(12)

        #scale = Scale(semitones=13, chromatic=['a', 'b', 'c', 'd', 'e', 'f'])
        #subscale = scale.sub_scale([0, 2, 4, 6])
        #m = random_measure(12, scale=scale)
        #m2 = random_measure(12, scale=scale)

        r = Riff(measures=[m, m2])
        #r = Riff(filename='test.riff')
        #r.write_riff("test.riff")
        big = r.create_sample()
        self.riff = big.get_bytes()
        self.rate = big.rate

        #second timer to calculate elapsed time
        t2 = time.time() - timer
        print("runtime: {0}s".format(t2))

    def play(self):
        """
        play riff if created
        """
        if self.riff is not None:
            sd.play(self.riff, self.rate, blocking=True)
        else:
            print("create riff first")

top = Tk()
top.geometry("200x100")
app = Window(top)
app.mainloop()
