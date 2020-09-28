import mido
import os, shutil
import re
from collections import namedtuple
from mido import Message, MetaMessage, MidiFile, MidiTrack



DESTINATION_DIRECTORY = '/Users/mac/Desktop/Chords/12 - B major-G# minor/4 notes'

os.chdir(DESTINATION_DIRECTORY)



Note = namedtuple('Note', ['value', 'velocity', 'position_in_sec', 'duration'])
RTNote = namedtuple('RTNote', ['value', 'velocity', 'duration'])


KeyNote = {'major':[0,5,7], 'minor':[2,4,9]}

chord_name_index = ('C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B')

degrees = {'b5':4.5, '5':5, '#5':5.5, '6':6, '7':6.5, '7+':7, 'b9':1.5, '9':2, '#9':2.5, 'b11':3.5, '11':4, '#11':4.5 ,'b13':5.5, '13':6}


def note_number_to_chord_name(note):
    chord_name = chord_name_index[note % 12]
    chord_octave = (note / 12) - 1

    return chord_name


def add_notes(track, notes, sec_per_tick):
    #times_in_ticks = [n.position_in_sec / sec_per_tick for n in notes] #genuine
    times_in_ticks = [0 for n in notes]

    for ix, note in enumerate(notes):
        time_delta_in_ticks = int(
            times_in_ticks[ix] - (times_in_ticks[ix-1] if ix > 0 else 0))
        track.append(
            Message(
                'note_on',
                note=note.value,
                velocity=note.velocity,
                time=max(time_delta_in_ticks - note.duration, 0)
            )
        )
        track.append(
            Message(
                'note_off',
                note=note.value,
                velocity=note.velocity,
                time=note.duration
            )
        )

def set_chord(track, notes, sec_per_tick):
    #times_in_ticks = [n.position_in_sec / sec_per_tick for n in notes] #genuine
    times_in_ticks = [0 for n in notes]


    for ix, note in enumerate(notes):
        time_delta_in_ticks = int(
            times_in_ticks[ix] - (times_in_ticks[ix-1] if ix > 0 else 0))
        track.append(
            Message(
                'note_on',
                note=note.value,
                velocity=note.velocity,
                time=max(time_delta_in_ticks - note.duration, 0)
            )
        )

    for note in notes:
        track.append(
            Message(
                'note_off',
                note=note.value,
                velocity=note.velocity,
                time=note.duration
            )
        )


def create_chord(root):

    root = root
    bpm = 120
    n = range(3)


    note = [RTNote()]

    ''' major chords '''
    for i in [0, 5, 7]: # primary numbers
        root_note = root + i
        mediant_note = root+i+4 if i>2 else root+i+3

        notes = [RTNote(root+i, 127, one_bar_duration), RTNote(root+i+4, 127, 0), RTNote(root+i+7, 127, 0)]
        create_midi_file_with_notes(note_number_to_chord_name(root_note), notes, bpm)

    ''' minor chords '''
    for i in [2, 4, 9]:
        root_note = root + i
        notes = [RTNote(root+i, 127, one_bar_duration), RTNote(root+i+3, 127, 0), RTNote(root+i+7, 127, 0)]
        create_midi_file_with_notes(note_number_to_chord_name(root_note) + "m", notes, bpm)


def create_major_chords(root):

    major_chords = [[RTNote(root+i, 127, one_bar_duration), RTNote(root+i+4, 127, 0), RTNote(root+i+7, 127, 0)]
              for i in (0,5,7)]

    return major_chords


def create_minor_chords(root):

    minor_chords = [[RTNote(root+i, 127, one_bar_duration), RTNote(root+i+3, 127, 0), RTNote(root+i+7, 127, 0)]
              for i in (2,4,9)]

    return minor_chords


def root_chord(root, mediant):          #todo *args

    mediant = (4 if mediant == 'major' else 3)
    crd = mediant
    d = []
    octave = 0

    #note = root + int((degrees[note] - 1) * 2) - offset + (octave * 12)

    chords = [[RTNote(root, 127, one_bar_duration), RTNote(root+i+mediant, 127, 0), RTNote(root+i+7, 127, 0)]]
    #for i in (0 , 5, 7)
    return chords


#todo use with *args and **keys     !!!!!!!!!!!!

