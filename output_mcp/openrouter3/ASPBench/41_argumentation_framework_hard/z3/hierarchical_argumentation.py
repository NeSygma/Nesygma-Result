from z3 import *

# Problem parameters
arguments = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10', 'a11', 'a12', 'a13', 'a14', 'a15', 'a16']
N = len(arguments)

# Map argument names to indices
arg_to_idx = {arg: i for i, arg in enumerate(arguments)}

# Define levels
level = [0] * N
for i, arg in enumerate(arguments):
    if arg in ['a1', 'a2', 'a3', 'a4', 'a5', 'a6']:
        level[i] = 1
    elif arg in ['a7', 'a8', 'a9', 'a10', 'a11', 'a12']:
        level[i] = 2
    else:  # a13-a16
        level[i] = 3

# Define attacks
# Format: (attacker_index, target_index, is_strong)
attacks = []

# Strong attacks
strong_attacks = [
    ('a2', 'a1'), ('a9', 'a8'), ('a14', 'a13'), ('a15', 'a16'),
    ('a1', 'a14'), ('a16', 'a15'), ('a1', 'a3'), ('a1', 'a4'),
    ('a13', 'a7'), ('a13', 'a10'), ('a3', 'a5'), ('a5', 'a3')
]

# Weak attacks
weak_attacks = [
    ('a8', 'a2'), ('a13', 'a9'), ('a8', 'a5'), ('a8', 'a6'),
    ('a16', 'a11'), ('a16', 'a12'), ('a2', 'a7'), ('a10', 'a13')
]

# Convert to indices and add to attacks list
for attacker, target in strong_attacks:
    attacks.append((arg_to_idx[attacker], arg_to_idx[target], True))
for attacker, target in weak_attacks:
    attacks.append((arg_to_idx[attacker], arg_to_idx[target], False))

# Create solver
solver = Solver()

# Decision variables: whether each argument is in the extension
in_extension = [Bool(f'in_{arg}') for arg in arguments]

# Helper function to check if an attack is successful
def is_successful_attack(attacker_idx, target_idx, is_strong):
    if is_strong:
        return True  # Strong attacks are always successful
    else:
        # Weak attack is successful only if attacker level > target level
        return level[attacker_idx] > level[target_idx]

# Build attack success matrix
attack_success = [[False for _ in range(N)] for _ in range(N)]
for attacker_idx, target_idx, is_strong in attacks:
    attack_success[attacker_idx][target_idx] = is_successful_attack(attacker_idx, target_idx, is_strong)

# 1. Conflict-Free: No argument in extension successfully attacks another in extension
for i in range(N):
    for j in range(N):
        if attack_success[i][j]:
            # If i attacks j successfully, they cannot both be in extension
            solver.add(Implies(And(in_extension[i], in_extension[j]), False))

# 2. Self-Defending: For every argument A in extension and every external B that successfully attacks A,
# there must be some C in extension that successfully attacks B
for A in range(N):
    for B in range(N):
        if attack_success[B][A]:  # B successfully attacks A
            # If A is in extension and B is not, then there must be some C in extension that attacks B
            # We need: in_extension[A] and not in_extension[B] => exists C in extension such that attack_success[C][B]
            # This is tricky in Z3 - we'll use a helper variable
            defending = Bool(f'defend_{A}_{B}')
            # defending is true if there exists some C in extension that attacks B
            # We'll model this with an OR over all possible C
            defending_conditions = []
            for C in range(N):
                if attack_success[C][B]:
                    defending_conditions.append(in_extension[C])
            if defending_conditions:
                solver.add(defending == Or(defending_conditions))
            else:
                # No one can defend against B
                solver.add(defending == False)
            
            # Constraint: If A is in extension and B is not, then defending must be true
            solver.add(Implies(And(in_extension[A], Not(in_extension[B])), defending))

# 3. Maximal: Cannot add any argument outside while maintaining conflict-free and self-defending
# For each argument not in extension, adding it would violate conflict-free or self-defending
for A in range(N):
    # Create a temporary solver to check if we can add A
    temp_solver = Solver()
    
    # Add all current extension constraints
    for i in range(N):
        for j in range(N):
            if attack_success[i][j]:
                temp_solver.add(Implies(And(in_extension[i], in_extension[j]), False))
    
    # Add self-defending constraints (simplified version)
    for A2 in range(N):
        for B in range(N):
            if attack_success[B][A2]:
                defending_conditions = []
                for C in range(N):
                    if attack_success[C][B]:
                        defending_conditions.append(in_extension[C])
                if defending_conditions:
                    temp_solver.add(Implies(And(in_extension[A2], Not(in_extension[B])), Or(defending_conditions)))
    
    # Try to add A to the extension
    temp_solver.add(in_extension[A])
    
    # Check if this is satisfiable
    # If it is satisfiable, then A could be added, so the current extension is not maximal
    # We need to ensure that for every A not in extension, adding A makes it unsatisfiable
    # This is complex - we'll use a different approach
    
    # Instead, we'll use the standard approach for maximal admissible sets:
    # The extension must be admissible (conflict-free + self-defending) and
    # for every argument outside, adding it would violate admissibility
    
    # We'll handle maximality differently: after finding admissible sets, we'll check maximality

# For now, let's focus on finding admissible sets first
# We'll add a constraint that the extension is non-empty (to avoid trivial solution)
solver.add(Or(in_extension))

# Check for satisfiability
result = solver.check()

if result == sat:
    print("STATUS: sat")
    model = solver.model()
    
    # Extract the extension
    extension = []
    for i, arg in enumerate(arguments):
        if is_true(model[in_extension[i]]):
            extension.append(arg)
    
    extension.sort()
    print(f"Extension found: {extension}")
    
    # Check if it's maximal (preferred)
    # For each argument not in extension, try adding it
    is_maximal = True
    for arg in arguments:
        if arg not in extension:
            # Create a new solver to check if we can add this argument
            temp_solver = Solver()
            
            # Add the current extension
            for i, a in enumerate(arguments):
                if a in extension:
                    temp_solver.add(in_extension[i])
                else:
                    temp_solver.add(Not(in_extension[i]))
            
            # Try to add the new argument
            arg_idx = arg_to_idx[arg]
            temp_solver.add(in_extension[arg_idx])
            
            # Add conflict-free constraints
            for i in range(N):
                for j in range(N):
                    if attack_success[i][j]:
                        temp_solver.add(Implies(And(in_extension[i], in_extension[j]), False))
            
            # Add self-defending constraints
            for A in range(N):
                for B in range(N):
                    if attack_success[B][A]:
                        defending_conditions = []
                        for C in range(N):
                            if attack_success[C][B]:
                                defending_conditions.append(in_extension[C])
                        if defending_conditions:
                            temp_solver.add(Implies(And(in_extension[A], Not(in_extension[B])), Or(defending_conditions)))
            
            if temp_solver.check() == sat:
                is_maximal = False
                print(f"Argument {arg} could be added while maintaining admissibility")
                break
    
    if is_maximal:
        print("The extension is maximal (preferred)")
        print(f"hierarchical_stable_extensions: [{extension}]")
    else:
        print("The extension is not maximal")
        
elif result == unsat:
    print("STATUS: unsat")
    print("No admissible extension found")
else:
    print("STATUS: unknown")