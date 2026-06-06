from z3 import *

# Building IDs and their classes
# Garza Tower: 0 (class 1)
# Yates House: 1 (class 3)
# Zimmer House: 2 (class 3)
# Flores Tower: 3 (class 1)
# Lynch Building: 4 (class 2)
# King Building: 5 (class 2)
# Meyer Building: 6 (class 2)
# Ortiz Building: 7 (class 2)

def class_of(b):
    return If(b == 0, 1,  # Garza Tower
              If(b == 1, 3,  # Yates House
                If(b == 2, 3,  # Zimmer House
                  If(b == 3, 1,  # Flores Tower
                    If(b == 4, 2,  # Lynch Building
                      If(b == 5, 2,  # King Building
                        If(b == 6, 2,  # Meyer Building
                          If(b == 7, 2, 0)  # Ortiz Building
                        )  # Meyer
                      )  # King
                    )  # Lynch
                  )  # Flores
                )  # Zimmer
              )  # Yates
            )  # Garza

# Initial ownership (as sets of building IDs)
initial_realprop = [0, 1, 2]  # Garza, Yates, Zimmer
initial_southco = [3, 4]       # Flores, Lynch
initial_trustcorp = [5, 6, 7]  # King, Meyer, Ortiz

# Option A
opt_a_realprop = [3, 0]        # Flores Tower, Garza Tower
opt_a_southco = [4, 1, 2]      # Lynch, Yates, Zimmer
opt_a_trustcorp = [5, 6, 7]    # King, Meyer, Ortiz

# Option B
opt_b_realprop = [0, 5, 7]     # Garza, King, Ortiz
opt_b_southco = [3, 4]         # Flores, Lynch
opt_b_trustcorp = [6, 1, 2]    # Meyer, Yates, Zimmer

# Option C
opt_c_realprop = [0, 4]        # Garza, Lynch
opt_c_southco = [3, 1, 2]      # Flores, Yates, Zimmer
opt_c_trustcorp = [5, 6, 7]    # King, Meyer, Ortiz

# Option D
opt_d_realprop = [0, 6, 1]     # Garza, Meyer, Yates
opt_d_southco = [3, 4]         # Flores, Lynch
opt_d_trustcorp = [5, 7, 2]    # King, Ortiz, Zimmer

# Option E
opt_e_realprop = [0, 1, 2]     # Garza, Yates, Zimmer
opt_e_southco = [4, 7]         # Lynch, Ortiz
opt_e_trustcorp = [3, 5, 6]    # Flores, King, Meyer

# Helper to check if a list contains a building (Z3 expression)
def list_contains(lst, b):
    return Or([x == b for x in lst])

# Helper to count occurrences of a building in a list (Z3 expression)
def list_count(lst, b):
    return Sum([If(x == b, 1, 0) for x in lst])

# Helper to check if a list is equal to another (Z3 expression)
def lists_equal(l1, l2):
    return And(
        And([list_contains(l1, b) for b in l2]),
        And([list_contains(l2, b) for b in l1]),
        length_eq(l1, l2)
    )

# Helper to check if two lists have the same length
def length_eq(l1, l2):
    return length(l1) == length(l2)

def length(lst):
    return Sum([If(Not(x == -1), 1, 0) for x in lst])

# Helper to get the set difference (buildings in initial but not in post)
def removed_buildings(initial, post):
    return [b for b in initial if not any(b == pb for pb in post)]

# Helper to get the set difference (buildings in post but not in initial)
def added_buildings(initial, post):
    return [b for b in post if not any(b == ib for ib in initial)]

# Check if a trade is valid for a company
# Returns a Z3 expression that is True if the trade is valid
def is_valid_trade_expr(initial, post):
    removed = removed_buildings(initial, post)
    added = added_buildings(initial, post)
    
    # Case 1: Trade one building for one other building of the same class
    case1 = And(
        length(removed) == 1,
        length(added) == 1,
        class_of(removed[0]) == class_of(added[0])
    )
    
    # Case 2: Trade one class 1 building for two class 2 buildings
    case2 = And(
        length(removed) == 1,
        length(added) == 2,
        class_of(removed[0]) == 1,
        class_of(added[0]) == 2,
        class_of(added[1]) == 2
    )
    
    # Case 3: Trade one class 2 building for two class 3 buildings
    case3 = And(
        length(removed) == 1,
        length(added) == 2,
        class_of(removed[0]) == 2,
        class_of(added[0]) == 3,
        class_of(added[1]) == 3
    )
    
    return Or(case1, case2, case3)

# Now, for each option, check if the post-trade state is reachable by exactly one trade
solver = Solver()

# We will test each option independently
found_options = []

