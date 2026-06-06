from z3 import *

solver = Solver()

# Variables for each clue's chapter
r_ch = Int('r_ch')
s_ch = Int('s_ch')
t_ch = Int('t_ch')
u_ch = Int('u_ch')
w_ch = Int('w_ch')
x_ch = Int('x_ch')
z_ch = Int('z_ch')

# Base constraints
# All chapters between 1 and 7
solver.add(r_ch >= 1, r_ch <= 7)
solver.add(s_ch >= 1, s_ch <= 7)
solver.add(t_ch >= 1, t_ch <= 7)
solver.add(u_ch >= 1, u_ch <= 7)
solver.add(w_ch >= 1, w_ch <= 7)
solver.add(x_ch >= 1, x_ch <= 7)
solver.add(z_ch >= 1, z_ch <= 7)

# All clues in different chapters
solver.add(Distinct([r_ch, s_ch, t_ch, u_ch, w_ch, x_ch, z_ch]))

# Constraint 1: T cannot be in chapter 1
solver.add(t_ch != 1)

# Constraint 2: T must be before W
solver.add(t_ch < w_ch)

# Constraint 3: Exactly two chapters separating T and W
# This means w_ch - t_ch == 3 (since chapters between are t_ch+1 and t_ch+2)
solver.add(w_ch - t_ch == 3)

# Constraint 4: S and Z not adjacent
solver.add(Or(s_ch - z_ch != 1, z_ch - s_ch != 1))  # This is wrong, need absolute difference
# Correct: |s_ch - z_ch| != 1
solver.add(Not(Or(s_ch - z_ch == 1, z_ch - s_ch == 1)))

# Constraint 5: W and X not adjacent
solver.add(Not(Or(w_ch - x_ch == 1, x_ch - w_ch == 1)))

# Constraint 6: U and X adjacent
solver.add(Or(u_ch - x_ch == 1, x_ch - u_ch == 1))

# Additional: U is in chapter 3
solver.add(u_ch == 3)

# Now test each option
found_options = []

# Option A: R is mentioned in chapter 1
solver.push()
solver.add(r_ch == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: R is mentioned in chapter 5
solver.push()
solver.add(r_ch == 5)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: S is mentioned in chapter 7
solver.push()
solver.add(s_ch == 7)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: W is mentioned in chapter 6
solver.push()
solver.add(w_ch == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: X is mentioned in chapter 4
solver.push()
solver.add(x_ch == 4)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")