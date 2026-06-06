from z3 import *

#--- Declare Boolean variables ---
spill = Bool('spill')
tidy = Bool('tidy')
clumsy = Bool('clumsy')
goes_out = Bool('goes_out')
cleanly = Bool('cleanly')
valu_order_spotless = Bool('valu_order_spotless')
family_prioritizes = Bool('family_prioritizes')

#--- Premises ---
solver = Solver()

# 1. spill -> not tidy
solver.add(Implies(spill, Not(tidy)))

# 2. (clumsy ∧ goes_out) -> spill
solver.add(Implies(And(clumsy, goes_out), spill))

# 3. cleanly -> tidy
solver.add(Implies(cleanly, tidy))

# 4. valu_order_spotless -> cleanly
solver.add(Implies(valu_order_spotless, cleanly))

# 5. family_prioritizes -> valu_order_spotless
solver.add(Implies(family_prioritizes, valu_order_spotless))

#--- Peter's condition (exclusive or) ---
pc1 = And(spill, cleanly)          # spill ∧ cleanly
pc2 = And(Not(spill), Not(cleanly))# ¬spill ∧ ¬cleanly
# Exactly one of pc1, pc2 must hold
solver.add(Or(pc1, pc2))
solver.add(Not(And(pc1, pc2)))

#--- Conclusion components ---
c1 = And(clumsy, goes_out, family_prioritizes)          # clumsy ∧ goes_out ∧ family_prioritizes
c2 = And(Not(clumsy), Not(family_prioritizes))          # ¬clumsy ∧ ¬family_prioritizes
conclusion = Or(c1, c2)

#--- Check if premises entail NOT(conclusion) (i.e., conclusion is always true) ---
solver_not_concl = Solver()
solver_not_concl.add(solver.assertions())  # copy all premises
solver_not_concl.add(Not(conclusion))      # add ¬conclusion
sat_not_concl = solver_not_concl.check() == sat

#--- Check if premises entail conclusion (i.e., conclusion is always false) ---
solver_concl = Solver()
solver_concl.add(solver.assertions())
solver_concl.add(conclusion)               # add conclusion
sat_concl = solver_concl.check() == sat

#--- Determine result ---
if sat_not_concl and not sat_concl:
    # ¬conclusion is entailed → conclusion is True in all models
    print("STATUS: proved")
    print("RESULT: True")
elif not sat_not_concl and sat_concl:
    # conclusion is entailed → conclusion is False in all models
    print("STATUS: proved")
    print("RESULT: False")
else:
    # Both ¬conclusion and conclusion are possible → uncertain
    print("STATUS: unknown")
    print("RESULT: Uncertain")