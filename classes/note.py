"""
Note Class

author: JD Arthur
date: 7 April 2018
"""


from .constants import duration_list, lendict

class Note:
    """
    A note is a combination of pitch + duration.

    Pitch:
        In a C chromatic scale, pitch can be anything from C(0), D(0), ..., A(4), B(4)
        this is composed of a tone in the chromatic scale:
            ['c','c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
        and an octave in:
            [0, 1, 2, 3, 4]
    Duration:
        index into this list:
            ['thirty-second', 'sixteenth', 'eighth', 'quarter', 'half', 'whole']

        Represents note length in relation to a measure.
            i.e. a sixteenth note is 1/16 the length of the measure it is in

    so for example:
        x = Note(32, 3)
    represents a G# quarter note in octave 2
    """

    def __init__(self, rel_pitch=None, scale=None, abs_duration=None, hr_dict=None):
        self.duration_list = duration_list
        if scale is None:
            raise ScaleError("Missing scale!")
        else:
            self.scale = scale
        self.chromatic = self.scale.chromatic

        if rel_pitch is None:
            tone = hr_dict.get("tone", None)
            octave = hr_dict.get("octave", None)
            if tone is None:
                raise PitchError("Missing tone!")
            if octave is None:
                raise PitchError("Missing octave!")
            rel_pitch = self.get_rel_pitch(tone, octave)

        if rel_pitch < self.scale.min_pitch:
            raise PitchError("Pitch {0} is less than min " \
                "{1}.".format(rel_pitch, self.scale.min_pitch))
        if rel_pitch > self.scale.max_pitch:
            raise PitchError("Pitch {0} is greater than max " \
                "{1}.".format(rel_pitch, self.scale.min_pitch))
        self.rel_pitch = rel_pitch

        if abs_duration is None:
            notelength = hr_dict["notelength"]
            if notelength is None:
                raise DurationError("Missing note length!")
            abs_duration = self.get_abs_duration(notelength)

        if abs_duration < 0:
            raise DurationError("Duration {0} is less than min 0.".format(abs_duration))
        if abs_duration > 5:
            raise DurationError("Duration {0} is greater than max 5.".format(abs_duration))
        self.abs_duration = abs_duration
        self.frequency = self.scale.get_frequency(self.rel_pitch)
        self.hr_note, self.hr_duration = self.to_human_readable()
        self.len = lendict[self.hr_duration]

    def to_human_readable(self):
        """
        Convert absolute pitch/duration into human-readable representation
        Example in C major w/ 5 octaves:
          32 == G# in octave 2
          3 == quarter note
        """
        tone = self.chromatic[self.rel_pitch % 12].upper()
        octave = int(self.rel_pitch / 12)
        note = "{0}({1})".format(tone, octave)

        duration = self.duration_list[self.abs_duration]
        return note, duration

    def get_rel_pitch(self, tone, octave):
        """
        Get absolute pitch from tone and octave
        """
        num = self.chromatic.index(tone.lower())
        octave_shift = 12 * octave
        return num + octave_shift

    def get_abs_duration(self, notelength):
        """
    	get absolute duration from human-readable
        """
        return self.duration_list.index(notelength)

    def serial(self):
        """
        return a minimal version of this object that can be used to reconstruct it
        """
        minimal = {
            "rel_pitch" : self.rel_pitch,
            "abs_duration" : self.abs_duration
        }
        return minimal


"""
Exceptions for illegal Pitch + Duration input
"""
class PitchError(Exception):
    """"
    Illegal Pitch (out of range or missing)
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class DurationError(Exception):
    """
    Illegal duration (out of range or missing)
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class ScaleError(Exception):
    """
    Illegal scale (missing)
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)

"""
#examples

x = Note(32, 3)
note, duration = x.to_human_readable()
print(note) #G#(2)
print(duration) #quarter

y = Note(tone="g#", octave=2, notelength="quarter")
note, duration = y.to_human_readable()
print(note) #G#(2)
print(duration) #quarter
"""
