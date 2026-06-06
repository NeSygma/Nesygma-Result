from z3 import *

# Check each option by seeing if its negation is unsat (meaning it must be true)
solver = Solver()

# 0 = Wayne, 1 = Zara
pianist = [Int(f'pianist_{i}') for i in range(5)]
# 0 = modern, 1 = traditional
piece = [Int(f'piece_{i}') for i in range(5)]

# Domain constraints
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece[i] == 0, piece[i] == 1))

# Condition 1: The third solo is a traditional piece.
solver.add(piece[2] == 1)

# Condition 2: Exactly two of the traditional pieces are performed consecutively.
consec_pairs = [If(And(piece[i] == 1, piece[i+1] == 1), 1, 0) for i in range(4)]
solver.add(Sum(consec_pairs) == 1)

# Condition 3: In the fourth solo, either Wayne performs a traditional piece
# or Zara performs a modern piece.
solver.add(Or(And(pianist[3] == 0, piece[3] == 1), And(pianist[3] == 1, piece[3] == 0)))

# Condition 4: The pianist who performs the second solo does not perform the fifth solo.
solver.add(pianist[1] != pianist[4])

# Condition 5: No traditional piece is performed until Wayne performs at least one modern piece.
for i in range(5):
    if i == 0:
        solver.add(piece[0] != 1)  # First solo cannot be traditional
    else:
        solver.add(Implies(piece[i] == 1, 
                          Or([And(pianist[j] == 0, piece[j] == 0) for j in range(i)])))

# Additional condition from the question: The pianist who performs the first solo
# also performs the second solo.
solver.add(pianist[0] == pianist[1])

# For "must be true", we check if Not(option) is unsat under the given constraints.
# Let's first check the base constraints are satisfiable
print("Checking base constraints...")
base_solver = Solver()
for c in solver.assertions():
    base_solver.add(c)
r = base_solver.check()
print(f"Base constraints: {r}")
if r == sat:
    m = base_solver.model()
    for i in range(5):
        print(f"  Solo {i+1}: pianist={m[pianist[i]]} (0=Wayne,1=Zara), piece={m[piece[i]]} (0=modern,1=traditional)")

# Now check each option's negation
found_must = []
for letter, constr in [
    ("A", pianist[0] == 1),  # Zara performs first
    ("B", pianist[2] == 0),  # Wayne performs third
    ("C", pianist[4] == 1),  # Zara performs fifth
    ("D", piece[1] == 1),    # Second solo is traditional
    ("E", piece[3] == 0)     # Fourth solo is modern
]:
    s = Solver()
    for c in solver.assertions():
        s.add(c)
    s.add(Not(constr))  # Negate the option
    res = s.check()
    print(f"Not({letter}): {res}")
    if res == sat:
        m = s.model()
        for i in range(5):
            print(f"  Solo {i+1}: pianist={m[pianist[i]]}, piece={m[piece[i]]}")
    
    if res == unsat:
        found_must.append(letter)

if len(found_must) == 1:
    print("STATUS: sat")
    print(f"answer:{found_must[0]}")
elif len(found_must) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options are necessary {found_must}")
else:
    print("STATUS: unsat")
    print("Refine: No option is necessary")