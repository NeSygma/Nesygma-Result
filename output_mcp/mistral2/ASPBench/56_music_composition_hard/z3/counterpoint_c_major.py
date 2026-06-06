from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# --- Declare symbolic variables ---
# Soprano and Alto notes as arrays over time steps 1..8
soprano = [Int(f'soprano_{i}') for i in range(1, 9)]  # time steps 1-8
alto    = [Int(f'alto_{i}')    for i in range(1, 9)]  # time steps 1-8

# Harmonic intervals (semitone distance soprano - alto)
harmonic_interval = [Int(f'interval_{i}') for i in range(1, 9)]

# --- Helper: C Major scale notes (MIDI) ---
# C4=60, D4=62, E4=64, F4=65, G4=67, A4=69, B4=71
# C5=72, etc.
C_MAJOR = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81]  # C4 to A5

# Allowed harmonic consonances (semitones)
ALLOWED_HARMONIC_INTERVALS = [3, 4, 7, 8, 9, 12, 15, 16]

# --- Build solver ---
solver = Solver()

# --- Add constraints ---

# 1. Voice ranges
for i in range(1, 9):
    solver.add(soprano[i-1] >= 60, soprano[i-1] <= 81)  # C4 to A5
    solver.add(alto[i-1] >= 52, alto[i-1] <= 72)        # E3 to C5

# 2. All notes in C Major scale
for i in range(1, 9):
    solver.add(Or([soprano[i-1] == n for n in C_MAJOR]))
    solver.add(Or([alto[i-1] == n for n in C_MAJOR]))

# 3. No voice crossing: soprano > alto
for i in range(1, 9):
    solver.add(soprano[i-1] > alto[i-1])

# 4. Starting notes at time 1
solver.add(alto[0] == 60)  # C4
solver.add(Or(soprano[0] == 64, soprano[0] == 67))  # E4 or G4

# 5. Final resolution at time 8
solver.add(soprano[7] == 72)  # C5
solver.add(alto[7] == 60)     # C4

# 6. Cadence at time 7: both notes in V-chord (G, B, D)
# G4=67, B4=71, D5=74
solver.add(Or(alto[6] == 67, alto[6] == 71, alto[6] == 74))
solver.add(Or(soprano[6] == 67, soprano[6] == 71, soprano[6] == 74))

# 7. Harmonic consonances at all time steps
for i in range(1, 9):
    diff = soprano[i-1] - alto[i-1]
    solver.add(Or([diff == iv for iv in ALLOWED_HARMONIC_INTERVALS]))

# 8. Melodic leaps ≤ 7 semitones per voice
for i in range(2, 9):
    # Soprano
    solver.add(abs(soprano[i-1] - soprano[i-2]) <= 7)
    # Alto
    solver.add(abs(alto[i-1] - alto[i-2]) <= 7)

# 9. No parallel perfect fifths or octaves between consecutive steps
for i in range(2, 9):
    prev_interval = soprano[i-2] - alto[i-2]
    curr_interval = soprano[i-1] - alto[i-1]
    # Parallel perfect fifths: both 7 semitones
    solver.add(Not(And(prev_interval == 7, curr_interval == 7)))
    # Parallel octaves: both 12 semitones
    solver.add(Not(And(prev_interval == 12, curr_interval == 12)))

# --- Check satisfiability ---
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # --- Extract and print composition ---
    composition = []
    for i in range(1, 9):
        s_note = model[soprano[i-1]]
        a_note = model[alto[i-1]]
        interval = model[harmonic_interval[i-1]] if harmonic_interval[i-1] in model else None
        composition.append({
            'time': i,
            'soprano_note': s_note,
            'alto_note': a_note,
            'harmonic_interval_semitones': interval
        })
    
    # --- Compute analysis ---
    parallel_fifths = 0
    parallel_octaves = 0
    voice_crossings = 0
    
    for i in range(2, 9):
        prev_interval = model[soprano[i-2]].as_long() - model[alto[i-2]].as_long()
        curr_interval = model[soprano[i-1]].as_long() - model[alto[i-1]].as_long()
        if prev_interval == 7 and curr_interval == 7:
            parallel_fifths += 1
        if prev_interval == 12 and curr_interval == 12:
            parallel_octaves += 1
    
    # Voice crossings: check if any soprano <= alto
    for i in range(1, 9):
        if model[soprano[i-1]].as_long() <= model[alto[i-1]].as_long():
            voice_crossings += 1
    
    analysis = {
        'key': 'C_major',
        'num_steps': 8,
        'voices': ['Soprano', 'Alto'],
        'parallel_fifths': parallel_fifths,
        'parallel_octaves': parallel_octaves,
        'voice_crossings': voice_crossings,
        'cadence': 'authentic'
    }
    
    # Print composition
    print("composition:")
    for step in composition:
        print(f"  time: {step['time']}")
        print(f"    soprano_note: {step['soprano_note']}")
        print(f"    alto_note: {step['alto_note']}")
        print(f"    harmonic_interval_semitones: {step['harmonic_interval_semitones']}")
    
    # Print analysis
    print("analysis:")
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