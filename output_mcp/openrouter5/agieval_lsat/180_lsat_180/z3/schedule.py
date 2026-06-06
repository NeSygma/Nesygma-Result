from z3 import *

# Students: Grecia (G), Hakeem (H), Joe (J), Katya (K), Louise (L)
students = ['G', 'H', 'J', 'K', 'L']
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
shifts = [0, 1]  # 0 = first shift, 1 = second shift

# Decision variables: shift_assignment[day][shift] = student (as integer 0-4)
# We'll use Int variables
shift_var = {}
for d in range(5):
    for s in range(2):
        shift_var[(d, s)] = Int(f'shift_{days[d]}_{s}')

solver = Solver()

# Domain: each shift is assigned to one of the 5 students (0-4)
for d in range(5):
    for s in range(2):
        solver.add(shift_var[(d, s)] >= 0, shift_var[(d, s)] <= 4)

# Each student works exactly two shifts total
for student_idx in range(5):
    count = Sum([If(shift_var[(d, s)] == student_idx, 1, 0) for d in range(5) for s in range(2)])
    solver.add(count == 2)

# No student works both shifts of any day
for d in range(5):
    solver.add(shift_var[(d, 0)] != shift_var[(d, 1)])

# On two consecutive days, Louise works the second shift.
# Louise is index 4. Second shift is s=1.
# Two consecutive days: (Mon,Tue), (Tue,Wed), (Wed,Thu), (Thu,Fri)
# Exactly one of these pairs must have Louise on second shift on both days.
consecutive_pairs = [(0,1), (1,2), (2,3), (3,4)]
consecutive_louise_second = [And(shift_var[(d1,1)] == 4, shift_var[(d2,1)] == 4) for (d1,d2) in consecutive_pairs]
solver.add(Sum([If(c, 1, 0) for c in consecutive_louise_second]) == 1)

# On two nonconsecutive days, Grecia works the first shift.
# Grecia is index 0. First shift is s=0.
# Nonconsecutive pairs: (Mon,Wed), (Mon,Thu), (Mon,Fri), (Tue,Thu), (Tue,Fri), (Wed,Fri)
nonconsecutive_pairs = [(0,2), (0,3), (0,4), (1,3), (1,4), (2,4)]
nonconsecutive_grecia_first = [And(shift_var[(d1,0)] == 0, shift_var[(d2,0)] == 0) for (d1,d2) in nonconsecutive_pairs]
solver.add(Sum([If(c, 1, 0) for c in nonconsecutive_grecia_first]) == 1)

# Katya works on Tuesday and Friday.
# Katya is index 3.
# Katya works on Tuesday (day 1): she works either first or second shift on Tuesday
solver.add(Or(shift_var[(1,0)] == 3, shift_var[(1,1)] == 3))
# Katya works on Friday (day 4)
solver.add(Or(shift_var[(4,0)] == 3, shift_var[(4,1)] == 3))

# Hakeem and Joe work on the same day as each other at least once.
# Hakeem is index 1, Joe is index 2.
# At least one day where both Hakeem and Joe work (each on some shift that day)
same_day_hj = [Or(And(Or(shift_var[(d,0)] == 1, shift_var[(d,1)] == 1),
                      Or(shift_var[(d,0)] == 2, shift_var[(d,1)] == 2))) for d in range(5)]
solver.add(Or(same_day_hj))

# Grecia and Louise never work on the same day as each other.
# Grecia is 0, Louise is 4.
for d in range(5):
    grecia_works = Or(shift_var[(d,0)] == 0, shift_var[(d,1)] == 0)
    louise_works = Or(shift_var[(d,0)] == 4, shift_var[(d,1)] == 4)
    solver.add(Not(And(grecia_works, louise_works)))

# Now check the answer choices.
# The answer choices talk about "fall" and "spring" publication of cookbooks.
# This seems like a mismatch with the problem description about scheduling shifts.
# Let me re-read the problem...

# Actually, looking at the problem text more carefully:
# "Q: Which one of the following is an acceptable schedule for the publication of the cookbooks?"
# The answer choices are about fall/spring publications with letters K,L,M,N,O,P.
# But the problem description is about scheduling students for shifts at an art gallery.
# This looks like the question text got mixed up with a different problem's answer choices.

# Let me re-read: The problem describes scheduling students G,H,J,K,L for shifts Mon-Fri.
# The answer choices mention K,L,M,N,O,P for fall/spring publications.
# This is clearly a mismatch. The answer choices don't correspond to the problem.

# Let me check if maybe the answer choices are about which students work which shifts?
# Actually, looking more carefully at the answer choices format:
# (A)fall: K, L, M, and O spring: N and P
# These letters don't match our students (G,H,J,K,L).

# I think the problem statement got corrupted. Let me just solve the scheduling problem
# as described and see what valid schedules look like.

# Let me check if the solver finds any valid schedule at all.
result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("Found a valid schedule:")
    for d in range(5):
        first = m[shift_var[(d,0)]].as_long()
        second = m[shift_var[(d,1)]].as_long()
        names = ['G', 'H', 'J', 'K', 'L']
        print(f"  {days[d]}: first={names[first]}, second={names[second]}")
else:
    print("STATUS: unsat")
    print("No valid schedule found")