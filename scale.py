# (c) 2023 Antonio Rivera
# This code is licensed under GNU General Public license (see LICENSE.txt for details)

class Scale:
    def __init__(self, name, intervals=None):
        self.intervals = intervals
        self.name = name

    def set_interval(self, intervals):
        self.intervals = intervals

    def get_interval(self):
        return self.intervals


def get_scale_list_major():
    return major_scales


def get_scale_list_minor():
    return minor_scales


m_scales_name = ['Major Scale/Ionian', 'Major Pentatonic', 'Harmonic Major', 'Major Bebop',
                 'Major Blues', 'Mixolydian', 'Lydian']
min_scales_name = ['Minor Scale/Aeolian', 'Minor Pentatonic', 'Harmonic Minor', 'Melodic Minor',
                   'Minor Bebop', 'Minor Blues', 'Dorian', 'Phrygian', 'Locrian']

major = Scale(m_scales_name[0], [2, 2, 1, 2, 2, 2, 1])
pent = Scale(m_scales_name[1], [2, 2, 3, 2, 3])
harm = Scale(m_scales_name[2], [2, 2, 1, 2, 1, 3, 1])
bebop = Scale(m_scales_name[3], [2, 2, 1, 2, 2, 2, 1, 1])
blue = Scale(m_scales_name[4], [2, 2, 1, 2, 3, 2])
mix = Scale(m_scales_name[5], [2, 2, 1, 2, 2, 1, 2])
lyd = Scale(m_scales_name[6], [2, 2, 2, 1, 2, 2, 1])

minor = Scale(min_scales_name[0], [2, 1, 2, 2, 1, 2, 2])
m_pent = Scale(min_scales_name[1], [3, 2, 2, 3, 2])
m_harm = Scale(min_scales_name[2], [2, 1, 2, 2, 1, 3, 1])
m_mel = Scale(min_scales_name[3], [2, 1, 2, 2, 2, 2, 1])
m_bebop = Scale(min_scales_name[4], [2, 1, 1, 1, 2, 2, 1, 2])
m_blue = Scale(min_scales_name[5], [3, 2, 1, 1, 3, 2])
dor = Scale(min_scales_name[6], [2, 1, 2, 2, 2, 1, 2])
phry = Scale(min_scales_name[7], [1, 2, 2, 2, 1, 2, 2])
loc = Scale(min_scales_name[8], [1, 2, 2, 1, 2, 2, 2])

major_scales = [major, pent, harm, bebop, blue, mix, lyd]
minor_scales = [minor, m_pent, m_harm, m_mel, m_bebop, m_blue, dor, phry, loc]