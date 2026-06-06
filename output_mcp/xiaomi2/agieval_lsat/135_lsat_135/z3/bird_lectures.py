from z3 import *

solver = Solver()

# Birds: 0=Oystercatchers, 1=Petrels, 2=Rails, 3=Sandpipers, 4=Terns
birds = range(5)
bird_names = ['Oystercatchers', 'Petrels', 'Rails', 'Sandpipers', 'Terns']

# pos[b] = position (1-5) of bird b
pos = [Int(f'pos_{b}') for b in birds]
# hall[b] = True if Gladwyn Hall, False if Howard Auditorium
hall = [Bool(f'hall_{b}') for b in birds]

# All positions are 1-5 and distinct
for b in birds:
    solver.add(pos[b] >= 1, pos[b] <= 5)
solver.add(Distinct(pos))

# Constraint 1: First lecture is in Gladwyn Hall
# The bird at position 1 is in Gladwyn
solver.add(Or([And(pos[b] == 1, hall[b]) for b in birds]))

# Constraint 2: Fourth lecture is in Howard Auditorium
solver.add(Or([And(pos[b] == 4, Not(hall[b])) for b in birds]))

# Constraint 3: Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(hall[b], 1, 0) for b in birds]) == 3)

# Constraint 4: Sandpipers in Howard, sandpipers earlier than oystercatchers
solver.add(Not(hall[3]))  # Sandpipers in Howard
solver.add(pos[3] < pos[0])  # Sandpipers earlier than Oystercatchers

# Constraint 5: Terns earlier than Petrels, Petrels in Gladwyn
solver.add(pos[4] < pos[1])  # Terns earlier than Petrels
solver.add(hall[1])  # Petrels in Gladwyn

# Helper: "lecture at position i is in Gladwyn"
def pos_in_gladwyn(i):
    return Or([And(pos[b] == i, hall[b]) for b in birds])

# Helper: "lecture at position i is in Howard"
def pos_in_howard(i):
    return Or([And(pos[b] == i, Not(hall[b])) for b in birds])

# Answer choices - each must be checked for satisfiability
# "Must be false" = UNSAT when added to base constraints
options = {
    "A": And(pos_in_gladwyn(1), pos_in_gladwyn(2)),      # 1st and 2nd both Gladwyn
    "B": And(pos_in_howard(2), pos_in_howard(3)),         # 2nd and 3rd both Howard
    "C": And(pos_in_gladwyn(2), pos_in_gladwyn(5)),       # 2nd and 5th both Gladwyn
    "D": And(pos_in_howard(3), pos_in_howard(4)),         # 3rd and 4th both Howard
    "E": And(pos_in_gladwyn(3), pos_in_gladwyn(5)),       # 3rd and 5th both Gladwyn
}

must_be_false_options = []
possible_options = []

for letter in ["A", "B", "C", "D", "E"]:
    s = Solver()
    # Add all base constraints
    for c in solver.assertions():
        s.add(c)
    # Add the answer choice
    s.add(options[letter])
    result = s.check()
    if result == sat:
        possible_options.append(letter)
        m = s.model()
        print(f"Option {letter}: SAT (can be true)")
        for b in birds:
            print(f"  {bird_names[b]}: pos={m[pos[b]]}, hall={'Gladwyn' if is_true(m[hall[b]]) else 'Howard'}")
    elif result == unsat:
        must_be_false_options.append(letter)
        print(f"Option {letter}: UNSAT (must be false!)")
    else:
        print(f"Option {letter}: UNKNOWN")

print()
if len(must_be_false_options) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_false_options[0]}")
elif len(must_be_false_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-false options found {must_be_false_options}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-false options found")