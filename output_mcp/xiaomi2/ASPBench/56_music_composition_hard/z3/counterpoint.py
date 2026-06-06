from z3 import *

solver = Solver()

T = 8

# MIDI note arrays for each voice at each time step
soprano = [Int(f'soprano_{t}') for t in range(T)]
alto = [Int(f'alto_{t}') for t in range(T)]

# C Major scale semitone offsets (mod 12)
c_major_offsets = [0, 2, 4, 5, 7, 9, 11]

# V-chord pitch classes: G(7), B(11), D(2)
v_chord_offsets = [7, 11, 2]

# Allowed harmonic intervals (semitones)
allowed_harmonic = [3, 4, 7, 8, 9, 12, 15, 16]

# Helper: note is in C Major scale
def in_c_major(note):
    return Or([note % 12 == off for off in c_major_offsets])

# Helper: note's pitch class is in a set of offsets
def pitch_class_in(note, offsets):
    return Or([note % 12 == off for off in offsets])

# ============================================================
# CONSTRAINT 1: C Major scale
# ============================================================
for t in range(T):
    solver.add(in_c_major(soprano[t]))
    solver.add(in_c_major(alto[t]))

# ============================================================
# CONSTRAINT 2: Voice ranges
# Soprano: C4(60) to A5(81)
# Alto: E3(52) to C5(72)
# ============================================================
for t in range(T):
    solver.add(soprano[t] >= 60, soprano[t] <= 81)
    solver.add(alto[t] >= 52, alto[t] <= 72)

# ============================================================
# CONSTRAINT 3: No voice crossing (soprano strictly higher)
# ============================================================
for t in range(T):
    solver.add(soprano[t] > alto[t])

# ============================================================
# CONSTRAINT 4: Melodic leaps <= perfect fifth (7 semitones)
# ============================================================
for t in range(T - 1):
    solver.add(Abs(soprano[t+1] - soprano[t]) <= 7)
    solver.add(Abs(alto[t+1] - alto[t]) <= 7)

# ============================================================
# CONSTRAINT 5: Harmonic consonances
# ============================================================
for t in range(T):
    interval = soprano[t] - alto[t]
    solver.add(Or([interval == h for h in allowed_harmonic]))

# ============================================================
# CONSTRAINT 6: No parallel perfect fifths or parallel octaves
# Parallel = same harmonic interval type at t and t+1 AND
#            both voices move in the same direction
# ============================================================
for t in range(T - 1):
    harm_t = soprano[t] - alto[t]
    harm_t1 = soprano[t+1] - alto[t+1]
    sop_dir = soprano[t+1] - soprano[t]
    alt_dir = alto[t+1] - alto[t]
    
    same_direction = Or(
        And(sop_dir > 0, alt_dir > 0),
        And(sop_dir < 0, alt_dir < 0)
    )
    
    # No parallel perfect fifths
    solver.add(Not(And(harm_t == 7, harm_t1 == 7, same_direction)))
    
    # No parallel octaves
    solver.add(Not(And(harm_t == 12, harm_t1 == 12, same_direction)))

# ============================================================
# CONSTRAINT 7: Starting notes (time step 1 = index 0)
# Alto on C4(60), Soprano on E4(64) or G4(67)
# ============================================================
solver.add(alto[0] == 60)
solver.add(Or(soprano[0] == 64, soprano[0] == 67))

# ============================================================
# CONSTRAINT 8: Cadence at time 7 (index 6) - V-chord
# Both notes must have pitch class in {G, B, D}
# ============================================================
solver.add(pitch_class_in(soprano[6], v_chord_offsets))
solver.add(pitch_class_in(alto[6], v_chord_offsets))

# ============================================================
# CONSTRAINT 9: Final resolution at time 8 (index 7)
# Soprano on C5(72), Alto on C4(60)
# ============================================================
solver.add(soprano[7] == 72)
solver.add(alto[7] == 60)

# ============================================================
# SOLVE
# ============================================================
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    
    # Note name lookup
    semitone_names = {0:'C', 2:'D', 4:'E', 5:'F', 7:'G', 9:'A', 11:'B'}
    
    def midi_to_name(midi_val):
        octave = (midi_val // 12) - 1
        semitone = midi_val % 12
        return f"{semitone_names[semitone]}{octave}"
    
    # Print composition
    print("\n=== COMPOSITION ===")
    parallel_fifths = 0
    parallel_octaves = 0
    voice_crossings = 0
    
    for t in range(T):
        s_val = m.evaluate(soprano[t]).as_long()
        a_val = m.evaluate(alto[t]).as_long()
        interval = s_val - a_val
        s_name = midi_to_name(s_val)
        a_name = midi_to_name(a_val)
        print(f"Time {t+1}: Soprano={s_name}(MIDI {s_val}), Alto={a_name}(MIDI {a_val}), Harmonic Interval={interval} semitones")
    
    # Verify and count violations
    for t in range(T - 1):
        s_t = m.evaluate(soprano[t]).as_long()
        s_t1 = m.evaluate(soprano[t+1]).as_long()
        a_t = m.evaluate(alto[t]).as_long()
        a_t1 = m.evaluate(alto[t+1]).as_long()
        
        harm_t = s_t - a_t
        harm_t1 = s_t1 - a_t1
        sop_dir = s_t1 - s_t
        alt_dir = a_t1 - a_t
        
        if harm_t == 7 and harm_t1 == 7 and ((sop_dir > 0 and alt_dir > 0) or (sop_dir < 0 and alt_dir < 0)):
            parallel_fifths += 1
        if harm_t == 12 and harm_t1 == 12 and ((sop_dir > 0 and alt_dir > 0) or (sop_dir < 0 and alt_dir < 0)):
            parallel_octaves += 1
    
    for t in range(T):
        s_val = m.evaluate(soprano[t]).as_long()
        a_val = m.evaluate(alto[t]).as_long()
        if s_val <= a_val:
            voice_crossings += 1
    
    print(f"\n=== ANALYSIS ===")
    print(f"key: C_major")
    print(f"num_steps: {T}")
    print(f"voices: ['Soprano', 'Alto']")
    print(f"parallel_fifths: {parallel_fifths}")
    print(f"parallel_octaves: {parallel_octaves}")
    print(f"voice_crossings: {voice_crossings}")
    print(f"cadence: authentic")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")