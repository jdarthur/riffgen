import pyaudio
import wave
import sys
import numpy as np
import math
import time
import sounddevice as sd
import math
import random

"""
DONE: 
	bing
	variable length
TODO:
	multibing
	different tone for notes
		C7, A4, whatever...
	different length for notes
		quarter, eighth, whole, whatever
	smooth bing dropoff
	legato, staccato 
	differ

"""


def createSample(leng, rate, f = 440) :
	fs = rate     # sampling rate, Hz, must be integer
	duration = leng  # in seconds, may be float

	# generate samples, note conversion to float32 array
	samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
	decibels = 0
	negdec = 200
	for i in range(0, len(samples)) :
		#inc = ((vol*(duration << 6))/fs)
		inc =  negdec * (1 / (leng * fs))
		decibels = decibels - inc
		#print(decibels)
		#print(1 - inc)
		vol = math.pow(10, decibels/20)
		samples[i] = samples[i] * vol
		if( i % 200 == 0) : 
			pass
			#print("vol: " + str(vol))
			#print(decibels)
		#print(vol)
	return samples

frequencies = { 
'C'   :	261.626,
'C#'  : 277.183,
'D'   :	293.665,
'D#'  : 311.127,
'E'   :	329.628,
'F'   :	349.228,
'F#'  :	369.994,
'G'   :	391.995,
'G#'  : 415.305,
'A'   :	440,
'A#'  :	466.164,
'B'   :	493.883,
'rest' : 0,  
}
rate = 20000

def createNote(note, octave, leng=1, rate=rate) :
	f = frequencies[note.upper()]
	adjustfactor = math.pow(2, octave - 4)
	f = f * adjustfactor
	note = createSample(leng, int(rate), f)
	return note


def create_empty_sample(leng, rate) :
	samples = (np.empty(rate*leng)).astype(np.float32)
	return samples

def add_sample(sample1, sample2, position, num_pos, rate=rate) :
	rets = sample1
	startpoint = int(len(sample1) / num_pos) * position
	if(startpoint + len(sample2)) > len(sample1) :
		print("overrun. not adding")
		return rets
	for i in range (0, len(sample2)) :
		if rets[startpoint + i] == 0 :
			rets[startpoint + i] += sample2[i]
		else :
			rets[startpoint + i] = (rets[startpoint + i] + sample2[i]) / 2
		
		"""
		rets[startpoint + i] += sample2[i]
		if rets[startpoint + i] > .55 :
			rets[startpoint + i] = .55
		"""

	return rets


def rand_sequence(items, num_positions) :
	choices = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
	weights = [ 10,  10,  10,  10,  10,  10,  10]
	seq = []
	for i in range(0, items) :
		note = random.choice(choices)
		#print(note)
		pos = random.randint(0, num_positions)
		#print(pos)
		seq.append((note, 4, pos))
	return seq




timer = time.time()
#sequence = [("c", 4) 'd', 'e', 'f', 'g', 'a', 'b', 'c']
sequence = [("c", 4), ('d', 4), ("e", 4), ('f', 4),
			("g", 4), ('a', 4), ("b", 4), ('c', 5),
]
i = 0
seq2 = []
for note, octave in sequence :
	seq2.append((note, octave, i))
	i += 2
seq2.append(("c", 4, 2))
seq2.append(("c", 4, 4))
seq2.append(("c", 4, 6))
seq2.append(("c", 4, 7))


randseq = rand_sequence(12, 16)


beats = 4
positions = beats * 8
big = create_empty_sample(beats, rate)

samples = []
for note, octave, pos in randseq :
	n = createNote(note, octave, leng=.5), pos
	samples.append(n)

for samp, pos in samples :
	big = add_sample(big, samp, pos, positions)

t2 = time.time() - timer
print("runtime: {0}s".format(t2))

sd.play(big, rate, blocking=True)
