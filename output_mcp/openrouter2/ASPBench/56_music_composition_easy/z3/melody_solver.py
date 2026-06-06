from z3 import *

# ---------- Problem Parameters ----------
allowed_notes = [0, 2, 4, 5, 7, 9, 11]  # C, D, E, F, G, A, B in semitones
note_names = {0:"C", 2:"D", 4:"E", 5:"F", 7:"G", 9:"A", 11:"B"}

# ---------- Solver ----------
solver = Solver()

# 8 notes
m = [Int(f'm_{i}') for i in range(8)]

# Intervals between consecutive notes
intervals = [Int(f'interval_{i}') for i in range(7)]

# Direction of each interval: 1 ascending, -1 descending, 0 same
dir_vars = [Int(f'dir_{i}') for i in range(7)]

# Direction change flags
dir_change_vars = [Int(f'dir_change_{i}') for i in range(7)]

# Leap count (interval > 2 semitones)
leap_vars = [Int(f'leap_{i}') for i in range(7)]

# Analysis variables
leap_count = Int('leap_count')
direction_changes = Int('direction_changes')
final_resolution = Bool('final_resolution')

# ---------- Constraints ----------
# All notes must be from the C major scale
for i in range(8):
    solver.add(Or([m[i] == val for val in allowed_notes]))

# Start and end on tonic (C)
solver.add(m[0] == 0)
solver.add(m[7] == 0)

# Intervals and related constraints
for i in range(7):
    # interval = absolute difference
    solver.add(intervals[i] == Abs(m[i+1] - m[i]))
    # No large leaps > 4 semitones
    solver.add(intervals[i] <= 4)
    # Leap flag: 1 if interval > 2, else 0
    solver.add(leap_vars[i] == If(intervals[i] > 2, 1, 0))

# Direction of each interval
solver.add(dir_vars[0] == If(m[1] > m[0], 1, If(m[1] < m[0], -1, 0)))
for i in range(1, 7):
    solver.add(dir_vars[i] == If(m[i+1] > m[i], 1, If(m[i+1] < m[i], -1, 0)))

# Direction change flags
for i in range(1, 7):
    solver.add(dir_change_vars[i] == If(And(dir_vars[i] != dir_vars[i-1],
                                            dir_vars[i] != 0,
                                            dir_vars[i-1] != 0), 1, 0))

# Analysis aggregates
solver.add(leap_count == Sum(leap_vars))
solver.add(direction_changes == Sum(dir_change_vars[1:]))  # ignore index 0
solver.add(final_resolution == (m[7] == 0))

# ---------- Solve ----------
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Melody as note names
    melody = [note_names[model.eval(m[i], model_completion=True).as_long()] for i in range(8)]
    print("melody =", melody)
    # Intervals
    intervals_vals = [model.eval(intervals[i], model_completion=True).as_long() for i in range(7)]
    print("intervals =", intervals_vals)
    # Analysis
    print('analysis.key = "C_major"')
    print('analysis.total_steps = 8')
    print(f"analysis.leap_count = {model.eval(leap_count, model_completion=True).as_long()}")
    print(f"analysis.direction_changes = {model.eval(direction_changes, model_completion=True).as_long()}")
    print(f"analysis.final_resolution = {bool(model.eval(final_resolution))}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")