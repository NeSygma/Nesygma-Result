from z3 import *

# BENCHMARK_MODE is ON for this problem
BENCHMARK_MODE = True

# Declare the solo order as a permutation of 0..5 (0=first solo, 5=sixth solo)
solver = Solver()
order = [Int(f'solo_{i}') for i in range(6)]

# Each solo position is assigned to a distinct band member
solver.add(Distinct(order))

# Band members as constants for clarity
GUITARIST, KEYBOARD, PERCUSSION, SAX, TRUMPET, VIOLIN = 0, 1, 2, 3, 4, 5

# 1. The guitarist does not perform the fourth solo (index 3)
solver.add(order[3] != GUITARIST)

# 2. The percussionist performs a solo at some time before the keyboard player does
# We will enforce this by ensuring that the index of percussionist is less than the index of keyboard
percu_index = Int('percu_index')
keyb_index = Int('keyb_index')
solver.add(percu_index < keyb_index)
solver.add(And([If(order[i] == PERCUSSION, percu_index == i, True) for i in range(6)]))
solver.add(And([If(order[i] == KEYBOARD, keyb_index == i, True) for i in range(6)]))

# 3. The keyboard player performs a solo at some time after the violinist does and at some time before the guitarist does
# So: violin_index < keyb_index < guitar_index
violin_index = Int('violin_index')
guitar_index = Int('guitar_index')
solver.add(violin_index < keyb_index)
solver.add(keyb_index < guitar_index)
solver.add(And([If(order[i] == VIOLIN, violin_index == i, True) for i in range(6)]))
solver.add(And([If(order[i] == GUITARIST, guitar_index == i, True) for i in range(6)]))

# 4. The saxophonist performs a solo at some time after either the percussionist does or the trumpeter does, but not both
# Let sax_index be the position of saxophonist
# Let percu_index and trump_index be the positions of percussionist and trumpeter
# We need: (sax_index > percu_index) XOR (sax_index > trump_index)
sax_index = Int('sax_index')
trump_index = Int('trump_index')
solver.add(And([If(order[i] == SAX, sax_index == i, True) for i in range(6)]))
solver.add(And([If(order[i] == TRUMPET, trump_index == i, True) for i in range(6)]))

# Exactly one of the two "after" conditions holds
solver.add(Or(
    And(sax_index > percu_index, sax_index <= trump_index),
    And(sax_index > trump_index, sax_index <= percu_index)
))

# Ensure that the saxophonist is not after both or before both
solver.add(Not(And(sax_index > percu_index, sax_index > trump_index)))
solver.add(Not(And(sax_index <= percu_index, sax_index <= trump_index)))

# Now, we want to check which of the given options CANNOT be third (index 2)
# We will test each option by adding a constraint that the third solo is that option and see if it is possible
found_options = []

# Define the options as constraints for the third solo (order[2] == X)
options = [
    ("A", order[2] == GUITARIST),
    ("B", order[2] == KEYBOARD),
    ("C", order[2] == SAX),
    ("D", order[2] == TRUMPET),
    ("E", order[2] == VIOLIN)
]

for letter, constr in options:
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