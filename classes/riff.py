from .bigsample import BigSample
from .smallsample import SmallSample

class Riff :
	"""
	A riff is a collection of one or more measures.

	It only cares about instances of Hz * Seconds.

	It is readable from and writable to a .riff file. 
	This means it can be instantiated via either a list of
	Measure objects or a filename. 
	"""
	def __init__(self, Measures=None, filename=None) :
		if(Measures == None) :
			if(filename == None) :
				raise RiffError("Filename not defined!")
			self.Measures = load_riff(filename)
		else:
			self.Measures = Measures

		self.riff_dict = {}
		self.runtime = 0
		for item in Measures :
			for key in item.note_dict :
				self.riff_dict[key * item.position_length + self.runtime] = item.note_dict[key]
			self.runtime += float(item.MAX_POSITION + 1) * item.position_length
		print(self.riff_dict)
	
	def load_riff(filename) :
		pass

	def create_sample(self) :
		big = BigSample(self.runtime)
		rate = big.rate

		samples = []
		for key in self.riff_dict :
			freq = self.riff_dict[key][0]
			length = self.riff_dict[key][1]
			samp = SmallSample(freq, length, rate=big.rate).sample

			big.add_inplace2(samp, key * rate)

		return big

class RiffError(Exception) :
	def __init__(self, message) :
		self.message = message
		super(Exception, self).__init__(message)		
