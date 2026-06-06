from z3 import *

# Define building IDs and their classes
# Garza Tower: 0 (class 1)
# Yates House: 1 (class 3)
# Zimmer House: 2 (class 3)
# Flores Tower: 3 (class 1)
# Lynch Building: 4 (class 2)
# King Building: 5 (class 2)
# Meyer Building: 6 (class 2)
# Ortiz Building: 7 (class 2)

# Helper function to get class of a building
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

# Define the post-trade ownership for each option
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

# Helper to check if a trade of type 1 (same class) is possible
# trade_type1: remove b1, add b2, where class(b1) == class(b2)
# trade_type2: remove b1 (class 1), add b2, b3 (class 2)
# trade_type3: remove b1 (class 2), add b2, b3 (class 3)

def is_valid_single_trade(initial, post):
    # Case 1: Trade one building for one other building of the same class
    # The length of the list remains the same
    if len(initial) == len(post):
        # Exactly one building is removed and one is added, and they are of the same class
        # Find the removed and added buildings
        removed = [b for b in initial if not any(b == pb for pb in post)]
        added = [b for b in post if not any(b == ib for ib in initial)]
        if len(removed) == 1 and len(added) == 1:
            b_removed = removed[0]
            b_added = added[0]
            return class_of(b_removed) == class_of(b_added)
    # Case 2: Trade one class 1 building for two class 2 buildings
    # The length increases by 1
    elif len(post) == len(initial) + 1:
        removed = [b for b in initial if not any(b == pb for pb in post)]
        added = [b for b in post if not any(b == ib for ib in initial)]
        if len(removed) == 1 and len(added) == 2:
            b_removed = removed[0]
            b_added1, b_added2 = added[0], added[1]
            return And(
                class_of(b_removed) == 1,
                class_of(b_added1) == 2,
                class_of(b_added2) == 2
            )
    # Case 3: Trade one class 2 building for two class 3 buildings
    # The length increases by 1
    elif len(post) == len(initial) + 1:
        removed = [b for b in initial if not any(b == pb for pb in post)]
        added = [b for b in post if not any(b == ib for ib in initial)]
        if len(removed) == 1 and len(added) == 2:
            b_removed = removed[0]
            b_added1, b_added2 = added[0], added[1]
            return And(
                class_of(b_removed) == 2,
                class_of(b_added1) == 3,
                class_of(b_added2) == 3
            )
    return False

# Now, for each option, check if the post-trade state is reachable by exactly one trade
solver = Solver()

# We will test each option independently
found_options = []

# Option A
solver.push()
# Assert that the post-trade ownership matches option A
solver.add(And(
    list_contains(opt_a_realprop, 3),  # Flores Tower
    list_contains(opt_a_realprop, 0),  # Garza Tower
    list_count(opt_a_realprop, 3) == 1,
    list_count(opt_a_realprop, 0) == 1,
    list_count(opt_a_realprop, 1) == 0,
    list_count(opt_a_realprop, 2) == 0,
    
    list_contains(opt_a_southco, 4),  # Lynch
    list_contains(opt_a_southco, 1),  # Yates
    list_contains(opt_a_southco, 2),  # Zimmer
    list_count(opt_a_southco, 4) == 1,
    list_count(opt_a_southco, 1) == 1,
    list_count(opt_a_southco, 2) == 1,
    
    list_contains(opt_a_trustcorp, 5),  # King
    list_contains(opt_a_trustcorp, 6),  # Meyer
    list_contains(opt_a_trustcorp, 7),  # Ortiz
    list_count(opt_a_trustcorp, 5) == 1,
    list_count(opt_a_trustcorp, 6) == 1,
    list_count(opt_a_trustcorp, 7) == 1
))
# Assert that the change from initial to option A is a valid single trade for each company
if is_valid_single_trade(initial_realprop, opt_a_realprop) and \
   is_valid_single_trade(initial_southco, opt_a_southco) and \
   is_valid_single_trade(initial_trustcorp, opt_a_trustcorp):
    if solver.check() == sat:
        found_options.append("A")

solver.pop()

