from z3 import *

k, l, m, n, o, p = Bools('k l m n o p')

def get_base_solver():
    solver = Solver()
    solver.add(m != p)
    solver.add(k == n)
    solver.add(Implies(k, o))
    solver.add(Implies(m, Not(n)))
    return solver

# Debug option B
solver = get_base_solver()
solver.add(And(o, Not(p)))  # O fall, P spring

print("Checking option B:")
result = solver.check()
print(f"Result: {result}")
if result == sat:
    model = solver.model()
    print(f"Model: K={model[k]}, L={model[l]}, M={model[m]}, N={model[n]}, O={model[o]}, P={model[p]}")
    
    vars_list = [k, l, m, n, o, p]
    blocking = Or([v != model.eval(v) for v in vars_list])
    print(f"Blocking clause: {blocking}")
    
    solver.push()
    solver.add(blocking)
    result2 = solver.check()
    print(f"Second check result: {result2}")
    if result2 == sat:
        model2 = solver.model()
        print(f"Model2: K={model2[k]}, L={model2[l]}, M={model2[m]}, N={model2[n]}, O={model2[o]}, P={model2[p]}")
    solver.pop()

# Also debug option A
print("\nChecking option A:")
solver = get_base_solver()
solver.add(And(k, Not(l)))  # K fall, L spring
result = solver.check()
print(f"Result: {result}")
if result == sat:
    model = solver.model()
    print(f"Model: K={model[k]}, L={model[l]}, M={model[m]}, N={model[n]}, O={model[o]}, P={model[p]}")
    
    vars_list = [k, l, m, n, o, p]
    blocking = Or([v != model.eval(v) for v in vars_list])
    print(f"Blocking clause: {blocking}")
    
    solver.push()
    solver.add(blocking)
    result2 = solver.check()
    print(f"Second check result: {result2}")
    if result2 == sat:
        model2 = solver.model()
        print(f"Model2: K={model2[k]}, L={model2[l]}, M={model2[m]}, N={model2[n]}, O={model2[o]}, P={model2[p]}")
    solver.pop()