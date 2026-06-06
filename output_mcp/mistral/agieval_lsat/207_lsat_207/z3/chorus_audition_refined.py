from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare order variables for each singer
order = {s: Int(f'order_{s}') for s in ['K', 'L', 'T', 'W', 'Y', 'Z']}

# Base constraints (recording status and positions)
# 1. The fourth audition cannot be recorded (K and L are recorded)
# 2. The fifth audition must be recorded
# 4. Kammer's audition must take place earlier than Trillo's audition
# 5. Zinn's audition must take place earlier than Yoshida's audition

# Helper: Add ordering uniqueness and bounds
def add_base_constraints(solver):
    solver.add(Distinct(list(order.values())))
    for s in order:
        solver.add(order[s] >= 1, order[s] <= 6)
    # 1. The fourth audition cannot be recorded (K and L are recorded)
    solver.add(order['K'] != 4)
    solver.add(order['L'] != 4)
    # 2. The fifth audition must be recorded
    solver.add(Or(order['K'] == 5, order['L'] == 5))
    # 4. Kammer's audition must take place earlier than Trillo's audition
    solver.add(order['K'] < order['T'])
    # 5. Zinn's audition must take place earlier than Yoshida's audition
    solver.add(order['Z'] < order['Y'])

# Original Waite constraint (to be replaced in options)
# 3. Waite's audition must take place earlier than the two recorded auditions
original_waite_constraint = And(order['W'] < order['K'], order['W'] < order['L'])

# Now test each option as a replacement for the Waite constraint.
# For each option, we will check if it enforces the same effect as the original constraint:
# i.e., Waite is before both K and L.

found_options = []

# Option A: Zinn's audition is the only one that can take place earlier than Waite's.
# This means: for all other singers X (K, L, T, Y), order[X] > order['W']
# and order['Z'] can be either before or after, but only Z can be before W.
# To encode this, we add:
#   order['W'] < order['K']
#   order['W'] < order['L']
#   order['W'] < order['T']
#   order['W'] < order['Y']
opt_a_constr = And(
    order['W'] < order['K'],
    order['W'] < order['L'],
    order['W'] < order['T'],
    order['W'] < order['Y']
)

# Option B: Waite's audition must take place either immediately before or immediately after Zinn's.
opt_b_constr = Or(
    order['W'] == order['Z'] - 1,
    order['W'] == order['Z'] + 1
)

# Option C: Waite's audition must take place earlier than Lugo's.
opt_c_constr = order['W'] < order['L']

# Option D: Waite's audition must be either first or second.
opt_d_constr = Or(order['W'] == 1, order['W'] == 2)

# Option E: The first audition cannot be recorded.
opt_e_constr = And(order['K'] != 1, order['L'] != 1)

# Test each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    s = Solver()
    add_base_constraints(s)
    # Add the option's constraint instead of the original Waite constraint
    s.add(constr)
    # Now check if the resulting constraints enforce Waite before K and L (same effect as original)
    s.add(order['W'] < order['K'])
    s.add(order['W'] < order['L'])
    
    if s.check() == sat:
        found_options.append(letter)
    else:
        pass

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")