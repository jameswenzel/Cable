from constants import Note, Quality, Interval, Extended, Degree, DEGREE_MAP


def is_major(chord_name):
    '''Guesses a chord is major or minor by its capitalization'''
    return chord_name[0].isupper()


def to_chroma(pitch):
    '''Convert a numeric pitch in any octave to a chroma between 0-12'''
    return pitch % 12


def sharp_flat_delta(note_name):
    if note_name.endswith('b'):
        return -1
    elif note_name.endswith('#'):
        return 1
    elif note_name.endswith('bb'):
        return -2
    elif note_name.endswith('x'):
        return 2
    return 0


def get_intervals(root, quality, extended, *add):
    intervals = get_quality_intervals(quality)
    extended_intervals = get_extended_intervals(quality, extended)
    return bag_intervals(intervals, extended_intervals, add)


def get_relative_interval(root, relative_note, interval, octave=None):
    # get octave between root and open string
    target_note = root + interval
    return relative_note.interval_to(target_note)


def bag_intervals(quality, extended, add):
    '''Return a dict of degrees to intervals
    Ensures that extended notes override quality notes, and that added notes
    override both.
    '''
    intervals = {}
    for interval in quality:
        intervals[DEGREE_MAP[interval]] = interval
    for interval in extended:
        intervals[DEGREE_MAP[interval]] = interval
    for interval in add:
        intervals[DEGREE_MAP[interval]] = interval
    return intervals.values()


def get_quality_intervals(quality):
    if quality is None:
        return []
    return QUALITY_NOTE_MAP[quality]


def get_extended_intervals(quality, extended):
    '''Get the extended notes included in a chord extension'''
    if extended is None or (extended == Extended.E7 and
                            quality in {Quality.DIM, Quality.DOM,
                                        Quality.MIN_MAJ}):
        return []
    if extended == Extended.E7:
        if quality in (Quality.MIN, Quality.HALF_DIM):
            return [Interval.MINOR_SEVENTH]
        elif (quality == Quality.MAJ):
            return [Interval.MAJOR_SEVENTH]
    elif quality in (Quality.MAJ, Quality.MIN_MAJ):
        notes = [Interval.MAJOR_SEVENTH]
    else:
        notes = [Interval.MINOR_SEVENTH]
    extended_notes = EXTENDED_NOTE_MAP[extended]
    return notes + extended_notes


def score_difficulty(fingering):
    # TODO: account for barre chords
    return len(set(filter(bool, fingering)))


def get_intervals_from_fingering(tuning, root, fingering):
    filtered = filter(lambda x: x[1] != Note.X, zip(tuning, fingering))
    notes = map(lambda t: t[0] + Interval(t[1] % 12), filtered)
    return list(map(lambda note: root.interval_to(note), notes))


QUALITY_NOTE_MAP = {
    Quality.HALF_DIM: [Interval.ROOT, Interval.MINOR_THIRD,
                       Interval.DIMINISHED_FIFTH],
    Quality.MIN: [Interval.ROOT, Interval.MINOR_THIRD,
                  Interval.PERFECT_FIFTH],
    Quality.MAJ: [Interval.ROOT, Interval.MAJOR_THIRD,
                  Interval.PERFECT_FIFTH],
    Quality.SUS2: [Interval.ROOT, Interval.MAJOR_SECOND,
                   Interval.PERFECT_FIFTH],
    Quality.SUSb2: [Interval.ROOT, Interval.MINOR_SECOND,
                    Interval.PERFECT_FIFTH],
    Quality.SUSs2: [Interval.ROOT, Interval.AUGMENTED_SECOND,
                    Interval.PERFECT_FIFTH],
    Quality.SUS4: [Interval.ROOT, Interval.PERFECT_FOURTH,
                   Interval.PERFECT_FIFTH],
    Quality.SUSb4: [Interval.ROOT, Interval.DIMINISHED_FOURTH,
                    Interval.PERFECT_FIFTH],
    Quality.SUSs4: [Interval.ROOT, Interval.AUGMENTED_FOURTH,
                    Interval.PERFECT_FIFTH],
    Quality.AUG: [Interval.ROOT, Interval.MAJOR_THIRD,
                  Interval.AUGMENTED_FIFTH],
    Quality.DIM: [Interval.ROOT, Interval.MINOR_THIRD,
                  Interval.DIMINISHED_FIFTH, Interval.DIMINISHED_SEVENTH],
    Quality.DOM: [Interval.ROOT, Interval.MAJOR_THIRD,
                  Interval.PERFECT_FIFTH, Interval.MINOR_SEVENTH],
    Quality.MIN_MAJ: [Interval.ROOT, Interval.MINOR_THIRD,
                      Interval.PERFECT_FIFTH, Interval.MAJOR_SEVENTH]
}

# TODO: Define priorities
EXTENDED_NOTE_MAP = {
    Extended.Eb9: [Interval.MINOR_SECOND],
    Extended.E9: [Interval.MAJOR_SECOND],
    Extended.Es9: [Interval.AUGMENTED_SECOND],
    Extended.Eb11: [Interval.MAJOR_SECOND, Interval.DIMINISHED_FOURTH],
    Extended.E11: [Interval.MAJOR_SECOND, Interval.PERFECT_FOURTH],
    Extended.Es11: [Interval.MAJOR_SECOND, Interval.AUGMENTED_FOURTH],
    Extended.Eb13: [Interval.MAJOR_SECOND, Interval.PERFECT_FOURTH,
                    Interval.MINOR_SIXTH],
    Extended.E13: [Interval.MAJOR_SECOND,
                   Interval.PERFECT_FOURTH, Interval.MAJOR_SIXTH],
    Extended.Es13: [Interval.MAJOR_SECOND,
                    Interval.PERFECT_FOURTH, Interval.AUGMENTED_SIXTH]
}


def get_inverted_root(root, inversion):
    pass
