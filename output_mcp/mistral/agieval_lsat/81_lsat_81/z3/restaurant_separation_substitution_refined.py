from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Original problem constraints (without the restaurant separation constraint)
def original_constraints():
    # Spaces: 1 through 7
    # Businesses: optometrist (O), pharmacy (P), two restaurants (R1, R2), shoe store (S), toy store (T), veterinarian (V)
    O, P, R1, R2, S, T, V = Ints('O P R1 R2 S T V')
    
    # Each business is in a unique space
    spaces = [O, P, R1, R2, S, T, V]
    
    # All spaces are between 1 and 7
    constraints = [And(1 <= s, s <= 7) for s in spaces]
    
    # All businesses are in distinct spaces
    constraints.append(Distinct(spaces))
    
    # Pharmacy must be at one end (space 1 or 7)
    constraints.append(Or(P == 1, P == 7))
    
    # One restaurant must be at the other end
    constraints.append(Or(R1 == 1, R1 == 7, R2 == 1, R2 == 7))
    constraints.append(Or(
        And(P == 1, Or(R1 == 7, R2 == 7)),
        And(P == 7, Or(R1 == 1, R2 == 1))
    ))
    
    # Pharmacy must be next to either the optometrist or the veterinarian
    def is_adjacent(a, b):
        return Or(a == b + 1, a == b - 1)
    constraints.append(Or(is_adjacent(P, O), is_adjacent(P, V)))
    
    # Toy store cannot be next to the veterinarian
    constraints.append(Not(is_adjacent(T, V)))
    
    # Original restaurant separation constraint (to be replaced in options)
    # Two restaurants must be separated by at least two other businesses
    # This means the absolute difference in their positions is at least 3
    constraints.append(Or(R1 - R2 >= 3, R2 - R1 >= 3))
    
    return constraints, [O, P, R1, R2, S, T, V]

# Option constraints (substituting for the original restaurant separation constraint)
def option_constraints(option):
    O, P, R1, R2, S, T, V = Ints('O P R1 R2 S T V')
    spaces = [O, P, R1, R2, S, T, V]
    
    constraints = [And(1 <= s, s <= 7) for s in spaces]
    constraints.append(Distinct(spaces))
    
    # Pharmacy at one end
    constraints.append(Or(P == 1, P == 7))
    
    # One restaurant at the other end
    constraints.append(Or(R1 == 1, R1 == 7, R2 == 1, R2 == 7))
    constraints.append(Or(
        And(P == 1, Or(R1 == 7, R2 == 7)),
        And(P == 7, Or(R1 == 1, R2 == 1))
    ))
    
    # Pharmacy next to optometrist or veterinarian
    def is_adjacent(a, b):
        return Or(a == b + 1, a == b - 1)
    constraints.append(Or(is_adjacent(P, O), is_adjacent(P, V)))
    
    # Toy store not next to veterinarian
    constraints.append(Not(is_adjacent(T, V)))
    
    # Option-specific constraint
    if option == "A":
        # A restaurant must be in either space 3, space 4, or space 5
        constraints.append(Or(R1 == 3, R1 == 4, R1 == 5, R2 == 3, R2 == 4, R2 == 5))
    elif option == "B":
        # A restaurant must be next to either the optometrist or the veterinarian
        def is_adjacent(a, b):
            return Or(a == b + 1, a == b - 1)
        constraints.append(Or(
            is_adjacent(R1, O), is_adjacent(R1, V),
            is_adjacent(R2, O), is_adjacent(R2, V)
        ))
    elif option == "C":
        # Either the toy store or the veterinarian must be somewhere between the two restaurants
        constraints.append(Or(
            And(R1 < T, T < R2),
            And(R2 < T, T < R1),
            And(R1 < V, V < R2),
            And(R2 < V, V < R1)
        ))
    elif option == "D":
        # No more than two businesses can separate the pharmacy and the restaurant nearest it
        # This means the absolute difference between P and the nearest R is at most 3
        nearest_r = If(abs(P - R1) < abs(P - R2), R1, R2)
        constraints.append(abs(P - nearest_r) <= 3)
    elif option == "E":
        # The optometrist cannot be next to the shoe store
        def is_adjacent(a, b):
            return Or(a == b + 1, a == b - 1)
        constraints.append(Not(is_adjacent(O, S)))
    
    return constraints, [O, P, R1, R2, S, T, V]

# Evaluate each option for uniqueness and equivalence to the original constraint
def evaluate_option(letter):
    solver = Solver()
    constraints, vars_list = option_constraints(letter)
    solver.add(constraints)
    
    # Check if the option is satisfiable
    if solver.check() != sat:
        return False, None
    
    # Check if the solution is unique
    model = solver.model()
    
    # Block the current solution and check for another
    solver.add(Or([v != model[v] for v in vars_list]))
    if solver.check() != sat:
        # Unique solution found
        return True, model
    else:
        # Multiple solutions exist
        return False, None

# Evaluate each option
found_options = []

for letter in ["A", "B", "C", "D", "E"]:
    is_unique, model = evaluate_option(letter)
    if is_unique:
        found_options.append(letter)

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