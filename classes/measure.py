"""
Measure Class

author: JD Arthur
date: 7 Apr 2018
"""
from .constants import duration_dict
from .scale import Scale

class Measure:
    """
    A Measure is a collection of notes.

    It has a time signature and a tempo in beats per minute.
    Useful fields:
       note_dict:
       		dictionary of {position : (frequency, duration)} values
       		useful for translation to a Riff/Sample
       max_position:
            number of 32nd notes in this measure - 1
       position_length:
            length of a 32nd note at our tempo
    """
    def __init__(self, time_signature="common", tempo=120, key=None):
        self.top = 0
        self.bottom = 0
        if time_signature == "common":
            self.top = 4
            self.bottom = 4
        elif time_signature == "3/4":
            self.top = 3
            self.bottom = 4
        else:
            print("Unsupported time signature")
        self.time_signature = time_signature

        if key is None:
            self.key = Scale()
        else:
            self.key = key
        self.chromatic = self.key.chromatic

        self.max_position = 32 * (self.top / self.bottom) - 1
        self.tempo = tempo
        self.position_length = float(60/tempo) / 8
        self.note_dict = {}
        self.beats = int(32 * (self.top / self.bottom) / 8)

    def add(self, note, position):
        """
        Add a Note to a certain position.

        If you try to add to a Note to an illegal position,
        this method will throw a PositionError.

        args:
        	note: a Note object
        	position: an int in range [0 ... max_position]
        """
        if position > self.max_position:
            raise PositionError("Position {0} greater than " \
            	"max {1}".format(position, self.max_position))
        #self.note_dict[position] = (note.frequency, self.to_seconds(note))
        self.note_dict[position] = note

    def to_seconds(self, note):
        """
        Convert a note duration to a second-fraction using this measure's tempo

        returns:
        	float representing a note duration
        """
        note, duration = note.to_human_readable()
        fraction = duration_dict[duration]
        return (self.tempo / 60) * fraction

    def serial(self):
        """
        return a minimal version of this object that can be used to reconstruct it
        """
        notes = {}
        for pos in self.note_dict:
            note = self.note_dict[pos]
            notes[pos] = note.serial()

        minimal = {
            "key" : self.key.serial(),
            "time_signature" : self.time_signature,
            "tempo" : self.tempo,
            "notes" : notes

        }
        return minimal


class PositionError(Exception):
    """
    Error representing incorrect position in a Measure
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)
