from z3 import *

# Create solver
solver = Solver()

# Houses: J, K, L, M, N, O, P
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
# Map house names to indices for easier handling
house_to_idx = {house: i for i, house in enumerate(houses)}

# Variables: position[i] = house shown at position i (1-indexed for clarity)
# We'll use 0-indexed positions 0-6 for positions 1-7
position = [Int(f'pos_{i}') for i in range(7)]

# Each position must be a distinct house (0-6 representing J-P)
for i in range(7):
    solver.add(position[i] >= 0)
    solver.add(position[i] <= 6)

# All positions must be distinct (each house shown exactly once)
solver.add(Distinct(position))

# Map house indices to positions for easier constraint checking
# We'll create variables for where each house is shown
house_pos = {}
for house in houses:
    house_pos[house] = Int(f'house_pos_{house}')

# Each house must be at exactly one position
for house in houses:
    house_idx = house_to_idx[house]
    solver.add(Or([house_pos[house] == i for i in range(7)]))
    # Link position variables: position[i] = house_idx iff house_pos[house] = i
    for i in range(7):
        solver.add(Implies(position[i] == house_idx, house_pos[house] == i))
        solver.add(Implies(house_pos[house] == i, position[i] == house_idx))

# Constraint 1: J must be shown in the evening (positions 6 or 7, i.e., indices 5 or 6)
solver.add(Or(house_pos['J'] == 5, house_pos['J'] == 6))

# Constraint 2: K cannot be shown in the morning (positions 1 or 2, i.e., indices 0 or 1)
solver.add(Not(Or(house_pos['K'] == 0, house_pos['K'] == 1)))

# Constraint 3: L must be shown after K and before M
solver.add(house_pos['K'] < house_pos['L'])
solver.add(house_pos['L'] < house_pos['M'])

# Now evaluate each answer choice
# For each pair (X,Y), we need to check if it's possible to have X and Y adjacent (in either order)
# Adjacent means |pos_X - pos_Y| = 1

# Define the options with their constraints
# Each option is a pair of houses that we want to check if they CAN be consecutive
# We want to find which pair CANNOT be consecutive, so we'll check if it's possible
# If it's possible for a pair to be consecutive, then that pair is NOT the answer
# The answer is the pair for which it's IMPOSSIBLE to be consecutive

# For each option, we'll add the constraint that the two houses ARE consecutive (in either order)
# If the solver returns UNSAT, then that pair cannot be consecutive

# Option A: J, K
opt_a_constr = Or(
    house_pos['J'] == house_pos['K'] + 1,  # J after K
    house_pos['K'] == house_pos['J'] + 1   # K after J
)

# Option B: J, M
opt_b_constr = Or(
    house_pos['J'] == house_pos['M'] + 1,  # J after M
    house_pos['M'] == house_pos['J'] + 1   # M after J
)

# Option C: J, O
opt_c_constr = Or(
    house_pos['J'] == house_pos['O'] + 1,  # J after O
    house_pos['O'] == house_pos['J'] + 1   # O after J
)

# Option D: J, P
opt_d_constr = Or(
    house_pos['J'] == house_pos['P'] + 1,  # J after P
    house_pos['P'] == house_pos['J'] + 1   # P after J
)

# Option E: M, P
opt_e_constr = Or(
    house_pos['M'] == house_pos['P'] + 1,  # M after P
    house_pos['P'] == house_pos['M'] + 1   # P after M
)

# Now use the exact skeleton for multiple choice evaluation
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# According to the problem, we want the pair that CANNOT be shown consecutively
# That means we want the pair for which the constraint (being consecutive) is UNSAT
# But our logic above adds the constraint and checks if SAT
# So if a pair is SAT, it CAN be consecutive (not the answer)
# If a pair is UNSAT, it CANNOT be consecutive (is the answer)
# But we're collecting SAT results, so we need to invert the logic

# Actually, let me re-read the problem: "Which one of the following is a pair of houses that CANNOT be shown consecutively"
# So we want the pair where it's IMPOSSIBLE to be consecutive
# Our current logic checks if it's POSSIBLE to be consecutive
# So we need to find the pair where it's NOT possible

# Let me redo this more carefully
# For each pair, we check if it's possible to have them consecutive
# If it's possible, then that pair is NOT the answer
# If it's impossible, then that pair IS the answer

# So we should collect the pairs that are IMPOSSIBLE (unsat)
# But the skeleton collects SAT results
# Let me modify the approach

# Actually, looking at the skeleton again: it collects SAT results
# But we want the pair that CANNOT be consecutive (unsat)
# So we need to invert the logic

# Let me create a new approach: for each pair, check if it's possible to be consecutive
# If SAT, then it CAN be consecutive (not answer)
# If UNSAT, then it CANNOT be consecutive (answer)
# We want exactly one UNSAT result

# Let me rewrite the evaluation part
print("Evaluating each option for possibility of being consecutive:")
results = {}
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    results[letter] = result
    print(f"Option {letter}: {result}")
    solver.pop()

# Find which pair CANNOT be consecutive (unsat)
cannot_be_consecutive = [letter for letter, result in results.items() if result == unsat]

print(f"\nPairs that cannot be consecutive: {cannot_be_consecutive}")

if len(cannot_be_consecutive) == 1:
    print("STATUS: sat")
    print(f"answer:{cannot_be_consecutive[0]}")
elif len(cannot_be_consecutive) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {cannot_be_consecutive}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")