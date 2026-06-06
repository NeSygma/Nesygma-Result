from z3 import *

s = Solver()

# Booleans representing properties of colorectal cancer
deadly = Bool('deadly')
low_survival = Bool('low_survival')
severe = Bool('severe')
bile_duct = Bool('bile_duct')
cholangiocarcinoma = Bool('cholangiocarcinoma')
mild_flu = Bool('mild_flu')

# Premises
s.add(Implies(deadly, low_survival))
s.add(Implies(severe, deadly))
s.add(Implies(bile_duct, severe))
s.add(Implies(cholangiocarcinoma, bile_duct))
s.add(Implies(mild_flu, low_survival))
s.add(Not(And(bile_duct, low_survival)))

# Conclusion: cholangiocarcinoma AND (mild_flu OR bile_duct)
conclusion = And(cholangiocarcinoma, Or(mild_flu, bile_duct))

# Check if premises + conclusion is satisfiable
s.push()
s.add(conclusion)
result = s.check()
if result == unsat:
    print("STATUS: proved")
    print("Result: False")
    # Find a model of premises and not conclusion to show counterexample
    s.pop()
    s.push()
    s.add(Not(conclusion))
    if s.check() == sat:
        m = s.model()
        print("deadly =", m[deadly])
        print("low_survival =", m[low_survival])
        print("severe =", m[severe])
        print("bile_duct =", m[bile_duct])
        print("cholangiocarcinoma =", m[cholangiocarcinoma])
        print("mild_flu =", m[mild_flu])
    else:
        print("No model found")
else:
    print("STATUS: unknown")