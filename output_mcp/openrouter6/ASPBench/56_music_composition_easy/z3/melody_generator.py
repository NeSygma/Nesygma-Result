from z3 import *

# Define note indices: 0=C, 1=D, 2=E, 3=F, 4=G, 5=A, 6=B
note_names = ["C", "D", "E", "F", "G", "A", "B"]
# Semitone positions in C major scale (from C)
semitone_pos = [0, 2, 4, 5, 7, 9, 11]

# Create solver
solver = Solver()

# Melody: 8 notes, each an integer 0-6
melody = [Int(f'melody_{i}') for i in range(8)]

# Constraints: each note must be in scale (0-6)
for i in range(8):
    solver.add(melody[i] >= 0)
    solver.add(melody[i] <= 6)

# Start and end on tonic (C = index 0)
solver.add(melody[0] == 0)
solver.add(melody[7] == 0)

# No large leaps > 4 semitones
for i in range(7):
    # Get semitone positions
    semitone_i = semitone_pos[melody[i]]
    semitone_j = semitone_pos[melody[i+1]]
    # Compute absolute difference
    diff = If(semitone_j > semitone_i, semitone_j - semitone_i, semitone_i - semitone_j)
    solver.add(diff <= 4)

# Additional constraints for interesting melody? Not required, but we can add some to avoid trivial solutions.
# For example, avoid repeating same note too much? Not required.
# Let's add a constraint that not all notes are C (to make it interesting)
solver.add(Or([melody[i] != 0 for i in range(1,7)]))

# Check
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Melody:")
    melody_notes = []
    for i in range(8):
        note_idx = m[melody[i]].as_long()
        note_name = note_names[note_idx]
        melody_notes.append(note_name)
        print(f"  Note {i+1}: {note_name}")
    
    # Compute analysis
    total_steps = 8
    leap_count = 0
    direction_changes = 0
    prev_interval = 0  # 0 = no direction, 1 = up, -1 = down
    
    for i in range(7):
        semitone_i = semitone_pos[m[melody[i]].as_long()]
        semitone_j = semitone_pos[m[melody[i+1]].as_long()]
        interval = semitone_j - semitone_i
        # Leap count: intervals larger than 2 semitones
        if abs(interval) > 2:
            leap_count += 1
        # Direction change
        if interval > 0:
            curr_dir = 1
        elif interval < 0:
            curr_dir = -1
        else:
            curr_dir = 0
        if i > 0 and prev_interval != 0 and curr_dir != 0 and prev_interval != curr_dir:
            direction_changes += 1
        prev_interval = curr_dir
    
    final_resolution = True  # ends on tonic by constraint
    
    print("\nAnalysis:")
    print(f"  key: C_major")
    print(f"  total_steps: {total_steps}")
    print(f"  leap_count: {leap_count}")
    print(f"  direction_changes: {direction_changes}")
    print(f"  final_resolution: {final_resolution}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")