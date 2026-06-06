from z3 import *

# Create solver
solver = Solver()

# Define positions 1-5 (using 0-indexed for programming, but conceptually 1-5)
positions = range(5)  # 0,1,2,3,4 correspond to solos 1-5

# Pianist variables: 0 = Wayne, 1 = Zara
pianist = [Int(f'pianist_{i}') for i in positions]
for i in positions:
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))

# Type variables: 0 = Modern, 1 = Traditional
typ = [Int(f'typ_{i}') for i in positions]
for i in positions:
    solver.add(Or(typ[i] == 0, typ[i] == 1))

# Constraint 1: Third solo is traditional (position 2 in 0-indexed)
solver.add(typ[2] == 1)

# Constraint 2: Exactly two traditional pieces are performed consecutively
# This means there is exactly one pair (i, i+1) where both are T (1)
# And for all other consecutive pairs, at least one is M (0)
# Also, we need to ensure that there is exactly one such pair.

# First, define a variable for each consecutive pair being both T
pair_T = [Bool(f'pair_T_{i}') for i in range(4)]  # pairs: (0,1), (1,2), (2,3), (3,4)
for i in range(4):
    solver.add(pair_T[i] == And(typ[i] == 1, typ[i+1] == 1))

# Exactly one of these pairs is true
solver.add(Sum([If(pair_T[i], 1, 0) for i in range(4)]) == 1)

# Additionally, ensure no other consecutive Ts: For any pair not the chosen one, at least one is M
# But this is already enforced by the "exactly one pair" condition? Not exactly: if we have three consecutive Ts,
# then there would be two overlapping pairs both true. So we need to ensure that if pair_T[i] is true,
# then the adjacent pairs are false. But the "exactly one" condition already ensures that.

# However, we also need to ensure that there are no isolated Ts that are adjacent to the pair? 
# Actually, if we have T T T, then pairs (0,1) and (1,2) would both be true, violating "exactly one".
# So the "exactly one" condition already prevents three consecutive Ts.

# But what about T T M T? That would have pair (0,1) true, and pair (3,4) false because typ[4] is T but typ[3] is M.
# That's fine. So the "exactly one pair" condition seems sufficient.

# Constraint 3: Fourth solo condition (position 3 in 0-indexed)
# (pianist[3] = W AND typ[3] = T) OR (pianist[3] = Z AND typ[3] = M)
solver.add(Or(
    And(pianist[3] == 0, typ[3] == 1),
    And(pianist[3] == 1, typ[3] == 0)
))

# Constraint 4: Pianist of second solo ≠ pianist of fifth solo
solver.add(pianist[1] != pianist[4])

# Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece.
# This means: For every position i where typ[i] == 1 (T), there exists some j < i such that typ[j] == 0 (M) AND pianist[j] == 0 (W).
# We can encode this as: For each i, if typ[i] == 1, then there exists j < i with typ[j] == 0 and pianist[j] == 0.
# Since positions are small, we can use a big OR over j < i.

for i in positions:
    # If this position is T, then there must be some earlier M by Wayne
    if i > 0:
        earlier_M_W = Or([And(typ[j] == 0, pianist[j] == 0) for j in range(i)])
        solver.add(Implies(typ[i] == 1, earlier_M_W))
    else:
        # For position 0 (first solo), if it's T, then there is no earlier position, so it would violate constraint.
        # So position 0 cannot be T.
        solver.add(typ[0] == 0)  # Because if typ[0] == 1, there is no j < 0, so constraint fails.

# Additional constraint from question: pianist[1] == pianist[2] (first and second solo same pianist)
# Note: positions: 0=first, 1=second, 2=third, 3=fourth, 4=fifth
solver.add(pianist[0] == pianist[1])

# Now, we need to test each option A through E.
# Option A: Zara performs the first solo → pianist[0] == 1 (Zara)
# Option B: Wayne performs the third solo → pianist[2] == 0 (Wayne)
# Option C: Zara performs the fifth solo → pianist[4] == 1 (Zara)
# Option D: The second solo is a traditional piece → typ[1] == 1
# Option E: The fourth solo is a modern piece → typ[3] == 0

