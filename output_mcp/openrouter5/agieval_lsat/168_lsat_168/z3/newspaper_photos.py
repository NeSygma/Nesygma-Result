from z3 import *

# We have 3 sections: Lifestyle, Metro, Sports
# Each section has exactly 2 photographs
# 3 photographers: Fuentes (F), Gagnon (G), Hue (H)
# We'll model the assignment of photographers to the 6 slots.

# Let's use integer variables for each slot.
# Slots: L0, L1 (Lifestyle), M0, M1 (Metro), S0, S1 (Sports)
# Each variable takes value 0 (Fuentes), 1 (Gagnon), or 2 (Hue)

F, G, H = 0, 1, 2

L0, L1 = Ints('L0 L1')
M0, M1 = Ints('M0 M1')
S0, S1 = Ints('S0 S1')

all_slots = [L0, L1, M0, M1, S0, S1]

solver = Solver()

# Domain: each slot is one of the three photographers
for v in all_slots:
    solver.add(Or(v == F, v == G, v == H))

# Condition 1: For each photographer, at least one but no more than three photographs appear.
# Count per photographer
count_F = Sum([If(v == F, 1, 0) for v in all_slots])
count_G = Sum([If(v == G, 1, 0) for v in all_slots])
count_H = Sum([If(v == H, 1, 0) for v in all_slots])

solver.add(count_F >= 1, count_F <= 3)
solver.add(count_G >= 1, count_G <= 3)
solver.add(count_H >= 1, count_H <= 3)

# Condition 2: At least one photograph in Lifestyle is by a photographer who has at least one photograph in Metro.
# A photographer has at least one in Metro if count of that photographer in Metro >= 1.
# We need: exists photographer p such that (L0==p or L1==p) AND (M0==p or M1==p)
# Let's encode this.
lifestyle_photographers = [L0, L1]
metro_photographers = [M0, M1]

# For each photographer value, check if they appear in both sections
cond2 = Or([
    And(
        Or([slot == p for slot in lifestyle_photographers]),
        Or([slot == p for slot in metro_photographers])
    )
    for p in [F, G, H]
])
solver.add(cond2)

# Condition 3: Number of Hue's photographs in Lifestyle = Number of Fuentes' photographs in Sports
count_H_Lifestyle = Sum([If(v == H, 1, 0) for v in [L0, L1]])
count_F_Sports = Sum([If(v == F, 1, 0) for v in [S0, S1]])
solver.add(count_H_Lifestyle == count_F_Sports)

# Condition 4: None of Gagnon's photographs can be in Sports.
solver.add(S0 != G)
solver.add(S1 != G)

# Now define each option's constraints

# Option A: Lifestyle: both by Fuentes; Metro: one Fuentes, one Hue; Sports: one Gagnon, one Hue
opt_a = And(
    L0 == F, L1 == F,
    Or(And(M0 == F, M1 == H), And(M0 == H, M1 == F)),
    Or(And(S0 == G, S1 == H), And(S0 == H, S1 == G))
)

# Option B: Lifestyle: one Fuentes, one Gagnon; Metro: one Fuentes, one Gagnon; Sports: both Hue
opt_b = And(
    Or(And(L0 == F, L1 == G), And(L0 == G, L1 == F)),
    Or(And(M0 == F, M1 == G), And(M0 == G, M1 == F)),
    S0 == H, S1 == H
)

# Option C: Lifestyle: both Fuentes; Metro: both Gagnon; Sports: both Hue
opt_c = And(
    L0 == F, L1 == F,
    M0 == G, M1 == G,
    S0 == H, S1 == H
)

# Option D: Lifestyle: both Gagnon; Metro: one Fuentes, one Gagnon; Sports: one Fuentes, one Hue
opt_d = And(
    L0 == G, L1 == G,
    Or(And(M0 == F, M1 == G), And(M0 == G, M1 == F)),
    Or(And(S0 == F, S1 == H), And(S0 == H, S1 == F))
)

# Option E: Lifestyle: one Gagnon, one Hue; Metro: both Hue; Sports: one Fuentes, one Hue
opt_e = And(
    Or(And(L0 == G, L1 == H), And(L0 == H, L1 == G)),
    M0 == H, M1 == H,
    Or(And(S0 == F, S1 == H), And(S0 == H, S1 == F))
)

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