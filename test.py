import mido
import os

#path = os.path.abspath(mido.__file__)
#print (path)


from mido import MidiFile
from majorChords import RTNote


mid = MidiFile("Cmaj-1-bar-120bpm.mid", clip=True)
print(mid)


for msg in mid.tracks[0]:
    print msg


'''
for msg in mid.tracks[0]:
    print msg
    #print msg.__dict__
    print dir(msg)
    if (hasattr(msg, 'note')):
        print msg.note
    #print type(msg.type)
'''


'''
notes = RTNote(60, '127', '500')
print notes.value
'''

