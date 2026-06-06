from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Initialize solver
solver = Solver()

# Declare companies and building classes
companies = ["RealProp", "Southco", "Trustcorp"]
building_classes = [1, 2, 3]

# Declare buildings and their initial owners and classes
buildings = {
    "Garza Tower": ("RealProp", 1),
    "Yates House": ("RealProp", 3),
    "Zimmer House": ("RealProp", 3),
    "Flores Tower": ("Southco", 1),
    "Lynch Building": ("Southco", 2),
    "King Building": ("Trustcorp", 2),
    "Meyer Building": ("Trustcorp", 2),
    "Ortiz Building": ("Trustcorp", 2),
}

# Track the current owner and class of each building
current_owner = {b: o for b, (o, _) in buildings.items()}
current_class = {b: c for b, (_, c) in buildings.items()}

# Decision variables for the final owner and class of each building
final_owner = {b: Const(f"final_owner_{b}", StringSort()) for b in buildings}
final_class = {b: Int(f"final_class_{b}") for b in buildings}

# Helper function to convert company names to Z3 constants
company_const = {c: String(c) for c in companies}

# Initialize final_owner and final_class to initial values
for b in buildings:
    solver.add(final_owner[b] == company_const[current_owner[b]])
    solver.add(final_class[b] == current_class[b])

# Define the final counts of buildings of each class for each company
final_counts = {
    (c, cls): Int(f"final_counts_{c}_{cls}") for c in companies for cls in building_classes
}

# Initialize final_counts to the initial counts
initial_counts = {
    ("RealProp", 1): 1,
    ("RealProp", 2): 0,
    ("RealProp", 3): 2,
    ("Southco", 1): 1,
    ("Southco", 2): 1,
    ("Southco", 3): 0,
    ("Trustcorp", 1): 0,
    ("Trustcorp", 2): 3,
    ("Trustcorp", 3): 0,
}

# Calculate final_counts based on final_owner and final_class
for c in companies:
    for cls in building_classes:
        solver.add(final_counts[(c, cls)] == Sum([
            If(final_owner[b] == company_const[c], If(final_class[b] == cls, 1, 0), 0)
            for b in buildings
        ]))

# Trade rules:
# 1. Trading one building for one other building of the same class: No change in counts.
# 2. Trading one class 1 building for two class 2 buildings: Decrease class 1 by 1, increase class 2 by 2.
# 3. Trading one class 2 building for two class 3 buildings: Decrease class 2 by 1, increase class 3 by 2.

# We will model the trades as constraints on the final counts.
# Let's define the number of trades of each type for each company.
# For simplicity, we will assume that trades can happen in any order and any number of times.

# Let's define the number of class 1 buildings traded by each company (Trade Rule 2)
traded_class1 = {c: Int(f"traded_class1_{c}") for c in companies}

# Let's define the number of class 2 buildings traded by each company (Trade Rule 3)
traded_class2 = {c: Int(f"traded_class2_{c}") for c in companies}

# Constraints on traded buildings:
# The number of class 1 buildings traded cannot exceed the initial number of class 1 buildings owned by the company.
solver.add(traded_class1["RealProp"] <= initial_counts[("RealProp", 1)])
solver.add(traded_class1["Southco"] <= initial_counts[("Southco", 1)])
solver.add(traded_class1["Trustcorp"] <= initial_counts[("Trustcorp", 1)])

# The number of class 2 buildings traded cannot exceed the initial number of class 2 buildings owned by the company.
solver.add(traded_class2["RealProp"] <= initial_counts[("RealProp", 2)])
solver.add(traded_class2["Southco"] <= initial_counts[("Southco", 2)])
solver.add(traded_class2["Trustcorp"] <= initial_counts[("Trustcorp", 2)])

# Constraints on final counts based on trades:
# For each company, the final number of class 2 buildings is equal to the initial number plus 2 times the number of class 1 buildings traded minus the number of class 2 buildings traded.
# For each company, the final number of class 3 buildings is equal to the initial number plus 2 times the number of class 2 buildings traded.

solver.add(final_counts[("RealProp", 2)] == initial_counts[("RealProp", 2)] + 2 * traded_class1["RealProp"] - traded_class2["RealProp"])
solver.add(final_counts[("RealProp", 3)] == initial_counts[("RealProp", 3)] + 2 * traded_class2["RealProp"])

solver.add(final_counts[("Southco", 2)] == initial_counts[("Southco", 2)] + 2 * traded_class1["Southco"] - traded_class2["Southco"])
solver.add(final_counts[("Southco", 3)] == initial_counts[("Southco", 3)] + 2 * traded_class2["Southco"])

solver.add(final_counts[("Trustcorp", 2)] == initial_counts[("Trustcorp", 2)] + 2 * traded_class1["Trustcorp"] - traded_class2["Trustcorp"])
solver.add(final_counts[("Trustcorp", 3)] == initial_counts[("Trustcorp", 3)] + 2 * traded_class2["Trustcorp"])

# Constraint: Trustcorp owns no class 2 buildings after trades
solver.add(final_counts[("Trustcorp", 2)] == 0)

# Now, evaluate the multiple choice options
found_options = []

# Option A: RealProp owns a class 1 building
# This means that the Garza Tower is still owned by RealProp in the final state.
opt_a_constr = (final_owner["Garza Tower"] == company_const["RealProp"])
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Southco owns only class 2 buildings
# This means Southco has no class 1 or class 3 buildings in the final state.
opt_b_constr = And(
    final_counts[("Southco", 1)] == 0,
    final_counts[("Southco", 2)] > 0,
    final_counts[("Southco", 3)] == 0
)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Southco has made at least one trade with Trustcorp
# This is modeled as: Southco traded at least one building, or Trustcorp traded at least one building.
opt_c_constr = Or(
    traded_class1["Southco"] > 0,
    traded_class2["Southco"] > 0,
    traded_class1["Trustcorp"] > 0,
    traded_class2["Trustcorp"] > 0
)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Trustcorp owns the Garza Tower
opt_d_constr = (final_owner["Garza Tower"] == company_const["Trustcorp"])
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Trustcorp owns the Zimmer House
opt_e_constr = (final_owner["Zimmer House"] == company_const["Trustcorp"])
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")