# Option B
solver.push()
solver.add(And(
    list_contains(opt_b_realprop, 0),  # Garza
    list_contains(opt_b_realprop, 5),  # King
    list_contains(opt_b_realprop, 7),  # Ortiz
    list_count(opt_b_realprop, 0) == 1,
    list_count(opt_b_realprop, 5) == 1,
    list_count(opt_b_realprop, 7) == 1,
    
    list_contains(opt_b_southco, 3),  # Flores
    list_contains(opt_b_southco, 4),  # Lynch
    list_count(opt_b_southco, 3) == 1,
    list_count(opt_b_southco, 4) == 1,
    
    list_contains(opt_b_trustcorp, 6),  # Meyer
    list_contains(opt_b_trustcorp, 1),  # Yates
    list_contains(opt_b_trustcorp, 2),  # Zimmer
    list_count(opt_b_trustcorp, 6) == 1,
    list_count(opt_b_trustcorp, 1) == 1,
    list_count(opt_b_trustcorp, 2) == 1
))
if is_valid_single_trade(initial_realprop, opt_b_realprop) and \
   is_valid_single_trade(initial_southco, opt_b_southco) and \
   is_valid_single_trade(initial_trustcorp, opt_b_trustcorp):
    if solver.check() == sat:
        found_options.append("B")

solver.pop()

# Option C
solver.push()
solver.add(And(
    list_contains(opt_c_realprop, 0),  # Garza
    list_contains(opt_c_realprop, 4),  # Lynch
    list_count(opt_c_realprop, 0) == 1,
    list_count(opt_c_realprop, 4) == 1,
    list_count(opt_c_realprop, 1) == 0,
    list_count(opt_c_realprop, 2) == 0,
    
    list_contains(opt_c_southco, 3),  # Flores
    list_contains(opt_c_southco, 1),  # Yates
    list_contains(opt_c_southco, 2),  # Zimmer
    list_count(opt_c_southco, 3) == 1,
    list_count(opt_c_southco, 1) == 1,
    list_count(opt_c_southco, 2) == 1,
    
    list_contains(opt_c_trustcorp, 5),  # King
    list_contains(opt_c_trustcorp, 6),  # Meyer
    list_contains(opt_c_trustcorp, 7),  # Ortiz
    list_count(opt_c_trustcorp, 5) == 1,
    list_count(opt_c_trustcorp, 6) == 1,
    list_count(opt_c_trustcorp, 7) == 1
))
if is_valid_single_trade(initial_realprop, opt_c_realprop) and \
   is_valid_single_trade(initial_southco, opt_c_southco) and \
   is_valid_single_trade(initial_trustcorp, opt_c_trustcorp):
    if solver.check() == sat:
        found_options.append("C")

solver.pop()

# Option D
solver.push()
solver.add(And(
    list_contains(opt_d_realprop, 0),  # Garza
    list_contains(opt_d_realprop, 6),  # Meyer
    list_contains(opt_d_realprop, 1),  # Yates
    list_count(opt_d_realprop, 0) == 1,
    list_count(opt_d_realprop, 6) == 1,
    list_count(opt_d_realprop, 1) == 1,
    
    list_contains(opt_d_southco, 3),  # Flores
    list_contains(opt_d_southco, 4),  # Lynch
    list_count(opt_d_southco, 3) == 1,
    list_count(opt_d_southco, 4) == 1,
    
    list_contains(opt_d_trustcorp, 5),  # King
    list_contains(opt_d_trustcorp, 7),  # Ortiz
    list_contains(opt_d_trustcorp, 2),  # Zimmer
    list_count(opt_d_trustcorp, 5) == 1,
    list_count(opt_d_trustcorp, 7) == 1,
    list_count(opt_d_trustcorp, 2) == 1
))
if is_valid_single_trade(initial_realprop, opt_d_realprop) and \
   is_valid_single_trade(initial_southco, opt_d_southco) and \
   is_valid_single_trade(initial_trustcorp, opt_d_trustcorp):
    if solver.check() == sat:
        found_options.append("D")

solver.pop()

# Option E
solver.push()
solver.add(And(
    list_contains(opt_e_realprop, 0),  # Garza
    list_contains(opt_e_realprop, 1),  # Yates
    list_contains(opt_e_realprop, 2),  # Zimmer
    list_count(opt_e_realprop, 0) == 1,
    list_count(opt_e_realprop, 1) == 1,
    list_count(opt_e_realprop, 2) == 1,
    
    list_contains(opt_e_southco, 4),  # Lynch
    list_contains(opt_e_southco, 7),  # Ortiz
    list_count(opt_e_southco, 4) == 1,
    list_count(opt_e_southco, 7) == 1,
    
    list_contains(opt_e_trustcorp, 3),  # Flores
    list_contains(opt_e_trustcorp, 5),  # King
    list_contains(opt_e_trustcorp, 6),  # Meyer
    list_count(opt_e_trustcorp, 3) == 1,
    list_count(opt_e_trustcorp, 5) == 1,
    list_count(opt_e_trustcorp, 6) == 1
))
if is_valid_single_trade(initial_realprop, opt_e_realprop) and \
   is_valid_single_trade(initial_southco, opt_e_southco) and \
   is_valid_single_trade(initial_trustcorp, opt_e_trustcorp):
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