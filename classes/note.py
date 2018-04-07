from .scale import Scale
from .constants import *

class Note :
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

	def __init__(self, abs_pitch=None, abs_duration=None, tone=None, octave=None, notelength=None, chromatic=None, scale=None) :
		
		self.duration_list = duration_list
		if(scale == None) :
			self.scale = Scale()
		else :
			self.scale = scale
		self.chromatic = self.scale.chromatic

		if(abs_pitch == None) :
			if(tone == None) :
				raise PitchError("Missing tone")
			if(octave == None) :
				raise PitchError("Missing octave")
			abs_pitch = self.get_abs_pitch(tone, octave)

		if(abs_pitch < self.scale.MIN_PITCH) :
			raise PitchError("Pitch {0} is less than min {1}.".format(abs_pitch, self.scale.MIN_PITCH))
		if(abs_pitch > self.scale.MAX_PITCH) :
			raise PitchError("Pitch {0} is greater than max {1}.".format(abs_pitch, self.scale.MAX_PITCH))
		self.abs_pitch = abs_pitch

		if(abs_duration == None) :
			if(notelength == None) :
				raise DurationError("Missing note length")
			abs_duration = self.get_abs_duration(notelength)

		if(abs_duration < 0) :
			raise DurationError("Duration {0} is less than min 0.".format(abs_duration))
		if(abs_duration > 5) :
			raise DurationError("Duration {0} is greater than max 5.".format(abs_duration))
		self.abs_duration = abs_duration
		self.frequency = self.scale.get_frequency(self.abs_pitch)

	
	def to_human_readable(self) :
		tone = self.chromatic[self.abs_pitch % 12].upper()
		octave = int(self.abs_pitch / 12)
		note = "{0}({1})".format(tone, octave)

		duration = self.duration_list[self.abs_duration]
		return note, duration

	def get_abs_pitch(self, tone, octave) :
		num = self.chromatic.index(tone.lower())
		octave_shift = 12 * octave
		return num + octave_shift

	def get_abs_duration(self, notelength) :
		return self.duration_list.index(notelength)


"""
Exceptions for illegal Pitch + Duration input
"""
class PitchError(Exception) :
	def __init__(self, message) :
		self.message = message
		super(Exception, self).__init__(message)

class DurationError(Exception) :
	def __init__(self, message) :
		self.message = message
		super(Exception, self).__init__(message)

"""
x = Note(32, 3)
note, duration = x.to_human_readable()
print(note) #G#(2)
print(duration) #quarter
"""

"""
y = Note(tone="g#", octave=2, notelength="quarter")
note, duration = y.to_human_readable()
print(note) #G#(2)
print(duration) #quarter
"""
