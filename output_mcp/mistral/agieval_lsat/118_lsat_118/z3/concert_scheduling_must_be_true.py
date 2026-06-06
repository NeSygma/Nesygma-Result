from z3 import *

solver = Solver()

# Declare variables for each band's slot (1-6)
uneasy = Int('uneasy')
vegemite = Int('vegemite')
wellspring = Int('wellspring')
xpert = Int('xpert')
yardsign = Int('yardsign')
zircon = Int('zircon')

# All slots are between 1 and 6
solver.add(uneasy >= 1, uneasy <= 6)
solver.add(vegemite >= 1, vegemite <= 6)
solver.add(wellspring >= 1, wellspring <= 6)
solver.add(xpert >= 1, xpert <= 6)
solver.add(yardsign >= 1, yardsign <= 6)
solver.add(zircon >= 1, zircon <= 6)

# All slots are distinct
solver.add(Distinct(uneasy, vegemite, wellspring, xpert, yardsign, zircon))

# Given: Vegemite performs in slot three
solver.add(vegemite == 3)

# Constraints:
# Vegemite performs in an earlier slot than Zircon
solver.add(vegemite < zircon)
# Wellspring and Zircon each perform in an earlier slot than Xpert
solver.add(wellspring < xpert)
solver.add(zircon < xpert)
# Uneasy performs in one of the last three slots
solver.add(uneasy >= 4)
# Yardsign performs in one of the first three slots
solver.add(yardsign <= 3)

# Now test each option to see if it must be true
# For "must be true", we check if the negation is unsatisfiable
must_be_true = []

# Option A: Uneasy performs in an earlier slot than Xpert (uneasy < xpert)
# Negation: uneasy >= xpert
s_neg_a = Solver()
s_neg_a.add(solver.assertions())
s_neg_a.add(uneasy >= xpert)
if s_neg_a.check() == unsat:
    must_be_true.append("A")

# Option B: Wellspring performs in an earlier slot than zircon (wellspring < zircon)
# Negation: wellspring >= zircon
s_neg_b = Solver()
s_neg_b.add(solver.assertions())
s_neg_b.add(wellspring >= zircon)
if s_neg_b.check() == unsat:
    must_be_true.append("B")

# Option C: Xpert performs in an earlier slot than Uneasy (xpert < uneasy)
# Negation: xpert >= uneasy
s_neg_c = Solver()
s_neg_c.add(solver.assertions())
s_neg_c.add(xpert >= uneasy)
if s_neg_c.check() == unsat:
    must_be_true.append("C")

# Option D: Yardsign performs in an earlier slot than Wellspring (yardsign < wellspring)
# Negation: yardsign >= wellspring
s_neg_d = Solver()
s_neg_d.add(solver.assertions())
s_neg_d.add(yardsign >= wellspring)
if s_neg_d.check() == unsat:
    must_be_true.append("D")

# Option E: Zircon performs in an earlier slot than Uneasy (zircon < uneasy)
# Negation: zircon >= uneasy
s_neg_e = Solver()
s_neg_e.add(solver.assertions())
s_neg_e.add(zircon >= uneasy)
if s_neg_e.check() == unsat:
    must_be_true.append("E")

# Output result
if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")