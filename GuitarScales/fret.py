# (c) 2023 Antonio Rivera
# This code is licensed under GNU General Public license (see LICENSE.txt for details)

import copy



class Fret:
    def __init__(self, note=None, visible=None, root_check=None):
        self.note = note
        self.visible = visible
        self.root_check = root_check

    def get_note(self): return self.note

    def set_note(self, note): self.note = note

    def is_visible(self): return self.visible

    def set_visibility(self, vis): self.visible = vis

    def is_root(self): return self.root_check

    def set_root(self, root): self.root_check = root


class Strings:
    def __init__(self, string_note, note_array, starting_index):
        self.string_note = string_note
        self.string_frets = []  # Instance attribute for each instance of Strings
        self.fill_out_string(note_array, starting_index)

    def fill_out_string(self, note_array, starting_index):
        note_index = starting_index

        for i in range(25):
            if note_index < 12:
                self.string_frets.append(copy.copy(note_array[note_index]))
            else:
                note_index = 0
                self.string_frets.append(copy.copy(note_array[note_index]))
            note_index += 1


a = Fret('A')
ash = Fret('A#')
b = Fret('B')
c = Fret('C')
csh = Fret('C#')
d = Fret('D')
dsh = Fret('D#')
e = Fret('E')
f = Fret('F')
fsh = Fret('F#')
g = Fret('G')
gsh = Fret('G#')

notes_array = [a, ash, b, c, csh, d, dsh, e, f, fsh, g, gsh]

string_e = Strings('E', notes_array, 7)
string_a = Strings('A', notes_array, 0)
string_d = Strings('D', notes_array, 5)
string_g = Strings('G', notes_array, 10)
string_b = Strings('B', notes_array, 2)
string_e1 = Strings('E', notes_array, 7)

fretboard = [string_e, string_a, string_d, string_g, string_b, string_e1]


#for x in fretboard:
    #print(f"start of string {x.string_note}")
    #for y in range(25):
        #print(x.string_frets[y].get_note())
    #print(f"end of string {x.string_note}")
