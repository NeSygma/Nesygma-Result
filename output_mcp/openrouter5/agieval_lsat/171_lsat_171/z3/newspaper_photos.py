from z3 import *

# We have 3 sections: Lifestyle (L), Metro (M), Sports (S)
# Each section has exactly 2 photographs
# 3 photographers: Fuentes (F), Gagnon (G), Hue (H)
# Total 6 photographs

# Let's model using integer variables for counts.
# Variables: For each photographer P and section S, the number of photos by P in S.
# Domain: each is 0, 1, or 2 (since each section has exactly 2 photos)

solver = Solver()

# Count variables: FL, FM, FS, GL, GM, GS, HL, HM, HS
FL, FM, FS = Ints('FL FM FS')
GL, GM, GS = Ints('GL GM GS')
HL, HM, HS = Ints('HL HM HS')

# All counts are non-negative integers
counts = [FL, FM, FS, GL, GM, GS, HL, HM, HS]
for c in counts:
    solver.add(c >= 0)
    solver.add(c <= 2)  # at most 2 per section per photographer

# Each section has exactly 2 photographs
solver.add(FL + GL + HL == 2)  # Lifestyle
solver.add(FM + GM + HM == 2)  # Metro
solver.add(FS + GS + HS == 2)  # Sports

# For each photographer, at least one but no more than three of that photographer's photographs must appear
solver.add(1 <= FL + FM + FS, FL + FM + FS <= 3)  # Fuentes total
solver.add(1 <= GL + GM + GS, GL + GM + GS <= 3)  # Gagnon total
solver.add(1 <= HL + HM + HS, HL + HM + HS <= 3)  # Hue total

# At least one photograph in the Lifestyle section must be by a photographer who has at least one photograph in the Metro section.
# This means: there exists a photographer P such that (photo by P in Lifestyle) AND (photo by P in Metro).
# i.e., (FL >= 1 and FM >= 1) OR (GL >= 1 and GM >= 1) OR (HL >= 1 and HM >= 1)
solver.add(Or(And(FL >= 1, FM >= 1), And(GL >= 1, GM >= 1), And(HL >= 1, HM >= 1)))

# The number of Hue's photographs in the Lifestyle section must be the same as the number of Fuentes' photographs in the Sports section.
solver.add(HL == FS)

# None of Gagnon's photographs can be in the Sports section.
solver.add(GS == 0)

# Now evaluate each option about Fuentes' photographs.
# Option A: One is in Lifestyle, one is in Metro, and one is in Sports.
# That means FL == 1, FM == 1, FS == 1
opt_a = And(FL == 1, FM == 1, FS == 1)

# Option B: One is in Lifestyle, and two are in Sports.
# FL == 1, FS == 2, FM == 0
opt_b = And(FL == 1, FS == 2, FM == 0)

# Option C: Two are in Lifestyle, and one is in Sports.
# FL == 2, FS == 1, FM == 0
opt_c = And(FL == 2, FS == 1, FM == 0)

# Option D: One is in Metro, and two are in Sports.
# FM == 1, FS == 2, FL == 0
opt_d = And(FM == 1, FS == 2, FL == 0)

# Option E: Two are in Metro, and one is in Sports.
# FM == 2, FS == 1, FL == 0
opt_e = And(FM == 2, FS == 1, FL == 0)

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