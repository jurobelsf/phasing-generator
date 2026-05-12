import random
import numpy as np
import pretty_midi  # Used for exporting the results as a MIDI file
import os
from mingus.core import scales, notes  # Used for getting notes from musical scales


tonics = ["C", "D", "E", "F", "G", "A", "B"]
scale_types = ["major", "minor", "dorian"]

# Those are the main scales, to add another one check out the ones available in the mingus library,
# and add them in the get_scale function using the scales module

seq_len = int(input("sequence length: "))
n_candidates = int(input("number of simulations: "))

note_duration = input(
    "note duration "
    "(4=quarter, 8=eighth, 16=sixteenth): "
)

base_octave = 4


def get_scale(tonic, scale_type):

    if scale_type == "major":
        scale_notes = scales.Major(tonic).ascending()

    elif scale_type == "minor":
        scale_notes = scales.NaturalMinor(tonic).ascending()

    elif scale_type == "dorian":
        scale_notes = scales.Dorian(tonic).ascending()

    else:
        return []

    return [
        notes.note_to_int(n) + (base_octave + 1) * 12
        for n in scale_notes
    ]


# =========================
# RANDOM SEQUENCE
# =========================

def random_sequence(scale):

    return [
        random.choice(scale)
        for i in range(seq_len)
    ]


# =========================
# Interval score
# You can play with the scores, for instance, to value more dissonant intervals that create tension
# =========================

interval_score = {

    # unison
    0: 0.6,

    # seconds
    1: 0.55,
    2: 0.6,

    # thirds
    3: 0.65,
    4: 0.6,

    # fourth / fifth
    5: 0.7,
    7: 0.65,

    # sixths
    8: 0.7,
    9: 0.65,

    # sevenths
    10: 0.6,
    11: 0.6,

    # tritone
    6: 0.75
}


# =========================
# MUSICAL METRICS
# =========================

def interval(a, b):

    return abs(a - b) % 12


def consonance(seq1, seq2):

    return np.mean([
        interval_score[interval(a, b)]
        for a, b in zip(seq1, seq2)
    ])


def variety_score(seq):

    return len(set(seq)) / len(seq)


def repetition_penalty(seq):

    return sum(
        1 for i in range(len(seq)-1)
        if seq[i] == seq[i+1]
    ) / len(seq)


def interval_variety(seq):

    intervals = [
        abs(seq[i+1] - seq[i]) % 12
        for i in range(len(seq)-1)
    ]

    return len(set(intervals)) / len(intervals)


# =========================
# TOTAL SCORE
# =========================

def total_score(seq):

    scores = []

    # evaluate all rotations
    for k in range(len(seq)):

        rotated = seq[k:] + seq[:k]

        s = consonance(seq, rotated)

        scores.append(s)

    stability = np.mean(scores)

    variety = variety_score(seq)

    interval_div = interval_variety(seq)

    repetition = repetition_penalty(seq)

    final = (  # Try changing those constants to get new results!!

        0.9 * stability +

        0.7 * variety +

        0.6 * interval_div -

        0.8 * repetition
    )

    return final


# =========================
# MIDI EXPORT
# =========================

def create_phasing_midi(seq, filename):

    midi = pretty_midi.PrettyMIDI()  # this creates a MIDI object

    # We create 2 MIDI instruments
    inst1 = pretty_midi.Instrument(program=0)
    inst2 = pretty_midi.Instrument(program=0)

    seq1 = seq * len(seq)

    seq2 = []

    for i in range(len(seq)):

        rotated = seq[i:] + seq[:i]

        seq2 += rotated

    # convert to MIDI time duration
    if note_duration == "4":
        midi_time = 0.5

    elif note_duration == "8":
        midi_time = 0.25

    elif note_duration == "16":
        midi_time = 0.125

    else:
        midi_time = 0.25

    t = 0.0  # the initial time in the MIDI

    for n1, n2 in zip(seq1, seq2):

        inst1.notes.append(
            pretty_midi.Note(
                velocity=90,
                pitch=n1,
                start=t,
                end=t + midi_time
            )
        )

        inst2.notes.append(
            pretty_midi.Note(
                velocity=90,
                pitch=n2,
                start=t,
                end=t + midi_time
            )
        )

        t += midi_time

    midi.instruments.append(inst1)
    midi.instruments.append(inst2)

    # the .write method is the one that actually creates the .mid file
    midi.write(filename)


