import math

class Scale :
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
	def __init__(self, base_frequency=64.0, semitones=12, octaves=5) :
		self.freq_list = []
		self.MIN_PITCH = 0
		self.MAX_PITCH = semitones * octaves - 1

		for i in range(0, octaves * semitones) :
			freq = math.pow(2, float(i) / float(semitones)) * base_frequency
			self.freq_list.append(freq)
		#print(self.freq_list)

	def get_frequency(self, abs_pitch) :
		return self.freq_list[abs_pitch]

	

"""
s = Scale(base_frequency=65.4064)
print(s.get_frequency(32))
print(s.MIN_PITCH)
print(s.MAX_PITCH)
"""