from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Define companies as a datatype
Company = Datatype('Company')
Company.declare('RealProp')
Company.declare('Southco')
Company.declare('Trustcorp')
Company = Company.create()

# Define classes as a datatype
Class = Datatype('Class')
Class.declare('Class1')
Class.declare('Class2')
Class.declare('Class3')
Class = Class.create()

# Define buildings as symbolic constants
GarzaTower = Int('GarzaTower')
YatesHouse = Int('YatesHouse')
ZimmerHouse = Int('ZimmerHouse')
FloresTower = Int('FloresTower')
LynchBuilding = Int('LynchBuilding')
KingBuilding = Int('KingBuilding')
MeyerBuilding = Int('MeyerBuilding')
OrtizBuilding = Int('OrtizBuilding')

# List of all buildings
buildings = [GarzaTower, YatesHouse, ZimmerHouse, FloresTower, LynchBuilding, KingBuilding, MeyerBuilding, OrtizBuilding]

# Initial ownership and class
initial_owner = Function('initial_owner', IntSort(), Company)
initial_class = Function('initial_class', IntSort(), Class)

# Set initial ownership and class
solver = Solver()

# RealProp's buildings
solver.add(initial_owner(GarzaTower) == Company.RealProp)
solver.add(initial_class(GarzaTower) == Class.Class1)

solver.add(initial_owner(YatesHouse) == Company.RealProp)
solver.add(initial_class(YatesHouse) == Class.Class3)

solver.add(initial_owner(ZimmerHouse) == Company.RealProp)
solver.add(initial_class(ZimmerHouse) == Class.Class3)

# Southco's buildings
solver.add(initial_owner(FloresTower) == Company.Southco)
solver.add(initial_class(FloresTower) == Class.Class1)

solver.add(initial_owner(LynchBuilding) == Company.Southco)
solver.add(initial_class(LynchBuilding) == Class.Class2)

# Trustcorp's buildings
solver.add(initial_owner(KingBuilding) == Company.Trustcorp)
solver.add(initial_class(KingBuilding) == Class.Class2)

solver.add(initial_owner(MeyerBuilding) == Company.Trustcorp)
solver.add(initial_class(MeyerBuilding) == Class.Class2)

solver.add(initial_owner(OrtizBuilding) == Company.Trustcorp)
solver.add(initial_class(OrtizBuilding) == Class.Class2)

# Current ownership and class (after trades)
current_owner = Function('current_owner', IntSort(), Company)
current_class = Function('current_class', IntSort(), Class)

# Initialize current_owner and current_class to initial values
for b in buildings:
    solver.add(current_owner(b) == initial_owner(b))
    solver.add(current_class(b) == initial_class(b))

# Final state constraint: Trustcorp owns no class 2 buildings
# For all buildings owned by Trustcorp, their class is not Class2
for b in buildings:
    solver.add(Implies(current_owner(b) == Company.Trustcorp, 
                      current_class(b) != Class.Class2))

# Option A: RealProp owns a class 1 building
opt_a_constr = Exists([b], And(
    current_owner(b) == Company.RealProp,
    current_class(b) == Class.Class1
))

# Option B: Southco owns only class 2 buildings
opt_b_constr = ForAll([b], Implies(
    current_owner(b) == Company.Southco,
    current_class(b) == Class.Class2
))

# Option C: Southco has made at least one trade with Trustcorp
# This is true if there exists a building that was owned by Southco and is now owned by Trustcorp,
# or vice versa.
opt_c_constr = Exists([b], Or(
    And(
        initial_owner(b) == Company.Southco,
        current_owner(b) == Company.Trustcorp
    ),
    And(
        initial_owner(b) == Company.Trustcorp,
        current_owner(b) == Company.Southco
    )
))

# Option D: Trustcorp owns the Garza Tower
opt_d_constr = current_owner(GarzaTower) == Company.Trustcorp

# Option E: Trustcorp owns the Zimmer House
opt_e_constr = current_owner(ZimmerHouse) == Company.Trustcorp

# Evaluate each option
found_options = []
for letter, constr in [
    ("A", opt_a_constr),
    ("B", opt_b_constr),
    ("C", opt_c_constr),
    ("D", opt_d_constr),
    ("E", opt_e_constr)
]:
    solver.push()
    # Add the constraint for this option
    solver.add(constr)
    # Check if the constraint is satisfiable under the base constraints
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