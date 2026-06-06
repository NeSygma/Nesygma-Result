from z3 import *

# Define constants for C major scale semitone values
scale_vals = [0, 2, 4, 5, 7, 9, 11]

# Melody length
N = 8

# Declare note variables (semitone values)
notes = [Int(f'n{i}') for i in range(N)]

solver = Solver()

# Domain constraints: each note must be one of the scale values
for n in notes:
    solver.add(Or([n == v for v in scale_vals]))

# Start and end on tonic C (0 semitones)
solver.add(notes[0] == 0)
solver.add(notes[-1] == 0)

# Interval variables (signed semitone differences)
intervals = [Int(f'int{i}') for i in range(N-1)]
for i in range(N-1):
    solver.add(intervals[i] == notes[i+1] - notes[i])
    # No large leaps > 4 semitones (absolute value)
    solver.add(Abs(intervals[i]) <= 4)

# Analysis variables
leap_count = Int('leap_count')
solver.add(leap_count == Sum([If(Abs(intervals[i]) > 2, 1, 0) for i in range(N-1)]))

# Direction signs: -1 for down, 0 for unison, 1 for up
signs = [If(intervals[i] > 0, 1, If(intervals[i] < 0, -1, 0)) for i in range(N-1)]
# Direction changes count (ignore unisons)
changes = []
for i in range(1, N-1):
    changes.append(If(And(signs[i] != 0, signs[i-1] != 0, signs[i] != signs[i-1]), 1, 0))

direction_changes = Int('direction_changes')
solver.add(direction_changes == Sum(changes))

# Final resolution boolean (True if last note is tonic)
final_resolution = Bool('final_resolution')
solver.add(final_resolution == (notes[-1] == 0))

# Check satisfiability and print a model
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # Print melody as note names for readability
    semitone_to_name = {0: 'C', 2: 'D', 4: 'E', 5: 'F', 7: 'G', 9: 'A', 11: 'B'}
    melody_names = [semitone_to_name[m.eval(n).as_long()] for n in notes]
    print('melody =', melody_names)
    # Print intervals (signed semitone differences)
    interval_vals = [m.eval(i).as_long() for i in intervals]
    print('intervals =', interval_vals)
    print('analysis.leap_count =', m.eval(leap_count))
    print('analysis.direction_changes =', m.eval(direction_changes))
    print('analysis.final_resolution =', m.eval(final_resolution))
else:
    print('STATUS: unsat')