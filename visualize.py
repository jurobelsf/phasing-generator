"""
Optional visualization module.

Requires:

pip install musicntwrk music21 pygame

For score rendering you may also need MuseScore:
https://musescore.org

Installing all of this can be a bit cumbersome, so I recommend watching: https://www.youtube.com/watch?v=ylLOn-QH0gQ
"""

from musicntwrk.comptools.displayNotes import displayNotes
from musicntwrk.comptools.music import NoteSeq


def phasing_sequences(seq):

    seq1 = NoteSeq(seq)

    seq2 = NoteSeq(seq)

    seq1_final = seq1 * len(seq1)

    seq2_final = NoteSeq()

    for i in range(len(seq2)):

        seq2_final += seq2.rotate(i)

    return seq1_final, seq2_final


def visualize(seq):

    s1, s2 = phasing_sequences(seq)

    displayNotes(
        [s1, s2],
        show='midi'
    )

visualize("") #Insert here the sequence in string notation

#Example:
#visualize("C8 D A# C D# G D F A C G D#")