# We'll test each option by adding it and checking if the solver is still satisfiable.
# According to the skeleton, we need to find which option MUST be true (i.e., is true in all models).
# So we test each option: if adding the option makes the solver unsatisfiable, then that option is NOT necessarily true.
# But wait: The question asks "which one of the following must be true?" meaning that in every valid scenario satisfying the constraints,
# that statement is true. So we need to check for each option: if there exists a model where the option is false, then it's not "must be true".
# The skeleton approach: For each option, we add the option and check satisfiability. If satisfiable, then the option is possible.
# But we need the option that is true in ALL models. So we need to check the negation: if adding the negation of the option makes the solver unsatisfiable,
# then the option must be true. However, the skeleton provided doesn't do that; it just checks if the option itself is satisfiable.
# Let me re-read the skeleton: It says "found_options" are those for which solver.check() == sat when adding the option.
# But that would give us options that are possible, not necessarily must-be-true.
# Actually, the skeleton is for "which of the following is likely/possible to be true?" but the question says "must be true".
# I need to adjust: For "must be true", we should check that the negation of the option leads to unsatisfiability.
# But the skeleton given is for "likely/possible". However, the problem says "must be true".
# Let me check the problem statement: "Q: If the pianist who performs the first solo also performs the second solo, then which one of the following must be true?"
# So it's a "must be true" question. The skeleton provided is for "likely/possible" but the problem says "must be true".
# I think I need to use a different approach: For each option, check if the option is true in all models.
# One way: For each option, add the negation of the option and check if the solver is unsatisfiable. If yes, then the option must be true.
# But the skeleton says to use the exact skeleton below. Let me read carefully: "You MUST use the exact skeleton below for evaluating the multiple choice options."
# The skeleton is for "likely/possible" but the problem is "must be true". However, the skeleton might be adapted.
# Actually, looking at the skeleton: It adds the option and checks if sat. If exactly one option is sat, then that's the answer.
# But for "must be true", we need the option that is true in all models. So if we add the option and it's sat, that doesn't mean it must be true.
# I think there's a misunderstanding. Let me think: In logic, "must be true" means the statement is entailed by the premises.
# So we need to check for each option O: Does premises entail O? That is, is premises ∧ ¬O unsatisfiable?
# So I should check the negation of each option.
# But the skeleton says to add the option itself. Maybe the skeleton is for "which of the following could be true?" but the problem says "must be true".
# I'll follow the skeleton as given, but note that for "must be true", we should check the negation.
# However, the problem says "use the exact skeleton below", so I'll use it as is, but I'll interpret the result accordingly.
# Actually, re-reading the skeleton: It says "found_options" are those for which the solver is sat when adding the option.
# Then if exactly one found_option, print that as answer. But that would be for "which option is possible?" not "must be true".
# I think there might be a mistake in the problem statement or skeleton. Given the instruction to use the exact skeleton, I'll use it.
# But I'll also check the negation approach to be sure.

# Let me first use the skeleton as given, then verify with negation.

# Base solver is already set up with all constraints except the options.

# Define option constraints
opt_a_constr = (pianist[0] == 1)  # Zara performs first solo
opt_b_constr = (pianist[2] == 0)  # Wayne performs third solo
opt_c_constr = (pianist[4] == 1)  # Zara performs fifth solo
opt_d_constr = (typ[1] == 1)      # Second solo is traditional
opt_e_constr = (typ[3] == 0)      # Fourth solo is modern

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

# Additionally, let's print some models to understand the situation
print("\n--- Debugging: Checking each option's necessity ---")
# For each option, check if its negation makes the solver unsatisfiable
necessary_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        necessary_options.append(letter)
    solver.pop()

print(f"Necessary options (must be true): {necessary_options}")