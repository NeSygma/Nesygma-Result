from z3 import *

# Six lab sessions: 3 days (Wed, Thu, Fri) x 2 slots (morning, afternoon)
# Days: 0=Wednesday, 1=Thursday, 2=Friday
# Slots: 0=morning, 1=afternoon
# We'll assign each assistant to a (day, slot) pair.

assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]

# For each assistant, we have a day variable (0,1,2) and a slot variable (0,1)
day = {a: Int(f"day_{a}") for a in assistants}
slot = {a: Int(f"slot_{a}") for a in assistants}

solver = Solver()

# Domain constraints
for a in assistants:
    solver.add(day[a] >= 0, day[a] <= 2)
    solver.add(slot[a] >= 0, slot[a] <= 1)

# All different sessions: each assistant gets a unique (day, slot) pair
# We can encode this as: no two assistants share the same day AND slot
for i in range(len(assistants)):
    for j in range(i+1, len(assistants)):
        a1 = assistants[i]
        a2 = assistants[j]
        solver.add(Not(And(day[a1] == day[a2], slot[a1] == slot[a2])))

# Constraint 1: Kevin and Rebecca must lead sessions on the same day
solver.add(day["Kevin"] == day["Rebecca"])

# Constraint 2: Lan and Olivia cannot lead sessions on the same day
solver.add(day["Lan"] != day["Olivia"])

# Constraint 3: Nessa must lead an afternoon session
solver.add(slot["Nessa"] == 1)

# Constraint 4: Julio's session must meet on an earlier day than Olivia's
solver.add(day["Julio"] < day["Olivia"])

# Additional condition: Kevin's session meets on the day before Nessa's
solver.add(day["Kevin"] == day["Nessa"] - 1)

# Now we need to find who could lead the Thursday afternoon session.
# Thursday = day 1, afternoon = slot 1.
# For each assistant, we check if there exists a valid assignment where that assistant
# leads the Thursday afternoon session.

# We'll check each assistant individually
possible = []
for a in assistants:
    solver.push()
    solver.add(day[a] == 1)
    solver.add(slot[a] == 1)
    if solver.check() == sat:
        possible.append(a)
    solver.pop()

print("Possible assistants for Thursday afternoon:", possible)

# Now map to answer choices
# (A) Julio, Nessa
# (B) Kevin, Rebecca
# (C) Kevin, Nessa, Rebecca
# (D) Julio, Kevin, Nessa, Rebecca
# (E) Julio, Kevin, Lan, Nessa, Rebecca

opt_a_constr = And([day["Julio"] == 1, slot["Julio"] == 1])  # just check Julio
opt_b_constr = And([day["Kevin"] == 1, slot["Kevin"] == 1])  # just check Kevin
opt_c_constr = And([day["Kevin"] == 1, slot["Kevin"] == 1])  # just check Kevin
opt_d_constr = And([day["Julio"] == 1, slot["Julio"] == 1])  # just check Julio
opt_e_constr = And([day["Julio"] == 1, slot["Julio"] == 1])  # just check Julio

# Actually, we need to check each option as a set. The question asks:
# "which one of the following is a complete and accurate list of lab assistants any one of whom could lead the Thursday afternoon session?"
# So we need to check if the set of possible assistants matches exactly the set in each option.

# Let's build the sets
possible_set = set(possible)

options_sets = {
    "A": {"Julio", "Nessa"},
    "B": {"Kevin", "Rebecca"},
    "C": {"Kevin", "Nessa", "Rebecca"},
    "D": {"Julio", "Kevin", "Nessa", "Rebecca"},
    "E": {"Julio", "Kevin", "Lan", "Nessa", "Rebecca"}
}

found_options = []
for letter, opt_set in options_sets.items():
    if possible_set == opt_set:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")