def create_chords(chords, notes): #[60, chords, [7,9,11]]       #todo use with *args

    '''
    :param root:
    :param chords:
    :param notes:
    :param cmb:
    :return:

    sus2, sus4, b5, #5, 7+ ?
    '''

    mod_chords = []

    for chord in chords:

        root = chord[0].value
        cmb = notes

        #todo remove invalid combinations - remove all notes till this note
        ''' by the last note '''

        for note in cmb:

            # if note exist in chord remove it

            cd = int(re.findall(r"\d+", note)[0])        #todo extract value from list without [0] ?
            octave = 1 if cd > 7 else 0
            offset = (1 if (cd!=2 and cd!=9) else 0)

            note = root + int((degrees[note] - 1) * 2) - offset + (octave * 12)
            #note = root + (int((degrees[j] - 1) * 2) - offset) + (octave * 12)

            #todo object for chords - dict, nametuple ?
            #todo function for name

            new_chord = [n for n in chord]
            new_chord.append(RTNote(note , 127, 0))

            mod_chords.append(new_chord)

            #mod_chords[name] = new_chord
            new_chord = []

    #chords = chords + mod_chords
    return mod_chords


def get_chord_name(chord, name):

    #todo check for chord's num of notes

    name = '{}{}{}({})'.format(note_number_to_chord_name(root_note),key, d, j)
    return name


def create_midi_file_with_notes(filename, notes, bpm):

    with MidiFile() as midifile:
        track = MidiTrack()
        midifile.tracks.append(track)

        #track.append(Message('program_change', program=12, time=0))

        tempo = int((60.0 / bpm) * 1000000)
        track.append(MetaMessage('set_tempo', tempo=tempo))

        sec_per_tick = tempo / 1000000.0 / midifile.ticks_per_beat
        #add_notes(track, notes, sec_per_tick) # original

        set_chord(track, notes, sec_per_tick)
        midifile.save('{}.mid'.format(filename))

        #shutil.move(src_folder, dst_folder)



if __name__ == '__main__':

    bpm = 120
    time_delta = 0
    one_bar_duration = int(((60.0 / bpm) * 1000) * 4) - time_delta

    root = 71

    major_chords = create_major_chords(root)
    #create_4_note_chord(major_chords)

    minor_chords = create_minor_chords(root)

    # create_chords(root, 2th, 3th, 4th, 5th, 6th, 7th)     [b6, 6, 7, 7+, b9, 9, 9+, b11, 11, 11+, b13, 13]
    '''
    the list is being updated by removing its preceded degress which are included in the chord

    4 notes - 7, 7+
    5 to 6 notes - b9, 9 , #9, b11, 11 , #11, b13, 13
    6 notes - b11, 11 , #11, b13, 13
    7 notes - b13, 13

    '''


    chords = major_chords + minor_chords

    #major_chords = [[RTNote(root, 127, one_bar_duration), RTNote(root+4, 127, 0)] ]

    #minor_chords = [[RTNote(root, 127, one_bar_duration), RTNote(root+3, 127, 0)]]

    dim_chords = [[RTNote(root+11, 127, one_bar_duration), RTNote(root+11+3, 127, 0)]]


    chords = dim_chords

    for i in ['b5', '7']:
        chords = create_chords(chords, [i])


    for chord in chords:
        key = ("" if chord[1].value - chord[0].value == 4 else "m")

        name = '{}{}7b5'.format(note_number_to_chord_name(chord[0].value), key)  #todo name convention - Chord(x,y)
        create_midi_file_with_notes(name, chord, bpm)

    '''
    for chord in chords.iteritems():
        name = '{}11'.format(note_number_to_chord_name(chord[1][0].value))
        create_midi_file_with_notes(name, chord[1], bpm)
    '''

    '''
    chords = create_chords(major_chords, ['7', '9'], ['11'])    #['#9', 'b11', '11', '#11']
    for chord in chords.iteritems():
        create_midi_file_with_notes(chord[0], chord[1], bpm)



    chords = create_chords(minor_chords, '11')


    for chord in chords.iteritems():
        create_midi_file_with_notes(chord[0], chord[1], bpm)
    '''

    '''
    mid = MidiFile("Cmaj.mid", clip=True)

    for msg in mid.tracks[0]:
        print msg
    '''


#todo 3 chords notes add sus2, sus4, C+, Cdim etc'

#todo duration of one bar - by canceling bpm parameter ?
#todo ticks
#todo frame rate ?


#todo execute with or without main()
#todo abs.path ???

#todo what are polychords / polyvoicing ???
#todo what is yield and its uses