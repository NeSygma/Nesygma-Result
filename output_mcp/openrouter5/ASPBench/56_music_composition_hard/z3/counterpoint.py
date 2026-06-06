from z3 import *

# ============================================================
# Counterpoint Composition: Soprano & Alto, 8 time steps
# Key: C Major
# ============================================================

# Note names and their semitone offsets (within C Major scale)
note_names = ["C", "D", "E", "F", "G", "A", "B"]
note_to_offset = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

# Octave numbers: MIDI = (octave+1)*12 + offset
# C4 = 60, so octave 4 => base = 60
# We'll represent each note as an integer MIDI value.

# Voice ranges (MIDI)
SOPRANO_MIN = 60   # C4
SOPRANO_MAX = 81   # A5
ALTO_MIN = 52      # E3
ALTO_MAX = 72      # C5

# Allowed MIDI notes: C Major scale notes within extended range
# We'll generate all allowed MIDI values
allowed_midi = []
for octave in range(3, 6):  # octave 3 to 5 covers our ranges
    base = (octave + 1) * 12
    for note in ["C", "D", "E", "F", "G", "A", "B"]:
        midi = base + note_to_offset[note]
        allowed_midi.append(midi)

# Filter to unique and within reasonable range
allowed_midi = sorted(set(m for m in allowed_midi if 48 <= m <= 84))

# Create solver
solver = Solver()

# Decision variables: MIDI values for each voice at each time step (1-indexed)
T = 8
soprano = [Int(f"soprano_{t}") for t in range(1, T+1)]
alto = [Int(f"alto_{t}") for t in range(1, T+1)]

# Helper: constrain a variable to allowed MIDI values
def constrain_to_allowed(solver, var, min_val, max_val):
    # var must be one of the allowed_midi values within [min_val, max_val]
    allowed_in_range = [m for m in allowed_midi if min_val <= m <= max_val]
    solver.add(Or([var == m for m in allowed_in_range]))

# Constraint 1 & 2: All notes must be from C Major scale and within voice ranges
for t in range(T):
    constrain_to_allowed(solver, soprano[t], SOPRANO_MIN, SOPRANO_MAX)
    constrain_to_allowed(solver, alto[t], ALTO_MIN, ALTO_MAX)

# Constraint 3: No voice crossing - Soprano must be strictly higher than Alto
for t in range(T):
    solver.add(soprano[t] > alto[t])

# Constraint 4: Melodic leaps not exceeding perfect fifth (7 semitones)
for t in range(T-1):
    solver.add(Abs(soprano[t+1] - soprano[t]) <= 7)
    solver.add(Abs(alto[t+1] - alto[t]) <= 7)

# Constraint 5: Harmonic consonances - allowed harmonic intervals
allowed_intervals = [3, 4, 7, 8, 9, 12, 15, 16]
for t in range(T):
    interval = soprano[t] - alto[t]
    solver.add(Or([interval == i for i in allowed_intervals]))

# Constraint 6: No parallel perfect fifths or parallel octaves
# Parallel perfect fifth: both voices move by same interval, and the harmonic interval is 7 at both steps
# Parallel octave: both voices move by same interval, and the harmonic interval is 12 at both steps
for t in range(T-1):
    sop_move = soprano[t+1] - soprano[t]
    alto_move = alto[t+1] - alto[t]
    # If both voices move by the same amount AND the harmonic interval is a perfect fifth (7) at both steps
    # then it's a parallel fifth
    interval_t = soprano[t] - alto[t]
    interval_t1 = soprano[t+1] - alto[t+1]
    # Parallel fifth: sop_move == alto_move AND interval_t == 7 AND interval_t1 == 7
    solver.add(Not(And(sop_move == alto_move, interval_t == 7, interval_t1 == 7)))
    # Parallel octave: sop_move == alto_move AND interval_t == 12 AND interval_t1 == 12
    solver.add(Not(And(sop_move == alto_move, interval_t == 12, interval_t1 == 12)))

