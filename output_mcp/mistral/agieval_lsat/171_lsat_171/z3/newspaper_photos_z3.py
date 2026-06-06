from z3 import *

# BENCHMARK_MODE: ON
BENCHMARK_MODE = True

# Declare symbolic variables
# We have 6 photographs. Let's index them 0 to 5.
# section_assign[i] = section of photograph i (0=Lifestyle, 1=Metro, 2=Sports)
section_assign = [Int(f"section_{i}") for i in range(6)]

# photographer_assign[i] = photographer of photograph i (0=Fuentes, 1=Gagnon, 2=Hue)
photographer_assign = [Int(f"photographer_{i}") for i in range(6)]

# Helper: Count occurrences of a value in a list
from z3 import Sum, If

def count(lst, val):
    return Sum([If(x == val, 1, 0) for x in lst])

# Helper: Count occurrences of a value in a list for a specific index range
def count_in_range(lst, val, start, end):
    return Sum([If(And(x >= start, x <= end, lst[x] == val), 1, 0) for x in range(len(lst))])

# Constraints
solver = Solver()

# 1. Each photograph is assigned to exactly one section
for i in range(6):
    solver.add(Or(section_assign[i] == 0, section_assign[i] == 1, section_assign[i] == 2))

# 2. Exactly 2 photographs per section
solver.add(count(section_assign, 0) == 2)
solver.add(count(section_assign, 1) == 2)
solver.add(count(section_assign, 2) == 2)

# 3. Each photograph is assigned to exactly one photographer
for i in range(6):
    solver.add(Or(photographer_assign[i] == 0, photographer_assign[i] == 1, photographer_assign[i] == 2))

# 4. Each photographer has at least 1 and at most 3 photographs
solver.add(count(photographer_assign, 0) >= 1)
solver.add(count(photographer_assign, 0) <= 3)
solver.add(count(photographer_assign, 1) >= 1)
solver.add(count(photographer_assign, 1) <= 3)
solver.add(count(photographer_assign, 2) >= 1)
solver.add(count(photographer_assign, 2) <= 3)

# 5. At least one photograph in Lifestyle must be by a photographer who has at least one photograph in Metro
# This means: There exists a photographer p such that p has at least one photo in Metro AND at least one photo in Lifestyle
# We can encode this as: For some photographer p, count of p in Metro >= 1 AND count of p in Lifestyle >= 1
# To encode this, we can iterate over photographers and check if any satisfies both conditions
for p in range(3):
    solver.add(Implies(
        And(count_in_range(photographer_assign, p, 0, 5) >= 1,  # p has at least one photo
             count_in_range(photographer_assign, p, 0, 5) <= 3),
        True
    ))
    # Now, check if p has at least one photo in Metro and at least one in Lifestyle
    has_in_metro = count_in_range([If(photographer_assign[i] == p, section_assign[i], -1) for i in range(6)], 1, 0, 5) >= 1
    has_in_lifestyle = count_in_range([If(photographer_assign[i] == p, section_assign[i], -1) for i in range(6)], 0, 0, 5) >= 1
    solver.add(Implies(And(has_in_metro, has_in_lifestyle), True))

# Instead, a simpler way: There exists a photographer p such that p has at least one photo in Metro and at least one in Lifestyle
# We can encode this as: Or over p of (count of p in Metro >= 1 and count of p in Lifestyle >= 1)
met_lifestyle_constraint = False
for p in range(3):
    count_p_in_metro = count_in_range([If(photographer_assign[i] == p, section_assign[i], -1) for i in range(6)], 1, 0, 5)
    count_p_in_lifestyle = count_in_range([If(photographer_assign[i] == p, section_assign[i], -1) for i in range(6)], 0, 0, 5)
    met_lifestyle_constraint = Or(met_lifestyle_constraint, And(count_p_in_metro >= 1, count_p_in_lifestyle >= 1))
solver.add(met_lifestyle_constraint)

# 6. The number of Hue's photographs in Lifestyle must equal the number of Fuentes' photographs in Sports
# Hue is photographer 2, Fuentes is photographer 0
# Count Hue's photos in Lifestyle (section 0)
count_hue_in_lifestyle = count_in_range([If(photographer_assign[i] == 2, section_assign[i], -1) for i in range(6)], 0, 0, 5)
count_fuentes_in_sports = count_in_range([If(photographer_assign[i] == 0, section_assign[i], -1) for i in range(6)], 2, 0, 5)
solver.add(count_hue_in_lifestyle == count_fuentes_in_sports)

# 7. None of Gagnon's photographs can be in the Sports section
# Gagnon is photographer 1, Sports is section 2
for i in range(6):
    solver.add(Implies(photographer_assign[i] == 1, section_assign[i] != 2))

# Now, evaluate the multiple-choice options for Fuentes' photographs
# Fuentes is photographer 0
# We will check each option by constraining the number of Fuentes' photos in each section

# Option A: One in Lifestyle, one in Metro, one in Sports
opt_a_constr = And(
    count_in_range([If(photographer_assign[i] == 0, section_assign[i], -1) for i in range(6)], 0, 0, 5) == 1,
    count_in_range([If(photographer_assign[i] == 0, section_assign[i], -1) for i in range(6)], 1, 0, 5) == 1,
    count_in_range([If(photographer_assign[i] == 0, section_assign[i], -1) for i in range(6)], 2, 0, 5) == 1
)

# Option B: One in Lifestyle, two in Sports
opt_b_constr = And(
    count_in_range([If(photographer_assign[i] == 0, section_assign[i], -1) for i in range(6)], 0, 0, 5) == 1,
    count_in_range([If(photographer_assign[i] == 0, section_assign[i], -1) for i in range(6)], 2, 0, 5) == 2
)

# Option C: Two in Lifestyle, one in Sports
opt_c_constr = And(
    count_in_range([If(photographer_assign[i] == 0, section_assign[i], -1) for i in range(6)], 0, 0, 5) == 2,
    count_in_range([If(photographer_assign[i] == 0, section_assign[i], -1) for i in range(6)], 2, 0, 5) == 1
)

# Option D: One in Metro, two in Sports
opt_d_constr = And(
    count_in_range([If(photographer_assign[i] == 0, section_assign[i], -1) for i in range(6)], 1, 0, 5) == 1,
    count_in_range([If(photographer_assign[i] == 0, section_assign[i], -1) for i in range(6)], 2, 0, 5) == 2
)

# Option E: Two in Metro, one in Sports
opt_e_constr = And(
    count_in_range([If(photographer_assign[i] == 0, section_assign[i], -1) for i in range(6)], 1, 0, 5) == 2,
    count_in_range([If(photographer_assign[i] == 0, section_assign[i], -1) for i in range(6)], 2, 0, 5) == 1
)

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