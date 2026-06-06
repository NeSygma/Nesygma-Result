from z3 import *

# ============================================================
# Part 1: Abstract trade-count model for Trustcorp
# ============================================================
# Trustcorp starts with (class1=0, class2=3, class3=0)
# Trade types involving Trustcorp:
#   a = type-3 forward: give 1 class2, get 2 class3  (net: -1 c2, +2 c3)
#   b = type-2 backward: give 2 class2, get 1 class1 (net: -2 c2, +1 c1)
#   c = type-3 backward: give 2 class3, get 1 class2  (net: +1 c2, -2 c3)
#   d = type-2 forward: give 1 class1, get 2 class2   (net: +2 c2, -1 c1)

print("=== Part 1: Verify Trustcorp's final class counts ===")
a, b, c, d = Ints('a b c d')
s1 = Solver()
s1.add(a >= 0, b >= 0, c >= 0, d >= 0)
# Trustcorp class2 = 3 - a - 2b + c + 2d = 0
s1.add(3 - a - 2*b + c + 2*d == 0)
# Trustcorp class1 = b - d >= 0
s1.add(b - d >= 0)
# Trustcorp class3 = 2a - 2c >= 0
s1.add(2*a - 2*c >= 0)
# Total class3 in system = 2, so Trustcorp class3 <= 2
s1.add(2*a - 2*c <= 2)

# Verify class3 must be exactly 2
s1.push()
s1.add(2*a - 2*c != 2)
r = s1.check()
s1.pop()
if r == unsat:
    print("Verified: Trustcorp MUST have exactly 2 class 3 buildings")
else:
    print(f"UNEXPECTED: class3 != 2 is possible: {s1.model()}")

# Verify class1 must be exactly 1
s1.push()
s1.add(b - d != 1)
r = s1.check()
s1.pop()
if r == unsat:
    print("Verified: Trustcorp MUST have exactly 1 class 1 building")
else:
    print(f"UNEXPECTED: class1 != 1 is possible: {s1.model()}")

# ============================================================
# Part 2: Individual building model + answer choice checking
# ============================================================
print("\n=== Part 2: Answer choice verification ===")

buildings = ['Garza', 'Flores', 'Lynch', 'King', 'Meyer', 'Ortiz', 'Yates', 'Zimmer']
bclass = {
    'Garza': 1, 'Flores': 1,
    'Lynch': 2, 'King': 2, 'Meyer': 2, 'Ortiz': 2,
    'Yates': 3, 'Zimmer': 3
}
# 0=RealProp, 1=Southco, 2=Trustcorp
owner = {b: Int(f'owner_{b}') for b in buildings}

s2 = Solver()
for b in buildings:
    s2.add(Or(owner[b] == 0, owner[b] == 1, owner[b] == 2))

# Trustcorp owns no class 2 buildings
for b in buildings:
    if bclass[b] == 2:
        s2.add(owner[b] != 2)

# Trustcorp has exactly 1 class 1 building (derived above)
s2.add(Sum([If(owner[b] == 2, 1, 0) for b in buildings if bclass[b] == 1]) == 1)
# Trustcorp has exactly 2 class 3 buildings (derived above)
s2.add(Sum([If(owner[b] == 2, 1, 0) for b in buildings if bclass[b] == 3]) == 2)

# Define answer choices
# (A) RealProp owns a class 1 building
opt_a = Or([owner[b] == 0 for b in buildings if bclass[b] == 1])

# (B) Southco owns only class 2 buildings (at least one, all class 2)
southco_has = Or([owner[b] == 1 for b in buildings])
southco_only_c2 = And([Implies(owner[b] == 1, bclass[b] == 2) for b in buildings])
opt_b = And(southco_has, southco_only_c2)

# (C) Southco has made at least one trade with Trustcorp
# This is about the trade PROCESS, not just final state.
# Counterexample: Trustcorp trades King->RealProp for Yates+Zimmer (type3),
# then Meyer+Ortiz->RealProp for Garza (type2). Southco never trades.
# So (C) is NOT necessarily true.

# (D) Trustcorp owns the Garza Tower
opt_d = owner['Garza'] == 2

# (E) Trustcorp owns the Zimmer House
opt_e = owner['Zimmer'] == 2

found_options = []
for letter, constr in [('A', opt_a), ('B', opt_b), ('D', opt_d), ('E', opt_e)]:
    s2.push()
    s2.add(Not(constr))
    r = s2.check()
    if r == unsat:
        found_options.append(letter)
        print(f"Option {letter}: MUST be true (negation is unsat)")
    else:
        m = s2.model()
        names = {0: 'RealProp', 1: 'Southco', 2: 'Trustcorp'}
        print(f"Option {letter}: can be FALSE")
        for b in buildings:
            print(f"  {b:10s} class{bclass[b]} -> {names[int(str(m[owner[b]]))]}")
    s2.pop()

# Option C handled by counterexample argument
print(f"Option C: can be FALSE (Trustcorp can trade exclusively with RealProp)")

print(f"\nMust-be-true options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")