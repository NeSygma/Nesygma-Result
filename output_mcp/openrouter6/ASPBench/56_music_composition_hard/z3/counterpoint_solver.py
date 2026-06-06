from z3 import *

# Problem parameters
time_steps = 8
voices = ["soprano", "alto"]

# Define allowed MIDI numbers for C Major scale in each voice's range
# Soprano: C4 (60) to A5 (81)
soprano_allowed = []
for octave in range(4, 6):  # octaves 4 and 5
    for note, offset in [("C",0), ("D",2), ("E",4), ("F",5), ("G",7), ("A",9), ("B",11)]:
        midi = 60 + (octave-4)*12 + offset
        if 60 <= midi <= 81:
            soprano_allowed.append(midi)

# Alto: E3 (52) to C5 (72)
alto_allowed = []
for octave in range(3, 6):  # octaves 3, 4, 5
    for note, offset in [("C",0), ("D",2), ("E",4), ("F",5), ("G",7), ("A",9), ("B",11)]:
        midi = 60 + (octave-4)*12 + offset
        if 52 <= midi <= 72:
            alto_allowed.append(midi)

print("Soprano allowed MIDI:", sorted(set(soprano_allowed)))
print("Alto allowed MIDI:", sorted(set(alto_allowed)))

# Create solver
solver = Solver()

# Variables: MIDI numbers for each time step
soprano = [Int(f'soprano_{t}') for t in range(time_steps)]
alto = [Int(f'alto_{t}') for t in range(time_steps)]

# 1. C Major scale: notes must be from allowed sets
for t in range(time_steps):
    solver.add(Or([soprano[t] == m for m in soprano_allowed]))
    solver.add(Or([alto[t] == m for m in alto_allowed]))

# 2. Voice ranges already enforced by allowed sets

# 3. No voice crossing: Soprano > Alto at all times
for t in range(time_steps):
    solver.add(soprano[t] > alto[t])

# 4. Melodic leaps: consecutive notes ≤ 7 semitones
for t in range(time_steps - 1):
    solver.add(And(
        Abs(soprano[t+1] - soprano[t]) <= 7,
        Abs(alto[t+1] - alto[t]) <= 7
    ))

# 5. Harmonic consonances: allowed intervals
allowed_intervals = [3, 4, 7, 8, 9, 12, 15, 16]
for t in range(time_steps):
    interval = soprano[t] - alto[t]
    solver.add(Or([interval == i for i in allowed_intervals]))

# 6. No parallel motion: no parallel perfect fifths or octaves between consecutive steps
# Perfect fifth = 7 semitones, octave = 12 semitones
for t in range(time_steps - 1):
    # Current intervals
    curr_interval = soprano[t] - alto[t]
    next_interval = soprano[t+1] - alto[t+1]
    
    # Parallel perfect fifths: both intervals are 7 semitones AND voices move in same direction
    # Actually, parallel fifths occur when both voices move in same direction by same interval
    # But simpler: if both intervals are 7 semitones AND the difference between soprano notes equals difference between alto notes
    # Let's implement: if curr_interval == 7 and next_interval == 7, then check if voices move parallel
    # Parallel motion means: (soprano[t+1] - soprano[t]) == (alto[t+1] - alto[t])
    # But we need to avoid parallel perfect fifths AND parallel octaves
    # So: if both intervals are 7 or both are 12, then voices must NOT move parallel
    solver.add(Implies(
        And(curr_interval == 7, next_interval == 7),
        soprano[t+1] - soprano[t] != alto[t+1] - alto[t]
    ))
    solver.add(Implies(
        And(curr_interval == 12, next_interval == 12),
        soprano[t+1] - soprano[t] != alto[t+1] - alto[t]
    ))

# 7. Starting notes: time 1 (index 0)
# Alto must be on C4 (MIDI 60)
solver.add(alto[0] == 60)
# Soprano must be on E4 (64) or G4 (67)
solver.add(Or(soprano[0] == 64, soprano[0] == 67))

# 8. Cadence at time 7 (index 6): both notes must belong to V-chord (G, B, D)
# V-chord notes: G (MIDI 55, 67, 79...), B (59, 71, 83...), D (62, 74, 86...)
# But must be within voice ranges
v_chord_soprano = [m for m in soprano_allowed if m % 12 in [7, 11, 2]]  # G=7, B=11, D=2 mod 12
v_chord_alto = [m for m in alto_allowed if m % 12 in [7, 11, 2]]
print("V-chord soprano options:", v_chord_soprano)
print("V-chord alto options:", v_chord_alto)
solver.add(Or([soprano[6] == m for m in v_chord_soprano]))
solver.add(Or([alto[6] == m for m in v_chord_alto]))

# 9. Final resolution at time 8 (index 7): Soprano = C5 (72), Alto = C4 (60)
solver.add(soprano[7] == 72)
solver.add(alto[7] == 60)

# Check and print solution
result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("\nComposition:")
    for t in range(time_steps):
        s_midi = model[soprano[t]].as_long()
        a_midi = model[alto[t]].as_long()
        # Convert MIDI to note name
        def midi_to_note(midi):
            octave = (midi // 12) - 1
            note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
            note = note_names[midi % 12]
            # For diatonic notes, we want natural names
            if note in ["C#", "D#", "F#", "G#", "A#"]:
                # This shouldn't happen since we constrained to diatonic
                pass
            return f"{note}{octave}"
        
        s_note = midi_to_note(s_midi)
        a_note = midi_to_note(a_midi)
        interval = s_midi - a_midi
        print(f"Time {t+1}: Soprano {s_note} ({s_midi}), Alto {a_note} ({a_midi}), Interval {interval}")
    
    # Analysis summary
    print("\nAnalysis:")
    print("key: C_major")
    print("num_steps:", time_steps)
    print("voices:", voices)
    
    # Count violations (should be 0)
    parallel_fifths = 0
    parallel_octaves = 0
    voice_crossings = 0
    
    for t in range(time_steps - 1):
        s_diff = model[soprano[t+1]].as_long() - model[soprano[t]].as_long()
        a_diff = model[alto[t+1]].as_long() - model[alto[t]].as_long()
        curr_int = model[soprano[t]].as_long() - model[alto[t]].as_long()
        next_int = model[soprano[t+1]].as_long() - model[alto[t+1]].as_long()
        
        if curr_int == 7 and next_int == 7 and s_diff == a_diff:
            parallel_fifths += 1
        if curr_int == 12 and next_int == 12 and s_diff == a_diff:
            parallel_octaves += 1
        if model[soprano[t]].as_long() <= model[alto[t]].as_long():
            voice_crossings += 1
    
    print("parallel_fifths:", parallel_fifths)
    print("parallel_octaves:", parallel_octaves)
    print("voice_crossings:", voice_crossings)
    print("cadence: authentic")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No solution found - constraints may be too strict")
else:
    print("STATUS: unknown")