# Option A
solver.push()
# Assert that the post-trade ownership matches option A
solver.add(And(
    lists_equal(opt_a_realprop, [3, 0]),
    lists_equal(opt_a_southco, [4, 1, 2]),
    lists_equal(opt_a_trustcorp, [5, 6, 7])
))
# Assert that the change from initial to option A is a valid single trade for exactly one company
# (i.e., one company has a valid trade, others remain unchanged)
realprop_trade_valid = is_valid_trade_expr(initial_realprop, opt_a_realprop)
southco_trade_valid = is_valid_trade_expr(initial_southco, opt_a_southco)
trustcorp_trade_valid = is_valid_trade_expr(initial_trustcorp, opt_a_trustcorp)

# Exactly one company has a valid trade, others are unchanged
if solver.check(And(
    Or(realprop_trade_valid, southco_trade_valid, trustcorp_trade_valid),
    Not(And(realprop_trade_valid, southco_trade_valid)),
    Not(And(realprop_trade_valid, trustcorp_trade_valid)),
    Not(And(southco_trade_valid, trustcorp_trade_valid))
)) == sat:
    found_options.append("A")

solver.pop()

# Option B
solver.push()
solver.add(And(
    lists_equal(opt_b_realprop, [0, 5, 7]),
    lists_equal(opt_b_southco, [3, 4]),
    lists_equal(opt_b_trustcorp, [6, 1, 2])
))
realprop_trade_valid = is_valid_trade_expr(initial_realprop, opt_b_realprop)
southco_trade_valid = is_valid_trade_expr(initial_southco, opt_b_southco)
trustcorp_trade_valid = is_valid_trade_expr(initial_trustcorp, opt_b_trustcorp)

if solver.check(And(
    Or(realprop_trade_valid, southco_trade_valid, trustcorp_trade_valid),
    Not(And(realprop_trade_valid, southco_trade_valid)),
    Not(And(realprop_trade_valid, trustcorp_trade_valid)),
    Not(And(southco_trade_valid, trustcorp_trade_valid))
)) == sat:
    found_options.append("B")

solver.pop()

# Option C
solver.push()
solver.add(And(
    lists_equal(opt_c_realprop, [0, 4]),
    lists_equal(opt_c_southco, [3, 1, 2]),
    lists_equal(opt_c_trustcorp, [5, 6, 7])
))
realprop_trade_valid = is_valid_trade_expr(initial_realprop, opt_c_realprop)
southco_trade_valid = is_valid_trade_expr(initial_southco, opt_c_southco)
trustcorp_trade_valid = is_valid_trade_expr(initial_trustcorp, opt_c_trustcorp)

if solver.check(And(
    Or(realprop_trade_valid, southco_trade_valid, trustcorp_trade_valid),
    Not(And(realprop_trade_valid, southco_trade_valid)),
    Not(And(realprop_trade_valid, trustcorp_trade_valid)),
    Not(And(southco_trade_valid, trustcorp_trade_valid))
)) == sat:
    found_options.append("C")

solver.pop()

# Option D
solver.push()
solver.add(And(
    lists_equal(opt_d_realprop, [0, 6, 1]),
    lists_equal(opt_d_southco, [3, 4]),
    lists_equal(opt_d_trustcorp, [5, 7, 2])
))
realprop_trade_valid = is_valid_trade_expr(initial_realprop, opt_d_realprop)
southco_trade_valid = is_valid_trade_expr(initial_southco, opt_d_southco)
trustcorp_trade_valid = is_valid_trade_expr(initial_trustcorp, opt_d_trustcorp)

if solver.check(And(
    Or(realprop_trade_valid, southco_trade_valid, trustcorp_trade_valid),
    Not(And(realprop_trade_valid, southco_trade_valid)),
    Not(And(realprop_trade_valid, trustcorp_trade_valid)),
    Not(And(southco_trade_valid, trustcorp_trade_valid))
)) == sat:
    found_options.append("D")

solver.pop()

# Option E
solver.push()
solver.add(And(
    lists_equal(opt_e_realprop, [0, 1, 2]),
    lists_equal(opt_e_southco, [4, 7]),
    lists_equal(opt_e_trustcorp, [3, 5, 6])
))
realprop_trade_valid = is_valid_trade_expr(initial_realprop, opt_e_realprop)
southco_trade_valid = is_valid_trade_expr(initial_southco, opt_e_southco)
trustcorp_trade_valid = is_valid_trade_expr(initial_trustcorp, opt_e_trustcorp)

if solver.check(And(
    Or(realprop_trade_valid, southco_trade_valid, trustcorp_trade_valid),
    Not(And(realprop_trade_valid, southco_trade_valid)),
    Not(And(realprop_trade_valid, trustcorp_trade_valid)),
    Not(And(southco_trade_valid, trustcorp_trade_valid))
)) == sat:
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