# Constraint 7: Starting notes at time 1
# Alto must be on C4 (MIDI 60)
solver.add(alto[0] == 60)  # C4
# Soprano must be on E4 (MIDI 64) or G4 (MIDI 67)
solver.add(Or(soprano[0] == 64, soprano[0] == 67))  # E4 or G4

# Constraint 8: Cadence at time 7 - both notes must belong to V-chord (G, B, D)
# G = MIDI values: G3=55, G4=67, G5=79
# B = MIDI values: B3=59, B4=71, B5=83
# D = MIDI values: D3=50, D4=62, D5=74
v_chord_midi = [55, 59, 62, 67, 71, 74, 79, 83]  # G, B, D in various octaves
# But within ranges:
# Soprano range C4-A5: 60-81 => G4(67), B4(71), D5(74), G5(79)
# Alto range E3-C5: 52-72 => G3(55), B3(59), D4(62), G4(67), B4(71)
sop_v_allowed = [m for m in v_chord_midi if SOPRANO_MIN <= m <= SOPRANO_MAX]
alto_v_allowed = [m for m in v_chord_midi if ALTO_MIN <= m <= ALTO_MAX]
solver.add(Or([soprano[6] == m for m in sop_v_allowed]))
solver.add(Or([alto[6] == m for m in alto_v_allowed]))

# Constraint 9: Final resolution at time 8 - Soprano on C5 (72), Alto on C4 (60)
solver.add(soprano[7] == 72)  # C5
solver.add(alto[7] == 60)     # C4

# Also ensure the harmonic interval at time 8 is 12 (octave) - which is allowed
# Already covered by constraint 5

# ============================================================
# Solve
# ============================================================
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    
    # Build the composition output
    note_names_rev = {0: "C", 2: "D", 4: "E", 5: "F", 7: "G", 9: "A", 11: "B"}
    
    def midi_to_note(midi_val):
        """Convert MIDI integer to note name with octave."""
        offset = midi_val % 12
        octave = (midi_val // 12) - 1
        note = note_names_rev.get(offset, "?")
        return f"{note}{octave}"
    
    print("composition:")
    for t in range(T):
        s_val = m.eval(soprano[t]).as_long()
        a_val = m.eval(alto[t]).as_long()
        s_note = midi_to_note(s_val)
        a_note = midi_to_note(a_val)
        interval = s_val - a_val
        print(f"  time={t+1}: soprano={s_note} (MIDI {s_val}), alto={a_note} (MIDI {a_val}), interval={interval}")
    
    # Analysis
    print("analysis:")
    print(f"  key: C_major")
    print(f"  num_steps: 8")
    print(f"  voices: ['Soprano', 'Alto']")
    
    # Count violations (should be 0)
    parallel_fifths = 0
    parallel_octaves = 0
    voice_crossings = 0
    for t in range(T-1):
        s_t = m.eval(soprano[t]).as_long()
        a_t = m.eval(alto[t]).as_long()
        s_t1 = m.eval(soprano[t+1]).as_long()
        a_t1 = m.eval(alto[t+1]).as_long()
        sop_move = s_t1 - s_t
        alto_move = a_t1 - a_t
        int_t = s_t - a_t
        int_t1 = s_t1 - a_t1
        if sop_move == alto_move and int_t == 7 and int_t1 == 7:
            parallel_fifths += 1
        if sop_move == alto_move and int_t == 12 and int_t1 == 12:
            parallel_octaves += 1
    for t in range(T):
        s_t = m.eval(soprano[t]).as_long()
        a_t = m.eval(alto[t]).as_long()
        if s_t <= a_t:
            voice_crossings += 1
    
    print(f"  parallel_fifths: {parallel_fifths}")
    print(f"  parallel_octaves: {parallel_octaves}")
    print(f"  voice_crossings: {voice_crossings}")
    print(f"  cadence: authentic")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")