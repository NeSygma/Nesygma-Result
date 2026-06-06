from z3 import *

# Declare boolean variables representing properties of Djokovic
gs = Bool('gs')  # Grand Slam champion
o = Bool('o')    # Oscar-nominated actor
p = Bool('p')    # Professional tennis player
a = Bool('a')    # Athlete
c = Bool('c')    # Celebrity
wp = Bool('wp')  # Well-paid
f = Bool('f')    # Famous
t = Bool('t')    # Lives in tax haven

solver1 = Solver()  # for premises ∧ t
solver2 = Solver()  # for premises ∧ ¬t

# Base constraints (apply to both solvers)
solver1.add(Or(gs, o))                     # Everyone at the mixer is GS or O
solver1.add(Implies(gs, p))                # GS at mixer → P
solver1.add(Implies(o, c))                 # O at mixer → C
solver1.add(Implies(p, a))                 # P at mixer → A
solver1.add(Implies(c, wp))                # C at mixer → WP
solver1.add(Implies(a, f))                 # A at mixer → F
solver1.add(Implies(f, wp))                # F at mixer → WP (conditional from premise 8)
solver1.add(Implies(wp, t))                # WP at mixer → T

solver2.add(Or(gs, o))
solver2.add(Implies(gs, p))
solver2.add(Implies(o, c))
solver2.add(Implies(p, a))
solver2.add(Implies(c, wp))
solver2.add(Implies(a, f))
solver2.add(Implies(f, wp))
solver2.add(Implies(wp, t))

# Case 1: premises ∧ t
solver1.add(t)
# Case 2: premises ∧ ¬t
solver2.add(Not(t))

# Check satisfiability
res1 = solver1.check()
res2 = solver2.check()

# Determine conclusion
if res1 == sat and res2 == unsat:
    print("STATUS: proved")
    print("CONCLUSION: False")
elif res1 == unsat and res2 == sat:
    print("STATUS: proved")
    print("CONCLUSION: True")
elif res1 == sat and res2 == sat:
    print("STATUS: proved")
    print("CONCLUSION: Uncertain")
elif res1 == unsat and res2 == unsat:
    print("STATUS: unknown")
    print("CONCLUSION: Inconsistent")
else:
    print("STATUS: unknown")