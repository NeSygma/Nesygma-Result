from z3 import *

solver = Solver()

# Declare the band members and their solos (positions 1 to 6)
band_members = ["guitarist", "keyboard", "percussion", "saxophonist", "trumpeter", "violinist"]
# Assign each member to a solo position (1 to 6)
assignments = {m: Int(f"pos_{m}") for m in band_members}

# Each position from 1 to 6 must be assigned to exactly one band member
positions = [Int(f"pos_{i}") for i in range(1, 7)]
for p in positions:
    solver.add(p >= 1, p <= 6)

# Each band member is assigned to exactly one position
for m in band_members:
    solver.add(assignments[m] >= 1, assignments[m] <= 6)

# All positions are distinct (each solo is performed by exactly one member)
solver.add(Distinct(list(assignments.values())))

# Constraints from the problem statement
# 1. The guitarist does not perform the fourth solo.
solver.add(assignments["guitarist"] != 4)

# 2. The percussionist performs a solo at some time before the keyboard player does.
solver.add(assignments["percussion"] < assignments["keyboard"])

# 3. The keyboard player performs a solo at some time after the violinist does and at some time before the guitarist does.
solver.add(assignments["violinist"] < assignments["keyboard"])
solver.add(assignments["keyboard"] < assignments["guitarist"])

# 4. The saxophonist performs a solo at some time after either the percussionist does or the trumpeter does, but not both.
# This means: (sax > percussion and sax <= trump) or (sax > trump and sax <= percussion)
solver.add(Or(
    And(assignments["saxophonist"] > assignments["percussion"], 
         assignments["saxophonist"] <= assignments["trumpeter"]),
    And(assignments["saxophonist"] > assignments["trumpeter"], 
         assignments["saxophonist"] <= assignments["percussion"])
))

# Base constraints are set. Now evaluate the multiple-choice options.
# Each option is a statement that must be evaluated for validity under the constraints.
# We are to find which of the options (A-E) must be false EXCEPT one (i.e., which one is NOT false).
# So, we will check each option to see if it is possible (sat) or impossible (unsat).
# The correct answer is the one that is possible (sat).

# Define the constraints for each option:
# (A) The keyboard player performs the first solo.
opt_a_constr = (assignments["keyboard"] == 1)

# (B) The guitarist performs the second solo.
opt_b_constr = (assignments["guitarist"] == 2)

# (C) The guitarist performs a solo at some time before the saxophonist does.
opt_c_constr = (assignments["guitarist"] < assignments["saxophonist"])

# (D) The guitarist performs a solo at some time before the percussionist does.
opt_d_constr = (assignments["guitarist"] < assignments["percussion"])

# (E) The keyboard player performs a solo at some time before the saxophonist does.
opt_e_constr = (assignments["keyboard"] < assignments["saxophonist"])

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
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