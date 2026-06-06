from z3 import *

# We need to model the initial ownership and then apply exactly one trade.
# Let's encode buildings and their classes.

# Buildings and their classes:
# RealProp: Garza Tower (class 1), Yates House (class 3), Zimmer House (class 3)
# Southco: Flores Tower (class 1), Lynch Building (class 2)
# Trustcorp: King Building (class 2), Meyer Building (class 2), Ortiz Building (class 2)

# We'll assign each building a class constant.
# Building names: G (Garza), Y (Yates), Z (Zimmer), F (Flores), L (Lynch), K (King), M (Meyer), O (Ortiz)
# Classes: 1, 2, 3

buildings = ["G", "Y", "Z", "F", "L", "K", "M", "O"]
building_class = {
    "G": 1, "Y": 3, "Z": 3,
    "F": 1, "L": 2,
    "K": 2, "M": 2, "O": 2
}

# Initial owners: 0=RealProp, 1=Southco, 2=Trustcorp
initial_owner = {
    "G": 0, "Y": 0, "Z": 0,
    "F": 1, "L": 1,
    "K": 2, "M": 2, "O": 2
}

# After one trade, each building is owned by exactly one company.
# We'll create variables for the new owner of each building.
owner = {b: Int(f"owner_{b}") for b in buildings}

solver = Solver()

# Domain: each owner is 0, 1, or 2
for b in buildings:
    solver.add(owner[b] >= 0, owner[b] <= 2)

# The trade must be exactly one of three kinds:
# Type 1: Trade one building for one other building of the same class
# Type 2: Trade one class 1 building for two class 2 buildings
# Type 3: Trade one class 2 building for two class 3 buildings

# We need to model that exactly one trade happens.
# Let's think about what changes: after a trade, some buildings change owners.
# The total set of buildings owned by each company may change.

# Let's model the trade as: some buildings are "given" by their current owner to another company,
# and some buildings are "received" by that company from others.

# Actually, let's think about it differently.
# A trade involves:
# - One company gives away some buildings and receives some buildings.
# - Another company (or companies) give away some buildings and receive some.

# For Type 1: Company A gives building X to Company B, and Company B gives building Y to Company A.
#   X and Y must be same class.
# For Type 2: Company A gives a class 1 building to Company B, and Company B gives two class 2 buildings to Company A.
# For Type 3: Company A gives a class 2 building to Company B, and Company B gives two class 3 buildings to Company A.

# Let's model this with boolean variables for each possible trade.

# First, let's define which buildings could be involved in each type of trade.

# We'll create boolean variables for each possible "give" action.
# give[b][c] = True means building b is given by its current owner to company c (c != current owner)

# Actually, let's use a simpler approach: we model the final ownership and
# constrain that it differs from initial ownership by exactly one valid trade.

# Count how many buildings changed owner.
changed = [Bool(f"changed_{b}") for b in buildings]
for i, b in enumerate(buildings):
    solver.add(changed[i] == (owner[b] != initial_owner[b]))

# The number of buildings that changed owner must be:
# Type 1: 2 buildings change owner (one each way)
# Type 2: 3 buildings change owner (1 class 1 goes one way, 2 class 2 go the other)
# Type 3: 3 buildings change owner (1 class 2 goes one way, 2 class 3 go the other)

# So either 2 or 3 buildings change owner.
num_changed = Sum([If(changed[i], 1, 0) for i in range(len(buildings))])
solver.add(Or(num_changed == 2, num_changed == 3))

# Now, let's model the trade types more precisely.

# For each possible trade, we need to identify:
# - The "giver" company (the one that initiates the trade by giving a building)
# - The "receiver" company (the one that receives the primary building and gives back)

# Actually, trades are symmetric in terms of who gives what. Let's think of it as:
# Two companies A and B exchange buildings.

# Type 1: A gives X to B, B gives Y to A. X and Y same class.
#   So: owner[X] changes from A to B, owner[Y] changes from B to A.
#   Only these two buildings change owner.

