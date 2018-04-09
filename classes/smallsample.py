import numpy as np

class SmallSample :
	"""
	this creates a sample of 1 note. 
	"""
	def __init__(self, frequency, length, articulation='regular', rate=20000) :
		"""ampl_arr = articulations.get(length, None)
		if ampl_arr == None :
			articulations[length] = {}
			articulations[length][articulation] = create_ampl_array(length, rate, .7)
		
		ampl_arr = articulations[length][articulation]
		"""
		self.sample = (np.sin(2*np.pi*np.arange(rate*length)*frequency/rate)).astype(np.float32)
		#samples = np.multiply(samples, ampl_arr)


	def create_attackdecay(start_decibels, end_decibels, length):
		"""
		create a smaller array to control attack/decay in
		the complete amplitude array. 

		It will smoothly ramp decibels which correlated to a 
		logarithmic increase/decrease in amplitude I believe.
		"""

		inc = (start_decibels - end_decibels) * (1 / int(length))
		decibels = start_decibels
		ar = []
		for i in range(0, length) :
			decibels = decibels - inc
			vol = math.pow(10, decibels/20)
			ar.append(vol)
		return ar

	def create_ampl_array(leng, rate, decayfactor) :
		"""
		Create an array to control amplitude in the sample

		This will use a fixed attack length (1/64 of leng * rate). 
			Might rework this part if it matters
		Decay is variable based on decayfactor [0.0 : 1.0)
		I'm using this decay to do different articulations
			i.e. staccato has a decay factor of about .8
		"""
		amplitude_array = []
		high_db= 0
		inaudible_db = -200

		#attack phase
		attack_length = int(leng * rate / 64)
		att = create_attackdecay(inaudible_db, high_db, attack_length)

		#decay phase
		decay_length = int(leng * rate * decayfactor)
		dec = create_attackdecay(high_db, inaudible_db, decay_length)

		for i in range(0, int(leng * rate)) :
			if(i < attack_length) :
				amplitude_array.append(att[i])
			elif(leng * rate - i < decay_length) :
				amplitude_array.append(dec[decay_length - int(leng * rate) + i])
			else :
				amplitude_array.append(math.pow(10, high_db))
		return amplitude_array