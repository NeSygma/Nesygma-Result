from z3 import *

solver = Solver()

# Boolean variables: True means on the team
Myers = Bool('Myers')
Ortega = Bool('Ortega')
Paine = Bool('Paine')
Schmidt = Bool('Schmidt')
Thomson = Bool('Thomson')
Wong = Bool('Wong')
Yoder = Bool('Yoder')
Zayre = Bool('Zayre')

employees = [Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre]

# Constraint 1: If Myers is on the team, neither Ortega nor Paine can be
solver.add(Implies(Myers, And(Not(Ortega), Not(Paine))))

# Constraint 2: If Schmidt is on the team, both Paine and Thomson must be
solver.add(Implies(Schmidt, And(Paine, Thomson)))

# Constraint 3: If Wong is on the team, both Myers and Yoder must be
solver.add(Implies(Wong, And(Myers, Yoder)))

# Constraint 4: At least 4 employees on the team
solver.add(Sum([If(e, 1, 0) for e in employees]) >= 4)

# Premise: Yoder is NOT on the team
solver.add(Not(Yoder))

# Now test each option: can each person be ON the team?
# The EXCEPT answer is the one that CANNOT be on the team.

found_options = []

# Option A: Zayre can be on the team
solver.push()
solver.add(Zayre)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Thomson can be on the team
solver.push()
solver.add(Thomson)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Paine can be on the team
solver.push()
solver.add(Paine)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Ortega can be on the team
solver.push()
solver.add(Ortega)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Myers can be on the team
solver.push()
solver.add(Myers)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# The EXCEPT answer is the one NOT in found_options
# We need exactly 4 options to be possible (all except the answer)
print(f"Options that CAN be on the team: {found_options}")
print(f"Options that CANNOT be on the team: {[l for l in ['A','B','C','D','E'] if l not in found_options]}")

if len(found_options) == 4:
    except_answer = [l for l in ['A','B','C','D','E'] if l not in found_options][0]
    print("STATUS: sat")
    print(f"answer:{except_answer}")
elif len(found_options) > 4:
    print("STATUS: unsat")
    print(f"Refine: More than 4 options possible {found_options}")
elif len(found_options) < 4:
    print("STATUS: unsat")
    print(f"Refine: Fewer than 4 options possible {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")