from z3 import *

solver = Solver()

# There are 5 solos, indexed 0..4 (1st=0, 2nd=1, 3rd=2, 4th=3, 5th=4)
N = 5

# Variables: pianist for each solo (0=Wayne, 1=Zara)
p = [Int(f'p_{i}') for i in range(N)]
# Variables: piece type for each solo (0=modern, 1=traditional)
t = [Int(f't_{i}') for i in range(N)]

# Domains
for i in range(N):
    solver.add(Or(p[i] == 0, p[i] == 1))
    solver.add(Or(t[i] == 0, t[i] == 1))

# Condition 1: The third solo is a traditional piece.
solver.add(t[2] == 1)

# Condition 2: Exactly two of the traditional pieces are performed consecutively.
# Count consecutive traditional pairs (i,i+1) where both are traditional
consec_trad_pairs = Sum([If(And(t[i] == 1, t[i+1] == 1), 1, 0) for i in range(N-1)])
solver.add(consec_trad_pairs == 1)

# Condition 3: In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
# solo 4 = index 3
solver.add(Or(And(p[3] == 0, t[3] == 1), And(p[3] == 1, t[3] == 0)))

# Condition 4: The pianist who performs the second solo does not perform the fifth solo.
# second solo = index 1, fifth solo = index 4
solver.add(p[1] != p[4])

# Condition 5: No traditional piece is performed until Wayne performs at least one modern piece.
# i.e., for all i, if t[i]==1 then there exists j < i such that p[j]==0 and t[j]==0
# Equivalent: the first traditional piece cannot appear before the first Wayne modern piece.
# Encode: For each i, if t[i]==1 then there exists j < i with p[j]==0 and t[j]==0.
for i in range(N):
    if i == 0:
        # first solo cannot be traditional because no prior Wayne modern
        solver.add(t[0] != 1)
    else:
        # if t[i]==1, then at least one j < i has p[j]==0 and t[j]==0
        solver.add(Implies(t[i] == 1, Or([And(p[j] == 0, t[j] == 0) for j in range(i)])))

# Additional condition from the question: The fifth solo is a traditional piece.
solver.add(t[4] == 1)

# Now we need to determine: for exactly how many of the solos is the choice of pianist completely determined?
# We'll check each solo i: is p[i] forced to a specific value (0 or 1) in ALL valid models?
# We can check by testing if both p[i]==0 and p[i]==1 are possible.

determined_count = 0
for i in range(N):
    solver.push()
    solver.add(p[i] == 0)
    res0 = solver.check()
    solver.pop()
    
    solver.push()
    solver.add(p[i] == 1)
    res1 = solver.check()
    solver.pop()
    
    # If exactly one of the two is possible, then p[i] is determined
    if (res0 == sat) != (res1 == sat):
        determined_count += 1

# Now map determined_count to answer choices
# (A) one, (B) two, (C) three, (D) four, (E) five
found_options = []
for letter, constr in [("A", determined_count == 1), ("B", determined_count == 2), 
                        ("C", determined_count == 3), ("D", determined_count == 4),
                        ("E", determined_count == 5)]:
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