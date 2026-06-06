from z3 import *

# Let's simplify. Use a direct encoding: each position gets an article.
# Articles: G=0, H=1, J=2 (finance), Q=3, R=4, S=5 (nutrition), Y=6 (wildlife)

# topic_of function
def topic(a):
    if a in {0, 1, 2}:
        return 0  # finance
    elif a in {3, 4, 5}:
        return 1  # nutrition
    else:
        return 2  # wildlife

solver = Solver()

# pos[i] = article at position i (0=first, ..., 6=seventh)
pos = [Int(f"pos_{i}") for i in range(7)]
for i in range(7):
    solver.add(pos[i] >= 0, pos[i] <= 6)
solver.add(Distinct(pos))

# Constraint 1: No consecutive same topic
for i in range(6):
    # For each pair of distinct articles a1, a2: if pos[i]==a1 and pos[i+1]==a2, then topic(a1)!=topic(a2)
    cons = []
    for a1 in range(7):
        for a2 in range(7):
            if a1 != a2:
                cons.append(Implies(And(pos[i] == a1, pos[i+1] == a2), topic(a1) != topic(a2)))
    solver.add(And(cons))

# Constraint 2: S can be earlier than Q only if Q is third.
# S=5, Q=3. If S is before Q (position of S < position of Q), then Q must be at position 2 (third, index 2)
# position of S = the i such that pos[i] == 5
# position of Q = the i such that pos[i] == 3
# We need: If pos_of_S < pos_of_Q, then pos_of_Q == 2
# Let's encode using auxiliary variables
pos_of_S = Int('pos_of_S')
pos_of_Q = Int('pos_of_Q')
solver.add(Or([And(pos[i] == 5, pos_of_S == i) for i in range(7)]))
solver.add(Or([And(pos[i] == 3, pos_of_Q == i) for i in range(7)]))
solver.add(Implies(pos_of_S < pos_of_Q, pos_of_Q == 2))

# Constraint 3: S must be earlier than Y. S=5, Y=6
pos_of_Y = Int('pos_of_Y')
solver.add(Or([And(pos[i] == 6, pos_of_Y == i) for i in range(7)]))
solver.add(pos_of_S < pos_of_Y)

# Constraint 4: J (2) before G (0) before R (4)
pos_of_J = Int('pos_of_J')
pos_of_G = Int('pos_of_G')
pos_of_R = Int('pos_of_R')
solver.add(Or([And(pos[i] == 2, pos_of_J == i) for i in range(7)]))
solver.add(Or([And(pos[i] == 0, pos_of_G == i) for i in range(7)]))
solver.add(Or([And(pos[i] == 4, pos_of_R == i) for i in range(7)]))
solver.add(pos_of_J < pos_of_G)
solver.add(pos_of_G < pos_of_R)

# Now evaluate each option
name_to_idx = {"G": 0, "H": 1, "J": 2, "Q": 3, "R": 4, "S": 5, "Y": 6}
options = {
    "A": ["H", "S", "J", "Q", "Y", "G", "R"],
    "B": ["J", "Q", "G", "H", "S", "Y", "R"],
    "C": ["Q", "J", "S", "H", "Y", "G", "R"],
    "D": ["Q", "J", "Y", "S", "G", "R", "H"],
    "E": ["S", "G", "Q", "J", "Y", "R", "H"]
}

found_options = []
for letter, order in options.items():
    solver.push()
    for pos_idx, art_name in enumerate(order):
        art_idx = name_to_idx[art_name]
        solver.add(pos[pos_idx] == art_idx)
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