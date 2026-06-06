from z3 import *

# Solver configuration
BENCHMARK_MODE = True

# Define constants
allowed_offsets = [0,2,4,5,7,9,11]  # semitone offsets from C
# Compute allowed MIDI notes for soprano and alto based on ranges
soprano_allowed = [m for m in range(60,82) if (m-60)%12 in allowed_offsets]
# 60-81 inclusive
alto_allowed = [m for m in range(52,73) if (m-48)%12 in allowed_offsets]  # 48 is C3
# Allowed harmonic intervals (in semitones)
allowed_intervals = [3,4,7,8,9,12,15,16]
# V-chord notes for soprano and alto
# V-chord notes: G (7), B (11), D (2)
# Compute all MIDI notes for these within ranges
v_chord_offsets = [7,11,2]
# Soprano V-chord notes within 60-81
soprano_v_chord = [m for m in soprano_allowed if (m-60)%12 in v_chord_offsets]
# Alto V-chord notes within 52-72
alto_v_chord = [m for m in alto_allowed if (m-48)%12 in v_chord_offsets]

# Create solver
solver = Solver()

# Create variables for 8 time steps
soprano = [Int(f'soprano_{t}') for t in range(8)]
alto = [Int(f'alto_{t}') for t in range(8)]

# Add constraints for each time step
for t in range(8):
    # Notes must be from allowed sets
    solver.add(Or([soprano[t] == val for val in soprano_allowed]))
    solver.add(Or([alto[t] == val for val in alto_allowed]))
    # Voice crossing
    solver.add(soprano[t] > alto[t])
    # Harmonic consonance
    solver.add(Or([soprano[t] - alto[t] == d for d in allowed_intervals]))
    if t > 0:
        # Melodic leaps <= perfect fifth (7 semitones)
        solver.add(Abs(soprano[t] - soprano[t-1]) <= 7)
        solver.add(Abs(alto[t] - alto[t-1]) <= 7)
        # No parallel perfect fifths or octaves
        solver.add(Not(And(soprano[t-1] - alto[t-1] == 7, soprano[t] - alto[t] == 7)))
        solver.add(Not(And(soprano[t-1] - alto[t-1] == 12, soprano[t] - alto[t] == 12)))

# Starting notes (time 1 -> index 0)
solver.add(alto[0] == 60)  # C4
solver.add(Or(soprano[0] == 64, soprano[0] == 67))  # E4 or G4

# Cadence at time 7 (index 6)
solver.add(Or([soprano[6] == val for val in soprano_v_chord]))
solver.add(Or([alto[6] == val for val in alto_v_chord]))
# Interval at time 7 must not be an octave to avoid parallel octave with final resolution
solver.add(soprano[6] - alto[6] != 12)

# Final resolution at time 8 (index 7)
solver.add(soprano[7] == 72)  # C5
solver.add(alto[7] == 60)    # C4

# Check solver
result = solver.check()

# Helper to convert MIDI to note string
note_names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

def midi_to_note(midi):
    octave = midi // 12 - 1
    name = note_names[midi % 12]
    return f"{name}{octave}"

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Composition output
    print("composition:")
    for t in range(8):
        s_val = model[soprano[t]].as_long()
        a_val = model[alto[t]].as_long()
        interval = s_val - a_val
        print(f"time:{t+1} soprano_note:{midi_to_note(s_val)} alto_note:{midi_to_note(a_val)} harmonic_interval_semitones:{interval}")
    # Analysis
    # Compute counts
    parallel_fifths = 0
    parallel_octaves = 0
    voice_crossings = 0
    for t in range(1,8):
        s_prev = model[soprano[t-1]].as_long()
        a_prev = model[alto[t-1]].as_long()
        s_curr = model[soprano[t]].as_long()
        a_curr = model[alto[t]].as_long()
        if s_prev <= a_prev:
            voice_crossings += 1
        if (s_prev - a_prev == 7) and (s_curr - a_curr == 7):
            parallel_fifths += 1
        if (s_prev - a_prev == 12) and (s_curr - a_curr == 12):
            parallel_octaves += 1
    print("analysis:")
    print("key:C_major")
    print("num_steps:8")
    print("voices:[Soprano, Alto]")
    print(f"parallel_fifths:{parallel_fifths}")
    print(f"parallel_octaves:{parallel_octaves}")
    print(f"voice_crossings:{voice_crossings}")
    print("cadence:authentic")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")