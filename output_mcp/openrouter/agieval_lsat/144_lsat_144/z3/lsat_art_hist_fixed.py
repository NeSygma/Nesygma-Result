from z3 import *

# Topic constants
LITH = 0
OIL = 1
SCULPT = 2
WATER = 3

# Position variables (1..4)
pos_F, pos_G, pos_H, pos_J = Ints('pos_F pos_G pos_H pos_J')
# Topic assignment variables
topic_F, topic_G, topic_H, topic_J = Ints('topic_F topic_G topic_H topic_J')

solver = Solver()
# Domain constraints
for p in [pos_F, pos_G, pos_H, pos_J]:
    solver.add(p >= 1, p <= 4)
solver.add(Distinct(pos_F, pos_G, pos_H, pos_J))

# Topics distinct and within set
solver.add(Distinct(topic_F, topic_G, topic_H, topic_J))
for t in [topic_F, topic_G, topic_H, topic_J]:
    solver.add(Or(t == LITH, t == OIL, t == SCULPT, t == WATER))

# Helper: position of historian with a given topic
def pos_of(topic_val):
    # returns an expression that equals the position of the historian whose topic == topic_val
    return If(topic_F == topic_val, pos_F,
           If(topic_G == topic_val, pos_G,
           If(topic_H == topic_val, pos_H,
           pos_J)))

# Base constraints
# oil and water earlier than lith
solver.add(pos_of(OIL) < pos_of(LITH))
solver.add(pos_of(WATER) < pos_of(LITH))
# Farley earlier than oil lecture, and Farley cannot be oil
solver.add(topic_F != OIL)
solver.add(pos_F < pos_of(OIL))
# Holden earlier than Garcia and Jiang
solver.add(pos_H < pos_G)
solver.add(pos_H < pos_J)

# Options definitions
options = {}
# A: Farley sculptures (1), Holden lith (2), Garcia oil (3), Jiang water (4)
options['A'] = [pos_F==1, topic_F==SCULPT,
               pos_H==2, topic_H==LITH,
               pos_G==3, topic_G==OIL,
               pos_J==4, topic_J==WATER]
# B: Farley water (1), Jiang oil (2), Holden sculptures (3), Garcia lith (4)
options['B'] = [pos_F==1, topic_F==WATER,
               pos_J==2, topic_J==OIL,
               pos_H==3, topic_H==SCULPT,
               pos_G==4, topic_G==LITH]
# C: Garcia sculptures (1), Farley water (2), Holden oil (3), Jiang lith (4)
options['C'] = [pos_G==1, topic_G==SCULPT,
               pos_F==2, topic_F==WATER,
               pos_H==3, topic_H==OIL,
               pos_J==4, topic_J==LITH]
# D: Holden oil (1), Jiang water (2), Farley lith (3), Garcia sculptures (4)
options['D'] = [pos_H==1, topic_H==OIL,
               pos_J==2, topic_J==WATER,
               pos_F==3, topic_F==LITH,
               pos_G==4, topic_G==SCULPT]
# E: Holden sculptures (1), Farley water (2), Jiang oil (3), Garcia lith (4)
options['E'] = [pos_H==1, topic_H==SCULPT,
               pos_F==2, topic_F==WATER,
               pos_J==3, topic_J==OIL,
               pos_G==4, topic_G==LITH]

found_options = []
for letter, constrs in [("A", options['A']), ("B", options['B']), ("C", options['C']), ("D", options['D']), ("E", options['E'])]:
    solver.push()
    solver.add(constrs)
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