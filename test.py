from classes.note import Note
from classes.scale import Scale
from classes.measure import Measure

s = Scale(base_frequency=65.4064)

x = Note(32, 3, scale=s)
note, duration = x.to_human_readable()
print(note) #G#(2)
print(duration) #quarter

y = Note(tone="g#", octave=2, notelength="quarter", scale=s)
note, duration = y.to_human_readable()
print(note)
print(duration)

print(s.get_frequency(y.abs_pitch))
print(x.frequency)

G = Note(tone="g", octave=2, notelength="quarter")
A = Note(tone="a", octave=2, notelength="eighth")
m = Measure()
m.add(G, 0)
m.add(A, 8)
print(m.note_dict)


