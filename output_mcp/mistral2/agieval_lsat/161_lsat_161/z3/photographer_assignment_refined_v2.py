from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for each photographer's assignment
# Possible values: 0 = None, 1 = Silva, 2 = Thorne
photographers = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]
assign = {p: Int(f"assign_{p}") for p in photographers}

# Helper function to check if a photographer is assigned to a ceremony
# ceremony: 1 = Silva, 2 = Thorne
def is_assigned(p, ceremony):
    return assign[p] == ceremony

# Helper function to check if a photographer is not assigned to a ceremony
def not_assigned(p, ceremony):
    return Not(is_assigned(p, ceremony))

# Helper function to check if a photographer is not assigned at all
def not_assigned_any(p):
    return Not(Or([assign[p] == c for c in [1, 2]]))

# Base constraints
solver = Solver()

# 1. At least two photographers assigned to each ceremony
for ceremony in [1, 2]:
    solver.add(Sum([If(is_assigned(p, ceremony), 1, 0) for p in photographers]) >= 2)

# 2. Frost must be assigned together with Heideck to one of the ceremonies
solver.add(Or(
    And(is_assigned("Frost", 1), is_assigned("Heideck", 1)),
    And(is_assigned("Frost", 2), is_assigned("Heideck", 2))
))

# 3. If Lai and Mays are both assigned, they must be assigned to different ceremonies
solver.add(Not(And(
    Not(not_assigned_any("Lai")),
    Not(not_assigned_any("Mays")),
    is_assigned("Lai", 1), is_assigned("Mays", 1)
)))
solver.add(Not(And(
    Not(not_assigned_any("Lai")),
    Not(not_assigned_any("Mays")),
    is_assigned("Lai", 2), is_assigned("Mays", 2)
)))

# 4. If Gonzalez is assigned to Silva University, then Lai must be assigned to Thorne University
solver.add(Implies(
    is_assigned("Gonzalez", 1),
    is_assigned("Lai", 2)
))

# 5. Original constraint: If Knutson is not assigned to Thorne University, then both Heideck and Mays must be assigned to Thorne University
original_constraint = Implies(
    not_assigned("Knutson", 2),
    And(is_assigned("Heideck", 2), is_assigned("Mays", 2))
)
solver.add(original_constraint)

# Now, evaluate each answer choice to see which one is equivalent to the original constraint

# Answer choice A: If Knutson is assigned to Silva University, then Heideck and Mays cannot both be assigned to that ceremony.
opt_a_constr = Implies(
    is_assigned("Knutson", 1),
    Not(And(is_assigned("Heideck", 1), is_assigned("Mays", 1)))
)

# Answer choice B: If Knutson is assigned to Silva University, then Lai must also be assigned to that ceremony.
opt_b_constr = Implies(
    is_assigned("Knutson", 1),
    is_assigned("Lai", 1)
)

# Answer choice C: Unless Knutson is assigned to Thorne University, both Frost and Mays must be assigned to that ceremony.
# "Unless P, Q" is equivalent to "If not P, then Q"
opt_c_constr = Implies(
    not_assigned("Knutson", 2),
    And(is_assigned("Frost", 2), is_assigned("Mays", 2))
)

# Answer choice D: Unless Knutson is assigned to Thorne University, Heideck cannot be assigned to the same ceremony as Lai.
# "Unless P, Q" is equivalent to "If not P, then Q"
opt_d_constr = Implies(
    not_assigned("Knutson", 2),
    Not(Or(
        And(is_assigned("Heideck", 1), is_assigned("Lai", 1)),
        And(is_assigned("Heideck", 2), is_assigned("Lai", 2))
    ))
)

# Answer choice E: Unless either Heideck or Mays is assigned to Thorne University, Knutson must be assigned to that ceremony.
# "Unless P, Q" is equivalent to "If not P, then Q"
opt_e_constr = Implies(
    Not(Or(is_assigned("Heideck", 2), is_assigned("Mays", 2))),
    is_assigned("Knutson", 2)
)

# Now, check which answer choice is equivalent to the original constraint
# We will check if the answer choice produces the same assignments as the original constraint
# To do this, we will check if the answer choice is equivalent to the original constraint
# by checking if the two constraints produce the same models

# We will collect the assignments for the original constraint
original_assignments = []

# First, find a model under the original constraint
solver.push()
solver.add(original_constraint)
if solver.check() == sat:
    model = solver.model()
    original_assignments.append({p: model[assign[p]] for p in photographers})
    # Block this model to find another one
    solver.add(Or([assign[p] != model[assign[p]] for p in photographers]))
    if solver.check() == sat:
        model = solver.model()
        original_assignments.append({p: model[assign[p]] for p in photographers})
        # Block this model as well
        solver.add(Or([assign[p] != model[assign[p]] for p in photographers]))
        if solver.check() == sat:
            model = solver.model()
            original_assignments.append({p: model[assign[p]] for p in photographers})
solver.pop()

# Now, for each answer choice, check if it produces the same assignments as the original constraint
found_options = []

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    # Replace the original constraint with the answer choice
    solver.add(constr)
    # Check if the answer choice produces the same assignments as the original constraint
    # We will check if the answer choice produces at least the same number of models as the original constraint
    # and that the models are the same
    answer_assignments = []
    if solver.check() == sat:
        model = solver.model()
        answer_assignments.append({p: model[assign[p]] for p in photographers})
        # Block this model to find another one
        solver.add(Or([assign[p] != model[assign[p]] for p in photographers]))
        if solver.check() == sat:
            model = solver.model()
            answer_assignments.append({p: model[assign[p]] for p in photographers})
            # Block this model as well
            solver.add(Or([assign[p] != model[assign[p]] for p in photographers]))
            if solver.check() == sat:
                model = solver.model()
                answer_assignments.append({p: model[assign[p]] for p in photographers})
    solver.pop()
    
    # Check if the answer_assignments match the original_assignments
    # We will check if the sets of assignments are the same
    if set(tuple(sorted(assignment.items())) for assignment in answer_assignments) == set(tuple(sorted(assignment.items())) for assignment in original_assignments):
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")