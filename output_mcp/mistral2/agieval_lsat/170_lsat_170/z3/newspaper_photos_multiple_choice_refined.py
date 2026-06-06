from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for photographers per section
# Sections: Lifestyle, Metro, Sports
# Photographers: Fuentes (0), Gagnon (1), Hue (2)

# We have 2 photos per section, so we model the assignment of photographers to photos in each section.
# For each section, we have two photos, each assigned to a photographer.

# Lifestyle section: lifestyle_1, lifestyle_2
lifestyle_1 = Int('lifestyle_1')
lifestyle_2 = Int('lifestyle_2')

# Metro section: metro_1, metro_2
metro_1 = Int('metro_1')
metro_2 = Int('metro_2')

# Sports section: sports_1, sports_2
sports_1 = Int('sports_1')
sports_2 = Int('sports_2')

# Constraints:
# 1. Each photo is assigned to exactly one photographer (0, 1, or 2)
solver = Solver()
solver.add(lifestyle_1 >= 0, lifestyle_1 <= 2)
solver.add(lifestyle_2 >= 0, lifestyle_2 <= 2)
solver.add(metro_1 >= 0, metro_1 <= 2)
solver.add(metro_2 >= 0, metro_2 <= 2)
solver.add(sports_1 >= 0, sports_1 <= 2)
solver.add(sports_2 >= 0, sports_2 <= 2)

# 2. For each photographer, at least one but no more than three of that photographer's photographs must appear.
# Count the number of photos per photographer across all sections.
F_count = Sum([If(lifestyle_1 == 0, 1, 0), If(lifestyle_2 == 0, 1, 0),
               If(metro_1 == 0, 1, 0), If(metro_2 == 0, 1, 0),
               If(sports_1 == 0, 1, 0), If(sports_2 == 0, 1, 0)])
G_count = Sum([If(lifestyle_1 == 1, 1, 0), If(lifestyle_2 == 1, 1, 0),
               If(metro_1 == 1, 1, 0), If(metro_2 == 1, 1, 0),
               If(sports_1 == 1, 1, 0), If(sports_2 == 1, 1, 0)])
H_count = Sum([If(lifestyle_1 == 2, 1, 0), If(lifestyle_2 == 2, 1, 0),
               If(metro_1 == 2, 1, 0), If(metro_2 == 2, 1, 0),
               If(sports_1 == 2, 1, 0), If(sports_2 == 2, 1, 0)])

solver.add(F_count >= 1, F_count <= 3)
solver.add(G_count >= 1, G_count <= 3)
solver.add(H_count >= 1, H_count <= 3)

# 3. At least one photograph in the Lifestyle section must be by a photographer who has at least one photograph in the Metro section.
# This means: At least one of lifestyle_1 or lifestyle_2 must be equal to metro_1 or metro_2.
Lifestyle_has_Metro_Photographer = Or(
    Or(lifestyle_1 == metro_1, lifestyle_1 == metro_2),
    Or(lifestyle_2 == metro_1, lifestyle_2 == metro_2)
)
solver.add(Lifestyle_has_Metro_Photographer)

# 4. The number of Hue's photographs in the Lifestyle section must be the same as the number of Fuentes' photographs in the Sports section.
Hue_in_Lifestyle = Sum([If(lifestyle_1 == 2, 1, 0), If(lifestyle_2 == 2, 1, 0)])
Fuentes_in_Sports = Sum([If(sports_1 == 0, 1, 0), If(sports_2 == 0, 1, 0)])
solver.add(Hue_in_Lifestyle == Fuentes_in_Sports)

# 5. None of Gagnon's photographs can be in the Sports section.
Gagnon_not_in_Sports = And(
    sports_1 != 1,
    sports_2 != 1
)
solver.add(Gagnon_not_in_Sports)

# Scenario constraint: One photograph in the Lifestyle section is by Gagnon and one is by Hue.
# This means: {lifestyle_1, lifestyle_2} = {1, 2}
scenario_constraint = And(
    Or(And(lifestyle_1 == 1, lifestyle_2 == 2), And(lifestyle_1 == 2, lifestyle_2 == 1))
)

# Now, we evaluate the multiple choice options under this scenario.
found_options = []

# Option A: Exactly one photograph in the Metro section is by Fuentes.
opt_a_constr = And(
    scenario_constraint,
    Sum([If(metro_1 == 0, 1, 0), If(metro_2 == 0, 1, 0)]) == 1
)

# Option B: Exactly one photograph in the Metro section is by Gagnon.
opt_b_constr = And(
    scenario_constraint,
    Sum([If(metro_1 == 1, 1, 0), If(metro_2 == 1, 1, 0)]) == 1
)

# Option C: Both photographs in the Metro section are by Gagnon.
opt_c_constr = And(
    scenario_constraint,
    metro_1 == 1,
    metro_2 == 1
)

# Option D: Exactly one photograph in the Sports section is by Hue.
opt_d_constr = And(
    scenario_constraint,
    Sum([If(sports_1 == 2, 1, 0), If(sports_2 == 2, 1, 0)]) == 1
)

# Option E: Both photographs in the Sports section are by Hue.
opt_e_constr = And(
    scenario_constraint,
    sports_1 == 2,
    sports_2 == 2
)

# Test each option
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