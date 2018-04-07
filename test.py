from classes.note import Note
from classes.scale import Scale

x = Note(32, 3)
note, duration = x.to_human_readable()
print(note) #G#(2)
print(duration) #quarter

y = Note(tone="g#", octave=2, notelength="quarter")
note, duration = y.to_human_readable()
print(note) #G#(2)
print(duration) #quarter

s = Scale(base_frequency=65.4064)
print(s.get_frequency(y.abs_pitch))