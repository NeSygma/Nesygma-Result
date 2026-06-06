from z3 import *

solver = Solver()

# Variables: number of photos by each photographer in each section
# F=Fuentes, G=Gagnon, H=Hue
# L=Lifestyle, M=Metro, S=Sports
FL, FM, FS = Ints('FL FM FS')
GL, GM, GS = Ints('GL GM GS')
HL, HM, HS = Ints('HL HM HS')

all_vars = [FL, FM, FS, GL, GM, GS, HL, HM, HS]

# All variables are non-negative
for v in all_vars:
    solver.add(v >= 0)

# Exactly 2 photos per section
solver.add(FL + GL + HL == 2)
solver.add(FM + GM + HM == 2)
solver.add(FS + GS + HS == 2)

# Each photographer: at least 1, at most 3 total
solver.add(FL + FM + FS >= 1, FL + FM + FS <= 3)
solver.add(GL + GM + GS >= 1, GL + GM + GS <= 3)
solver.add(HL + HM + HS >= 1, HL + HM + HS <= 3)

# At least one Lifestyle photo is by a photographer who also has at least one Metro photo
solver.add(Or(
    And(FL >= 1, FM >= 1),
    And(GL >= 1, GM >= 1),
    And(HL >= 1, HM >= 1)
))

# Hue's photos in Lifestyle = Fuentes' photos in Sports
solver.add(HL == FS)

# No Gagnon photos in Sports
solver.add(GS == 0)

# Define option constraints for Fuentes
opt_a = And(FL == 1, FM == 1, FS == 1)
opt_b = And(FL == 1, FM == 0, FS == 2)
opt_c = And(FL == 2, FM == 0, FS == 1)
opt_d = And(FL == 0, FM == 1, FS == 2)
opt_e = And(FL == 0, FM == 2, FS == 1)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter}: SAT -> FL={m[FL]}, FM={m[FM]}, FS={m[FS]}, GL={m[GL]}, GM={m[GM]}, GS={m[GS]}, HL={m[HL]}, HM={m[HM]}, HS={m[HS]}")
    else:
        print(f"Option {letter}: {result}")
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