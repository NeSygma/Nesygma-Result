from z3 import *

solver = Solver()

# MIDI note definitions
C4, D4, E4, F4, G4, A4, B4 = 60, 62, 64, 65, 67, 69, 71
C5, D5, E5, F5, G5, A5, B5 = 72, 74, 76, 77, 79, 81, 83
C3, D3, E3, F3, G3, A3, B3 = 48, 50, 52, 53, 55, 57, 59

# C Major scale semitone offsets
c_major_offsets = [0, 2, 4, 5, 7, 9, 11]

# Soprano and Alto MIDI variables for time 1..8
sop = [Int(f'sop_{t}') for t in range(1, 9)]
alto = [Int(f'alto_{t}') for t in range(1, 9)]

# Allowed harmonic intervals
allowed_intervals = [3, 4, 7, 8, 9, 12, 15, 16]

# ============ CONSTRAINTS ============

# 1. C Major scale: note % 12 must be in {0, 2, 4, 5, 7, 9, 11}
for t in range(8):
    solver.add(Or([sop[t] % 12 == off for off in c_major_offsets]))
    solver.add(Or([alto[t] % 12 == off for off in c_major_offsets]))

# 2. Voice ranges
for t in range(8):
    solver.add(sop[t] >= 60, sop[t] <= 81)  # C4 to A5
    solver.add(alto[t] >= 52, alto[t] <= 72)  # E3 to C5

# 3. No voice crossing: Soprano must always be strictly higher than Alto
for t in range(8):
    solver.add(sop[t] > alto[t])

# 4. Melodic leaps: consecutive notes in each voice <= 7 semitones (perfect fifth)
for t in range(7):
    solver.add(Abs(sop[t+1] - sop[t]) <= 7)
    solver.add(Abs(alto[t+1] - alto[t]) <= 7)

# 5. Harmonic consonances: allowed intervals only
for t in range(8):
    interval = sop[t] - alto[t]
    solver.add(Or([interval == inv for inv in allowed_intervals]))

# 6. No parallel perfect fifths or parallel octaves between consecutive time steps
for t in range(7):
    # Forbid parallel perfect fifths (interval 7 at both t and t+1)
    solver.add(Not(And(sop[t] - alto[t] == 7, sop[t+1] - alto[t+1] == 7)))
    # Forbid parallel octaves (interval 12 at both t and t+1)
    solver.add(Not(And(sop[t] - alto[t] == 12, sop[t+1] - alto[t+1] == 12)))

# 7. Starting notes at time 1 (index 0)
solver.add(alto[0] == C4)   # Alto on C4
solver.add(Or(sop[0] == E4, sop[0] == G4))  # Soprano on E4 or G4

# 8. Cadence at time 7 (index 6): both notes from V-chord (G, B, D)
# V-chord notes in Soprano range (C4-A5): D4(62), G4(67), B4(71), D5(74), G5(79)
# V-chord notes in Alto range (E3-C5): G3(55), B3(59), D4(62), G4(67), B4(71)
v_chord_sop = [62, 67, 71, 74, 79]
v_chord_alto = [55, 59, 62, 67, 71]
solver.add(Or([sop[6] == n for n in v_chord_sop]))
solver.add(Or([alto[6] == n for n in v_chord_alto]))

# 9. Final resolution at time 8 (index 7): Soprano on C5, Alto on C4
solver.add(sop[7] == C5)  # C5 = 72
solver.add(alto[7] == C4)  # C4 = 60

# ============ SOLVE ============
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    
    def note_name(midi_val):
        notes_map = {0: 'C', 2: 'D', 4: 'E', 5: 'F', 7: 'G', 9: 'A', 11: 'B'}
        octave = midi_val // 12 - 1
        semitone = midi_val % 12
        return f"{notes_map[semitone]}{octave}"
    
    print("composition: [")
    for t in range(8):
        s_val = m[sop[t]].as_long()
        a_val = m[alto[t]].as_long()
        sn = note_name(s_val)
        an = note_name(a_val)
        interval = s_val - a_val
        comma = "," if t < 7 else ""
        print(f"  {{'time': {t+1}, 'soprano_note': '{sn}', 'alto_note': '{an}', 'harmonic_interval_semitones': {interval}}}{comma}")
    print("]")
    
    print("analysis: {")
    print("  'key': 'C_major',")
    print("  'num_steps': 8,")
    print("  'voices': ['Soprano', 'Alto'],")
    print("  'parallel_fifths': 0,")
    print("  'parallel_octaves': 0,")
    print("  'voice_crossings': 0,")
    print("  'cadence': 'authentic'")
    print("}")
else:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (refine required)")