# Type 2: A gives X (class 1) to B. B gives Y and Z (both class 2) to A.
#   So: owner[X] changes from A to B, owner[Y] changes from B to A, owner[Z] changes from B to A.
#   Three buildings change owner.

# Type 3: A gives X (class 2) to B. B gives Y and Z (both class 3) to A.
#   So: owner[X] changes from A to B, owner[Y] changes from B to A, owner[Z] changes from B to A.
#   Three buildings change owner.

# Let's model this with a "trade type" variable and constraints on which buildings are involved.

trade_type = Int('trade_type')
solver.add(trade_type >= 1, trade_type <= 3)

# For each pair of companies (giver, receiver) with giver != receiver:
# We'll create boolean variables for each possible trade.

# Actually, let's use a more direct encoding.

# We'll create variables for the "giver" and "receiver" companies.
giver = Int('giver')
receiver = Int('receiver')
solver.add(giver >= 0, giver <= 2)
solver.add(receiver >= 0, receiver <= 2)
solver.add(giver != receiver)

# For each building, we track whether it's "given" (changes from giver to receiver)
# or "received" (changes from receiver to giver).

# Let's create boolean variables for each building indicating the direction of change.
# given_by_giver[b] = True means building b was owned by giver and is now owned by receiver
# given_by_receiver[b] = True means building b was owned by receiver and is now owned by giver

given_by_giver = {b: Bool(f"given_by_giver_{b}") for b in buildings}
given_by_receiver = {b: Bool(f"given_by_receiver_{b}") for b in buildings}

for b in buildings:
    # If building b is given by giver to receiver
    solver.add(Implies(given_by_giver[b], And(initial_owner[b] == giver, owner[b] == receiver)))
    # If building b is given by receiver to giver
    solver.add(Implies(given_by_receiver[b], And(initial_owner[b] == receiver, owner[b] == giver)))
    # A building can't be both given by giver and given by receiver
    solver.add(Not(And(given_by_giver[b], given_by_receiver[b])))
    # If a building changes owner and its initial owner is giver, it must be given by giver
    solver.add(Implies(And(changed[buildings.index(b)], initial_owner[b] == giver), given_by_giver[b]))
    # If a building changes owner and its initial owner is receiver, it must be given by receiver
    solver.add(Implies(And(changed[buildings.index(b)], initial_owner[b] == receiver), given_by_receiver[b]))
    # If a building doesn't change owner, it's not given by either
    solver.add(Implies(Not(changed[buildings.index(b)]), And(Not(given_by_giver[b]), Not(given_by_receiver[b]))))

# Count how many buildings are given by giver and by receiver
num_given_by_giver = Sum([If(given_by_giver[b], 1, 0) for b in buildings])
num_given_by_receiver = Sum([If(given_by_receiver[b], 1, 0) for b in buildings])

# Type 1: giver gives 1 building, receiver gives 1 building, same class
# Type 2: giver gives 1 class 1 building, receiver gives 2 class 2 buildings
# Type 3: giver gives 1 class 2 building, receiver gives 2 class 3 buildings

# For Type 1:
type1_cond = And(trade_type == 1, num_given_by_giver == 1, num_given_by_receiver == 1)

# The two buildings must be of the same class
# We need to express: there exists b1 given by giver and b2 given by receiver such that class(b1) == class(b2)
# Since we have exactly one of each, we can just say:
# For all b1 given by giver and b2 given by receiver, class(b1) == class(b2)
# But since there's exactly one of each, we can use a simpler encoding.

# Let's collect the classes of buildings given by giver and receiver
# We'll use the fact that exactly one building is given by each side.

# For Type 2:
type2_cond = And(trade_type == 2, num_given_by_giver == 1, num_given_by_receiver == 2)

# The building given by giver must be class 1, and the two given by receiver must be class 2.
# For Type 3:
type3_cond = And(trade_type == 3, num_given_by_giver == 1, num_given_by_receiver == 2)

