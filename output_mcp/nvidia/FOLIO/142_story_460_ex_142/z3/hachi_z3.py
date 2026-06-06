from z3 import *
# Declare Boolean variables
A = Bool('A')
E = Bool('E')
G = Bool('G')
FF = Bool('FF')
HF = Bool('HF')
C = Bool('C')
# Premises
premises = [
    Or(Not(A), C),           # 1. A -> C
    Or(Not(E), Not(C)),      # 2. E -> not C
    Or(Not(G), A),           # 3. G -> A
    Or(Not(FF), G),          # 4. FF -> G
    Or(Not(HF), FF),         # 5. HF -> FF
    Or(FF, A)                # 6. FF ∨ A
]
# Conclusion: (E ∧ HF) ∨ (¬E ∧ ¬HF)
concl = Or(And(E, HF), And(Not(E), Not(HF)))
# Check premises ∧ concl
solver1 = Solver()
solver1.add(premises)
solver1.add(concl)
result1 = solver1.check()
# Check premises ∧ ¬concl
solver2 = Solver()
solver2.add(premises)
solver2.add(Not(concl))
result2 = solver2.check()
# Determine outcome
if result1 == sat and result2 == unsat:
    print("STATUS: proved")
    print("CONCLUSION: True")
elif result1 == unsat and result2 == sat:
    print("STATUS: proved")
    print("CONCLUSION: False")
elif result1 == sat and result2 == sat:
    print("STATUS: proved")
    print("CONCLUSION: Uncertain")
else:
    print("STATUS: proved")
    print("CONCLUSION: False")