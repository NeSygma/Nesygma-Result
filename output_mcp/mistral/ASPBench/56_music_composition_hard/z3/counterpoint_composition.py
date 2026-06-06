from z3 import *

# BENCHMARK_MODE: ON (model-finding task)
BENCHMARK_MODE = True

# Initialize solver
solver = Solver()

# Time steps
T = 8

# Voice ranges (MIDI numbers)
# Soprano: C4 (60) to A5 (81)
# Alto: E3 (52) to C5 (72)
# C Major scale notes (MIDI):
# C4=60, D4=62, E4=64, F4=65, G4=67, A4=69, B4=71,
# C5=72, D5=74, E5=76, F5=77, G5=79, A5=81

# Allowed MIDI values for C Major scale (C4 to A5 for Soprano, E3 to C5 for Alto)
allowed_midi = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81]

# Declare soprano and alto notes for each time step
soprano = [Int(f'soprano_{t}') for t in range(T)]
alto = [Int(f'alto_{t}') for t in range(T)]

# Helper: Convert MIDI to note name (for output only, not used in constraints)
# We'll just use MIDI numbers in constraints for simplicity

# 1. Voice ranges
for t in range(T):
    solver.add(soprano[t] >= 60, soprano[t] <= 81)  # C4 to A5
    solver.add(alto[t] >= 52, alto[t] <= 72)       # E3 to C5

# 2. All notes must be in C Major scale
for t in range(T):
    solver.add(Or([soprano[t] == m for m in allowed_midi]))
    solver.add(Or([alto[t] == m for m in allowed_midi]))

# 3. No voice crossing: soprano > alto at every time step
for t in range(T):
    solver.add(soprano[t] > alto[t])

# 4. Starting notes (time 1, index 0):
# Alto must be C4 (60)
# Soprano must be E4 (64) or G4 (67)
solver.add(alto[0] == 60)
solver.add(Or(soprano[0] == 64, soprano[0] == 67))

# 5. Cadence at time 7 (index 6): both notes must be in V-chord (G, B, D)
# G4=67, B4=71, D5=74
solver.add(Or(alto[6] == 67, alto[6] == 71, alto[6] == 74))
solver.add(Or(soprano[6] == 67, soprano[6] == 71, soprano[6] == 74))

# 6. Final resolution at time 8 (index 7): Soprano on C5 (72), Alto on C4 (60)
solver.add(soprano[7] == 72)
solver.add(alto[7] == 60)

# 7. Melodic leaps: consecutive notes in each voice must not exceed a perfect fifth (7 semitones)
for t in range(T-1):
    # Soprano
    solver.add(abs(soprano[t+1] - soprano[t]) <= 7)
    # Alto
    solver.add(abs(alto[t+1] - alto[t]) <= 7)

# 8. Harmonic consonances: allowed intervals (soprano - alto) are 3,4,7,8,9,12,15,16 semitones
for t in range(T):
    interval = soprano[t] - alto[t]
    solver.add(Or(
        interval == 3,
        interval == 4,
        interval == 7,
        interval == 8,
        interval == 9,
        interval == 12,
        interval == 15,
        interval == 16
    ))

# 9. No parallel motion: no parallel perfect fifths (7) or parallel octaves (12) between consecutive time steps
for t in range(T-1):
    interval_t = soprano[t] - alto[t]
    interval_t1 = soprano[t+1] - alto[t+1]
    # No parallel fifths (7) or octaves (12)
    solver.add(Not(And(interval_t == 7, interval_t1 == 7)))
    solver.add(Not(And(interval_t == 12, interval_t1 == 12)))

# Check satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract composition
    composition = []
    note_names = {
        60: "C4", 62: "D4", 64: "E4", 65: "F4", 67: "G4", 69: "A4", 71: "B4",
        72: "C5", 74: "D5", 76: "E5", 77: "F5", 79: "G5", 81: "A5",
        52: "E3", 53: "F3", 55: "G3", 57: "A3", 59: "B3", 60: "C4"  # E3=52, C4=60
    }
    
    for t in range(T):
        s_midi = model[soprano[t]].as_long()
        a_midi = model[alto[t]].as_long()
        interval = s_midi - a_midi
        composition.append({
            "time": t + 1,
            "soprano_note": note_names.get(s_midi, f"Unknown({s_midi})"),
            "alto_note": note_names.get(a_midi, f"Unknown({a_midi})"),
            "harmonic_interval_semitones": interval
        })
    
    # Compute analysis summary
    parallel_fifths = 0
    parallel_octaves = 0
    voice_crossings = 0
    
    for t in range(T-1):
        interval_t = model[soprano[t]].as_long() - model[alto[t]].as_long()
        interval_t1 = model[soprano[t+1]].as_long() - model[alto[t+1]].as_long()
        if interval_t == 7 and interval_t1 == 7:
            parallel_fifths += 1
        if interval_t == 12 and interval_t1 == 12:
            parallel_octaves += 1
    
    for t in range(T):
        if model[soprano[t]].as_long() <= model[alto[t]].as_long():
            voice_crossings += 1
    
    analysis = {
        "key": "C_major",
        "num_steps": T,
        "voices": ["Soprano", "Alto"],
        "parallel_fifths": parallel_fifths,
        "parallel_octaves": parallel_octaves,
        "voice_crossings": voice_crossings,
        "cadence": "authentic"
    }
    
    # Print composition
    print("composition =")
    for step in composition:
        print(f"  - time: {step['time']}")
        print(f"    soprano_note: {step['soprano_note']}")
        print(f"    alto_note: {step['alto_note']}")
        print(f"    harmonic_interval_semitones: {step['harmonic_interval_semitones']}")
    
    # Print analysis
    print("analysis =")
    print(f"  key: {analysis['key']}")
    print(f"  num_steps: {analysis['num_steps']}")
    print(f"  voices: {analysis['voices']}")
    print(f"  parallel_fifths: {analysis['parallel_fifths']}")
    print(f"  parallel_octaves: {analysis['parallel_octaves']}")
    print(f"  voice_crossings: {analysis['voice_crossings']}")
    print(f"  cadence: {analysis['cadence']}")

elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")