# =========================
# MIDI TO STRING
# =========================

def midi_to_string(seq):

    note_names = []

    duration = note_duration

    for n in seq:

        # remove octave number
        note = pretty_midi.note_number_to_name(n)[:-1]

        # add rhythmic duration
        note = note + duration

        note_names.append(note)

    return " ".join(note_names)


# =========================
# USER INPUT
# =========================

mode = input(
    "Choose mode: (1) for manual scale, or (2) for random search: "
)

best_score = -np.inf

best_seq = None

best_scale = None


# =========================
# MODE 1 - User scale
# =========================

if mode == "1":

    tonic = input(
        "enter tonic (C, D, E, F, G, A, B): "
    )

    scale_type = input(
        "enter scale (major, minor, dorian): "
    )

    scale = get_scale(tonic, scale_type)

    for i in range(n_candidates):

        seq = random_sequence(scale)

        score = total_score(seq)

        if score > best_score:

            best_score = score

            best_seq = seq

            best_scale = (tonic, scale_type)


# =========================
# MODE 2 - Random search
# =========================

else:

    for i in range(n_candidates):

        tonic = random.choice(tonics)

        scale_type = random.choice(scale_types)

        scale = get_scale(tonic, scale_type)

        seq = random_sequence(scale)

        score = total_score(seq)

        if score > best_score:

            best_score = score

            best_seq = seq

            best_scale = (tonic, scale_type)


# =========================
# OUTPUT
# =========================

print("\nbest result\n")

print("scale:", best_scale)

print("MIDI sequence:", best_seq)

print("string sequence:", midi_to_string(best_seq))

print("saving in:", os.getcwd())  # See where your file is being saved


# =========================
# EXPORT MIDI
# =========================

create_phasing_midi(
    best_seq,
    "coral.mid"
)


# =========================
# SUMMARY STATISTICS
# =========================

scores = []

for i in range(n_candidates):

    tonic = random.choice(tonics)

    scale_type = random.choice(scale_types)

    montecarlo_scale = get_scale(tonic, scale_type)

    seq = random_sequence(montecarlo_scale)

    result = total_score(seq)

    scores.append(result)



scores = np.array(scores)

mean_score = np.mean(scores)

median_score = np.median(scores)

std_score = np.std(scores)

max_score = np.max(scores)

min_score = np.min(scores)

# Pearson moment skewness
skewness = np.mean(
    ((scores - mean_score) / std_score) ** 3
)

print("\nSUMMARY STATISTICS\n")

print("Mean score:", round(mean_score, 4))

print("Median score:", round(median_score, 4))

print("Standard deviation:", round(std_score, 4))

print("Skewness:", round(skewness, 4))

print("Maximum score:", round(max_score, 4))

print("Minimum score:", round(min_score, 4))


# =========================
# SCORE DISTRIBUTION
# =========================

plt.figure(figsize=(10, 6))

plt.hist(
    scores,
    bins = round(np.sqrt(n_candidates)), #for better visualization
    color="#5c60aa",
    alpha=0.85
)

# mean line
plt.axvline(
    mean_score,
    color="#9df57a",
    linestyle="-",
    linewidth=3,
    label=f"Mean = {mean_score:.4f}"
)

# median line
plt.axvline(
    median_score,
    color="#9df57a",
    linestyle="--",
    linewidth=3,
    label=f"Median = {median_score:.4f}"
)

plt.xlabel("Score")

plt.ylabel("Frequency")

plt.title("Distribution of Generated Scores")

plt.legend()

plt.show()