# The building given by giver must be class 2, and the two given by receiver must be class 3.

# Now let's encode the class constraints for each type.

# For Type 1: the single building given by giver and the single building given by receiver have the same class.
# We can encode this as: for all pairs (b1,b2), if b1 is given by giver and b2 is given by receiver, then class(b1)==class(b2).
# Since there's exactly one of each, this works.

for b1 in buildings:
    for b2 in buildings:
        if b1 != b2:
            solver.add(Implies(And(type1_cond, given_by_giver[b1], given_by_receiver[b2]),
                               building_class[b1] == building_class[b2]))

# For Type 2: the building given by giver is class 1, and the two given by receiver are class 2.
for b in buildings:
    solver.add(Implies(And(type2_cond, given_by_giver[b]), building_class[b] == 1))
    solver.add(Implies(And(type2_cond, given_by_receiver[b]), building_class[b] == 2))

# For Type 3: the building given by giver is class 2, and the two given by receiver are class 3.
for b in buildings:
    solver.add(Implies(And(type3_cond, given_by_giver[b]), building_class[b] == 2))
    solver.add(Implies(And(type3_cond, given_by_receiver[b]), building_class[b] == 3))

# Exactly one trade type applies
solver.add(Or(type1_cond, type2_cond, type3_cond))

# Now let's define the options.

# Option A:
# RealProp (0): Flores Tower (F) and Garza Tower (G)
# Southco (1): Lynch Building (L), Yates House (Y), Zimmer House (Z)
# Trustcorp (2): King Building (K), Meyer Building (M), Ortiz Building (O)

opt_a_constr = And(
    owner["G"] == 0, owner["F"] == 0,
    owner["Y"] == 1, owner["Z"] == 1, owner["L"] == 1,
    owner["K"] == 2, owner["M"] == 2, owner["O"] == 2
)

# Option B:
# RealProp (0): Garza Tower (G), King Building (K), Ortiz Building (O)
# Southco (1): Flores Tower (F), Lynch Building (L)
# Trustcorp (2): Meyer Building (M), Yates House (Y), Zimmer House (Z)

opt_b_constr = And(
    owner["G"] == 0, owner["K"] == 0, owner["O"] == 0,
    owner["F"] == 1, owner["L"] == 1,
    owner["M"] == 2, owner["Y"] == 2, owner["Z"] == 2
)

# Option C:
# RealProp (0): Garza Tower (G), Lynch Building (L)
# Southco (1): Flores Tower (F), Yates House (Y), Zimmer House (Z)
# Trustcorp (2): King Building (K), Meyer Building (M), Ortiz Building (O)

opt_c_constr = And(
    owner["G"] == 0, owner["L"] == 0,
    owner["F"] == 1, owner["Y"] == 1, owner["Z"] == 1,
    owner["K"] == 2, owner["M"] == 2, owner["O"] == 2
)

# Option D:
# RealProp (0): Garza Tower (G), Meyer Building (M), Yates House (Y)
# Southco (1): Flores Tower (F), Lynch Building (L)
# Trustcorp (2): King Building (K), Ortiz Building (O), Zimmer House (Z)

opt_d_constr = And(
    owner["G"] == 0, owner["M"] == 0, owner["Y"] == 0,
    owner["F"] == 1, owner["L"] == 1,
    owner["K"] == 2, owner["O"] == 2, owner["Z"] == 2
)

# Option E:
# RealProp (0): Garza Tower (G), Yates House (Y), Zimmer House (Z)
# Southco (1): Lynch Building (L), Ortiz Building (O)
# Trustcorp (2): Flores Tower (F), King Building (K), Meyer Building (M)

opt_e_constr = And(
    owner["G"] == 0, owner["Y"] == 0, owner["Z"] == 0,
    owner["L"] == 1, owner["O"] == 1,
    owner["F"] == 2, owner["K"] == 2, owner["M"] == 2
)

# Now evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
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