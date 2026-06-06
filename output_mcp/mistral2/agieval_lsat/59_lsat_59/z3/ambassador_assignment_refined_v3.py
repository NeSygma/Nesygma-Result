from z3 import *

# Base constraints and original problem setup
solver = Solver()

# Countries
countries = ["Venezuela", "Yemen", "Zambia"]

# Ambassadors
ambassadors = ["Jaramillo", "Kayne", "Landon", "Novetzke", "Ong"]

# Assignments: ambassador -> country (0: Venezuela, 1: Yemen, 2: Zambia)
assignment = {a: Int(f"assignment_{a}") for a in ambassadors}

# Each ambassador is assigned to exactly one country
for a in ambassadors:
    solver.add(Or([assignment[a] == i for i in range(3)]))

# Each country has exactly one ambassador
for c_idx in range(3):
    country_ambassadors = [assignment[a] == c_idx for a in ambassadors]
    solver.add(Sum(country_ambassadors) == 1)

# Constraint 1: Either Kayne or Novetzke, but not both, is assigned to one of the ambassadorships.
solver.add(Or(
    And(assignment["Kayne"] >= 0, assignment["Novetzke"] < 0),
    And(assignment["Novetzke"] >= 0, assignment["Kayne"] < 0)
))

# Original constraint: If Jaramillo is assigned to one of the ambassadorships, then so is Kayne.
# Equivalent to: Jaramillo is not assigned OR Kayne is assigned.
original_constraint = Or(assignment["Jaramillo"] < 0, assignment["Kayne"] >= 0)

# Constraint 3: If Ong is assigned to Venezuela, Kayne is not assigned to Yemen.
# Equivalent to: If Ong is assigned to Venezuela, then Kayne is not assigned to Yemen.
# Which is: Ong is not assigned to Venezuela OR Kayne is not assigned to Yemen.
constraint3 = Or(
    assignment["Ong"] != 0,  # Not Venezuela
    assignment["Kayne"] != 1   # Not Yemen
)

# Constraint 4: If Landon is assigned to an ambassadorship, it is to Zambia.
# Equivalent to: If Landon is assigned, then Landon is assigned to Zambia.
# Which is: Landon is not assigned OR Landon is assigned to Zambia.
constraint4 = Or(
    assignment["Landon"] < 0,  # Not assigned
    assignment["Landon"] == 2   # Assigned to Zambia
)

# Add all constraints to the solver
solver.add(constraint3)
solver.add(constraint4)

# Define substitution constraints
substitutions = {
    "A": Or(assignment["Kayne"] < 0, assignment["Jaramillo"] >= 0),  # If Kayne is assigned, then Jaramillo is assigned
    "B": Implies(And(assignment["Landon"] >= 0, assignment["Ong"] >= 0), assignment["Novetzke"] >= 0),  # If Landon and Ong are both assigned, then Novetzke is assigned
    "C": Or(assignment["Ong"] < 0, assignment["Kayne"] >= 0),  # If Ong is not assigned, then Kayne is assigned
    "D": Not(And(assignment["Jaramillo"] >= 0, assignment["Novetzke"] >= 0)),  # Jaramillo and Novetzke are not both assigned
    "E": Not(And(assignment["Novetzke"] >= 0, assignment["Ong"] >= 0))  # Novetzke and Ong are not both assigned
}

found_options = []

# For each substitution, check if it is equivalent to the original constraint
for letter, substitution_constr in substitutions.items():
    # Check if the substitution constraint is equivalent to the original constraint
    # by ensuring that the set of valid assignments is the same
    
    # Create a solver for the substitution constraint
    s_sub = Solver()
    s_sub.add(constraint3)
    s_sub.add(constraint4)
    s_sub.add(substitution_constr)
    
    # Create a solver for the original constraint
    s_orig = Solver()
    s_orig.add(constraint3)
    s_orig.add(constraint4)
    s_orig.add(original_constraint)
    
    # Check if the two solvers produce the same set of models
    # We do this by checking if the constraints are logically equivalent
    # by ensuring that the constraints imply each other
    
    # Check if substitution_constr implies original_constraint
    s_implies = Solver()
    s_implies.add(Not(Implies(substitution_constr, original_constraint)))
    s_implies.add(constraint3)
    s_implies.add(constraint4)
    implies_result = s_implies.check()
    
    # Check if original_constraint implies substitution_constr
    s_implies2 = Solver()
    s_implies2.add(Not(Implies(original_constraint, substitution_constr)))
    s_implies2.add(constraint3)
    s_implies2.add(constraint4)
    implies_result2 = s_implies2.check()
    
    # If both implications hold, the constraints are equivalent
    if implies_result == unsat and implies_result2 == unsat:
        found_options.append(letter)

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")