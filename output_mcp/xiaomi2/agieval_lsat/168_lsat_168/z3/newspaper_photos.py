from z3 import *

solver = Solver()

# Variables: number of each photographer's photos in each section
# F=Fuentes, G=Gagnon, H=Hue
# Sections: L=Lifestyle, M=Metro, S=Sports
LF, LG, LH = Ints('LF LG LH')
MF, MG, MH = Ints('MF MG MH')
SF, SG, SH = Ints('SF SG SH')

# All variables are non-negative
for v in [LF, LG, LH, MF, MG, MH, SF, SG, SH]:
    solver.add(v >= 0)

# Constraint 1: Each section has exactly 2 photos
solver.add(LF + LG + LH == 2)
solver.add(MF + MG + MH == 2)
solver.add(SF + SG + SH == 2)

# Constraint 2: Each photographer has at least 1 and at most 3 photos total
solver.add(LF + MF + SF >= 1, LF + MF + SF <= 3)
solver.add(LG + MG + SG >= 1, LG + MG + SG <= 3)
solver.add(LH + MH + SH >= 1, LH + MH + SH <= 3)

# Constraint 3: At least one Lifestyle photo is by a photographer who has at least one Metro photo
solver.add(Or(
    And(LF >= 1, MF >= 1),
    And(LG >= 1, MG >= 1),
    And(LH >= 1, MH >= 1)
))

# Constraint 4: Hue's photos in Lifestyle == Fuentes' photos in Sports
solver.add(LH == SF)

# Constraint 5: No Gagnon photos in Sports
solver.add(SG == 0)

# Define each answer option
opt_a = And(LF == 2, LG == 0, LH == 0,
            MF == 1, MG == 0, MH == 1,
            SF == 0, SG == 1, SH == 1)

opt_b = And(LF == 1, LG == 1, LH == 0,
            MF == 1, MG == 1, MH == 0,
            SF == 0, SG == 0, SH == 2)

opt_c = And(LF == 2, LG == 0, LH == 0,
            MF == 0, MG == 2, MH == 0,
            SF == 0, SG == 0, SH == 2)

opt_d = And(LF == 0, LG == 2, LH == 0,
            MF == 1, MG == 1, MH == 0,
            SF == 1, SG == 0, SH == 1)

opt_e = And(LF == 0, LG == 1, LH == 1,
            MF == 0, MG == 0, MH == 2,
            SF == 1, SG == 0, SH == 1)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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