from z3 import *
import itertools

# Define business types
businesses = ['O', 'P', 'R1', 'R2', 'S', 'T', 'V']

# Generate all permutations of the 7 businesses
all_perms = list(itertools.permutations(businesses))

def check_base_constraints(assignment):
    # assignment: dict mapping space (1-7) to business label
    # Base constraints (excluding separation constraint)
    
    # Pharmacy at one end
    P_space = assignment['P']
    if not (P_space == 1 or P_space == 7):
        return False
    
    # One restaurant at the other end
    R1_space = assignment['R1']
    R2_space = assignment['R2']
    if P_space == 1:
        if not (R1_space == 7 or R2_space == 7):
            return False
    elif P_space == 7:
        if not (R1_space == 1 or R2_space == 1):
            return False
    
    # Pharmacy next to optometrist or veterinarian
    O_space = assignment['O']
    V_space = assignment['V']
    if not (abs(P_space - O_space) == 1 or abs(P_space - V_space) == 1):
        return False
    
    # Toy store not next to veterinarian
    T_space = assignment['T']
    if abs(T_space - V_space) == 1:
        return False
    
    # All spaces distinct (already ensured by permutation)
    return True

def check_separation_constraint(assignment):
    R1_space = assignment['R1']
    R2_space = assignment['R2']
    return abs(R1_space - R2_space) >= 3

def check_candidate_A(assignment):
    # A restaurant must be in either space 3, space 4, or space 5.
    R1_space = assignment['R1']
    R2_space = assignment['R2']
    return (R1_space in [3,4,5]) or (R2_space in [3,4,5])

def check_candidate_B(assignment):
    # A restaurant must be next to either the optometrist or the veterinarian.
    R1_space = assignment['R1']
    R2_space = assignment['R2']
    O_space = assignment['O']
    V_space = assignment['V']
    return (abs(R1_space - O_space) == 1 or abs(R1_space - V_space) == 1 or
            abs(R2_space - O_space) == 1 or abs(R2_space - V_space) == 1)

def check_candidate_C(assignment):
    # Either the toy store or the veterinarian must be somewhere between the two restaurants.
    R1_space = assignment['R1']
    R2_space = assignment['R2']
    T_space = assignment['T']
    V_space = assignment['V']
    low = min(R1_space, R2_space)
    high = max(R1_space, R2_space)
    # Check if T or V is in (low, high)
    for s in range(low+1, high):
        if s == T_space or s == V_space:
            return True
    return False

def check_candidate_D(assignment):
    # No more than two businesses can separate the pharmacy and the restaurant nearest it.
    P_space = assignment['P']
    R1_space = assignment['R1']
    R2_space = assignment['R2']
    dist1 = abs(P_space - R1_space)
    dist2 = abs(P_space - R2_space)
    min_dist = min(dist1, dist2)
    # "No more than two businesses can separate" means at most two businesses between them,
    # so the distance in positions is at most 3.
    return min_dist <= 3

def check_candidate_E(assignment):
    # The optometrist cannot be next to the shoe store.
    O_space = assignment['O']
    S_space = assignment['S']
    return abs(O_space - S_space) != 1

# Map assignment to a tuple of business types for spaces 1..7, with R for both restaurants
def assignment_to_type_tuple(assignment):
    # assignment: dict mapping business to space
    # We need the inverse: space to business type
    space_to_type = {}
    for business, space in assignment.items():
        if business in ['R1', 'R2']:
            space_to_type[space] = 'R'
        else:
            space_to_type[space] = business
    # Create tuple for spaces 1..7
    return tuple(space_to_type[i] for i in range(1, 8))

# Collect original solutions (with separation constraint)
original_solutions = set()
for perm in all_perms:
    assignment = {business: i+1 for i, business in enumerate(perm)}
    if check_base_constraints(assignment) and check_separation_constraint(assignment):
        original_solutions.add(assignment_to_type_tuple(assignment))

print(f"Original solutions count: {len(original_solutions)}")

# For each candidate, collect solutions
candidates = [
    ('A', check_candidate_A),
    ('B', check_candidate_B),
    ('C', check_candidate_C),
    ('D', check_candidate_D),
    ('E', check_candidate_E)
]

candidate_solutions = {}
for letter, check_func in candidates:
    solutions = set()
    for perm in all_perms:
        assignment = {business: i+1 for i, business in enumerate(perm)}
        if check_base_constraints(assignment) and check_func(assignment):
            solutions.add(assignment_to_type_tuple(assignment))
    candidate_solutions[letter] = solutions
    print(f"Candidate {letter} solutions count: {len(solutions)}")

# Find which candidate has the same solution set as original
equivalent_candidates = []
for letter, solutions in candidate_solutions.items():
    if solutions == original_solutions:
        equivalent_candidates.append(letter)

print(f"Equivalent candidates: {equivalent_candidates}")

# Now use the skeleton to output the answer
from z3 import *
solver = Solver()
# Base constraints (excluding separation constraint) - we don't need to add them for the skeleton output
# We just need to output the answer based on equivalent_candidates

found_options = equivalent_candidates  # This is the list of candidates that are equivalent

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")