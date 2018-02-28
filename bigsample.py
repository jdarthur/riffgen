import numpy as np

def create_empty_sample(leng, rate) :
	"""	
	Create an empty sample of 'leng' seconds at sampling rate 'rate'
	"""
	samples = (np.empty(rate*leng)).astype(np.float32)
	return samples

class BigSample(object) :
	def __init__(self, leng, rate) :
		self.leng = leng
		self.rate = rate
		self.arr = create_empty_sample(leng, rate)

	def unclip(self) :
		for i in range(0, len(self.arr)) :
			if(self.arr[i] > .75) :
				self.arr[i] == .75
			elif(self.arr[i] < -.75) :
				self.arr[i] == -.75

	def get_bytes(self) :
		#self.unclip()
		return self.arr



	def add_inplace(self, sample2, position, num_pos) :
		"""
		Add a sample to a bigger sample.
		will check for overrun (and skip if encountered). 
		
		Just adding amplitude values together in a loop here.
		The if-else is to avoid clipping on polyphony
			if there is already nonzero data here, average the 2 amplitudes
			maybe theres a better solution

		"""
		startpoint = int(len(self.arr) / num_pos) * position
		if(startpoint + len(sample2)) > len(self.arr) :
			print("overrun. not adding")
		for i in range (0, len(sample2)) :
			if self.arr[startpoint + i] == 0 :
				self.arr[startpoint + i] += sample2[i]
			else :
				self.arr[startpoint + i] = (self.arr[startpoint + i] + sample2[i]) / 2
