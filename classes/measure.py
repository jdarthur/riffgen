from .constants import *

class Measure :
	"""
	A measure is a collection of notes.

	It has a time signature and a tempo in beats per minute
	"""
	def __init__(self, time_signature="common", tempo=120) :
		self.top = 0
		self.bottom = 0
		if(time_signature == "common") : 
			self.top = 4
			self.bottom = 4
		elif (time_signature == "3/4") :
			self.top = 3
			self.bottom = 4
		else: 
			print("Unsupported time signature")
		
		self.MIN_POSITION = 0
		self.MAX_POSITION = 32 * (self.top / self.bottom) - 1
		self.tempo = tempo
		self.position_length = float(60/tempo) / 8
		self.note_dict = {}
		self.beats = int(32 * (self.top / self.bottom) / 8)

	def add(self, note, position) :
		if(position > self.MAX_POSITION) : 
			raise PositionError("Position {0} greater than max {1}".format(position, self.MAX_POSITION))
		self.note_dict[position] = (note.frequency, self.to_seconds(note))

	def to_seconds(self, note) :
		note, duration = note.to_human_readable()
		fraction = duration_dict[duration]
		return (self.tempo / 60 ) * fraction


class PositionError(Exception) :
	def __init__(self, message) :
		self.message = message
		super(Exception, self).__init__(message)

