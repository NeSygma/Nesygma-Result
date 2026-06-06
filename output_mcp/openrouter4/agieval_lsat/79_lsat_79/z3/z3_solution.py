from z3 import *

# Define Business sort
Business, (O, P, R1, R2, S, T, V) = EnumSort('Business', ['O', 'P', 'R1', 'R2', 'S', 'T', 'V'])

# Base constraints function
def get_base_solver():
    s = Solver()
    pos = Function('pos', Business, IntSort())
    
    for b in [O, P, R1, R2, S, T, V]:
        s.add(pos(b) >= 1, pos(b) <= 7)
    
    s.add(Distinct([pos(b) for b in [O, P, R1, R2, S, T, V]]))
    
    # Constraint 1: Pharmacy at one end, one restaurant at the other
    s.add(Or(
        And(pos(P) == 1, Or(pos(R1) == 7, pos(R2) == 7)),
        And(pos(P) == 7, Or(pos(R1) == 1, pos(R2) == 1))
    ))
    
    # Constraint 2: Two restaurants separated by at least 2 other businesses
    s.add(Or(pos(R1) - pos(R2) >= 3, pos(R2) - pos(R1) >= 3))
    
    # Constraint 3: Pharmacy next to optometrist or veterinarian
    s.add(Or(
        Abs(pos(P) - pos(O)) == 1,
        Abs(pos(P) - pos(V)) == 1
    ))
    
    # Constraint 4: Toy store not next to veterinarian
    s.add(Not(Abs(pos(T) - pos(V)) == 1))
    
    # Additional: Optometrist next to shoe store
    s.add(Abs(pos(O) - pos(S)) == 1)
    
    # Define business_at function
    business_at = Function('business_at', IntSort(), Business)
    for b in [O, P, R1, R2, S, T, V]:
        s.add(business_at(pos(b)) == b)
    
    # Left and right positions of the O-S pair
    min_os = If(pos(O) < pos(S), pos(O), pos(S))
    max_os = If(pos(O) < pos(S), pos(S), pos(O))
    
    left_pos = min_os - 1
    right_pos = max_os + 1
    
    # O-S pair not at ends (so both sides exist)
    s.add(min_os > 1)
    s.add(max_os < 7)
    
    left_biz = business_at(left_pos)
    right_biz = business_at(right_pos)
    
    return s, left_biz, right_biz

# Check each option
found_options = []

# Option A: pharmacy and a restaurant
s, left_biz, right_biz = get_base_solver()
# Negation of option A: NOT((left is P and right is a restaurant) or (left is a restaurant and right is P))
s.add(Not(Or(
    And(left_biz == P, Or(right_biz == R1, right_biz == R2)),
    And(Or(left_biz == R1, left_biz == R2), right_biz == P)
)))
resA = s.check()
print(f"Option A negation check: {resA}")

# Option B: pharmacy and the toy store
s, left_biz, right_biz = get_base_solver()
s.add(Not(Or(
    And(left_biz == P, right_biz == T),
    And(left_biz == T, right_biz == P)
)))
resB = s.check()
print(f"Option B negation check: {resB}")

# Option C: the two restaurants
s, left_biz, right_biz = get_base_solver()
s.add(Not(Or(
    And(left_biz == R1, right_biz == R2),
    And(left_biz == R2, right_biz == R1)
)))
resC = s.check()
print(f"Option C negation check: {resC}")

# Option D: a restaurant and the toy store
s, left_biz, right_biz = get_base_solver()
s.add(Not(Or(
    And(Or(left_biz == R1, left_biz == R2), right_biz == T),
    And(left_biz == T, Or(right_biz == R1, right_biz == R2))
)))
resD = s.check()
print(f"Option D negation check: {resD}")

# Option E: a restaurant and the veterinarian
s, left_biz, right_biz = get_base_solver()
s.add(Not(Or(
    And(Or(left_biz == R1, left_biz == R2), right_biz == V),
    And(left_biz == V, Or(right_biz == R1, right_biz == R2))
)))
resE = s.check()
print(f"Option E negation check: {resE}")

# Now determine which options MUST be true
if resA == unsat:
    found_options.append("A")
if resB == unsat:
    found_options.append("B")
if resC == unsat:
    found_options.append("C")
if resD == unsat:
    found_options.append("D")
if resE == unsat:
    found_options.append("E")

print(f"\nFound options (must be): {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")