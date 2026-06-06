from z3 import *

solver = Solver()
# Variables for positions
posK = Int('posK')
posL = Int('posL')
posT = Int('posT')
posW = Int('posW')
posY = Int('posY')
posZ = Int('posZ')
positions = [posK, posL, posT, posW, posY, posZ]
# Domain constraints
for p in positions:
    solver.add(p >= 1, p <= 6)
# All distinct
solver.add(Distinct(positions))
# Recorded constraints
# K and L are recorded; others not recorded (implicitly)
# Fourth audition cannot be recorded => position 4 not K nor L
solver.add(posK != 4, posL != 4)
# Fifth audition must be recorded => position 5 is K or L
solver.add(Or(posK == 5, posL == 5))
# Waite earlier than both recorded auditions
solver.add(posW < posK)
solver.add(posW < posL)
# K earlier than T
solver.add(posK < posT)
# Z earlier than Y
solver.add(posZ < posY)
# Additional condition for the question: K immediately before Y
solver.add(posY == posK + 1)

# Define option constraints
opt_a_constr = (posK == 2)  # A
opt_b_constr = (posT == 4)  # B
opt_c_constr = (posW == 3)  # C
opt_d_constr = (posY == 6)  # D
opt_e_constr = (posZ == 2)  # E

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