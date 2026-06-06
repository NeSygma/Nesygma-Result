from z3 import *

# Base constraints for the concert scheduling problem
solver = Solver()

# Compositions represented as integers for Z3
F, H, L, O, P, R, S, T = Ints('F H L O P R S T')

# Schedule: schedule[i] is the composition at position i (0 to 7)
schedule = [Int(f'schedule_{i}') for i in range(8)]

# Each position must be assigned a unique composition
solver.add(Distinct(schedule))

# Each composition must appear exactly once in the schedule
compositions = [F, H, L, O, P, R, S, T]
for comp in compositions:
    solver.add(Or([schedule[i] == comp for i in range(8)]))

# Constraint 1: T is performed either immediately before F or immediately after R
# Case 1: T immediately before F (schedule[i] = T, schedule[i+1] = F)
# Case 2: T immediately after R (schedule[i] = R, schedule[i+1] = T)
solver.add(Or(
    Or([And(schedule[i] == T, schedule[i+1] == F) for i in range(7)]),
    Or([And(schedule[i] == R, schedule[i+1] == T) for i in range(7)])
))

# Constraint 2: At least two compositions are performed either after F and before R, or after R and before F
# This means the number of compositions between F and R (in either order) is at least 2
# So, |position(F) - position(R)| >= 3
f_pos = [schedule[i] == F for i in range(8)]
r_pos = [schedule[i] == R for i in range(8)]

# Find the position of F and R
f_index = Int('f_index')
r_index = Int('r_index')
solver.add(Or([And(f_pos[i], f_index == i) for i in range(8)]))
solver.add(Or([And(r_pos[i], r_index == i) for i in range(8)]))

# Ensure at least two compositions between F and R
solver.add(Or(
    And(f_index < r_index, r_index - f_index >= 3),
    And(r_index < f_index, f_index - r_index >= 3)
))

# Constraint 3: O is performed either first or fifth
solver.add(Or(
    schedule[0] == O,
    schedule[4] == O
))

# Constraint 4: The eighth composition performed is either L or H
solver.add(Or(
    schedule[7] == L,
    schedule[7] == H
))

# Constraint 5: P is performed at some time before S
p_pos = [schedule[i] == P for i in range(8)]
s_pos = [schedule[i] == S for i in range(8)]
p_index = Int('p_index')
s_index = Int('s_index')
solver.add(Or([And(p_pos[i], p_index == i) for i in range(8)]))
solver.add(Or([And(s_pos[i], s_index == i) for i in range(8)]))
solver.add(p_index < s_index)

# Constraint 6: At least one composition is performed either after O and before S, or after S and before O
# This means that O and S are not adjacent, and there is at least one composition between them in either order
# So, |position(O) - position(S)| >= 2

# Find the position of O
o_pos = [schedule[i] == O for i in range(8)]
o_index = Int('o_index')
solver.add(Or([And(o_pos[i], o_index == i) for i in range(8)]))

# Ensure at least one composition between O and S
solver.add(Or(
    And(o_index < s_index, s_index - o_index >= 2),
    And(s_index < o_index, o_index - s_index >= 2)
))

# Now, test each option for P's position
found_options = []

# Option A: P is second (position 1)
solver.push()
solver.add(schedule[1] == P)
if solver.check() == sat:
    found_options.append("A")
    print("Option A is SAT")
else:
    print("Option A is UNSAT")
solver.pop()

# Option B: P is third (position 2)
solver.push()
solver.add(schedule[2] == P)
if solver.check() == sat:
    found_options.append("B")
    print("Option B is SAT")
else:
    print("Option B is UNSAT")
solver.pop()

# Option C: P is fourth (position 3)
solver.push()
solver.add(schedule[3] == P)
if solver.check() == sat:
    found_options.append("C")
    print("Option C is SAT")
else:
    print("Option C is UNSAT")
solver.pop()

# Option D: P is sixth (position 5)
solver.push()
solver.add(schedule[5] == P)
if solver.check() == sat:
    found_options.append("D")
    print("Option D is SAT")
else:
    print("Option D is UNSAT")
solver.pop()

# Option E: P is seventh (position 6)
solver.push()
solver.add(schedule[6] == P)
if solver.check() == sat:
    found_options.append("E")
    print("Option E is SAT")
else:
    print("Option E is UNSAT")
solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")