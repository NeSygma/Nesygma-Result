from z3 import *

def base_solver(extra_constraints=None):
    s = Solver()
    # Variables for each business location (1..7)
    opt = Int('opt')
    pharm = Int('pharm')
    rest1 = Int('rest1')
    rest2 = Int('rest2')
    shoe = Int('shoe')
    toy = Int('toy')
    vet = Int('vet')
    vars = [opt, pharm, rest1, rest2, shoe, toy, vet]
    for v in vars:
        s.add(v >= 1, v <= 7)
    s.add(Distinct(vars))
    # Pharmacy at an end
    s.add(Or(pharm == 1, pharm == 7))
    # One restaurant at the opposite end
    s.add(Or(And(pharm == 1, Or(rest1 == 7, rest2 == 7)),
          And(pharm == 7, Or(rest1 == 1, rest2 == 1)))
    # Pharmacy next to opt or vet
    s.add(Or(Abs(pharm - opt) == 1, Abs(pharm - vet) == 1))
    # Toy not next to vet
    s.add(Abs(toy - vet) != 1)
    if extra_constraints:
        for c in extra_constraints:
            s.add(c)
    return s, vars

def collect_models(solver, vars):
    models = set()
    while solver.check() == sat:
        m = solver.model()
        # canonicalize restaurant pair (unordered)
        r = tuple(sorted((m[vars[2]].as_long(), m[vars[3]].as_long())))
        tup = (m[vars[0]].as_long(), m[vars[1]].as_long(), r,
               m[vars[4]].as_long(), m[vars[5]].as_long(), m[vars[6]].as_long())
        models.add(tup)
        # block this model
        block = [v != m[v] for v in vars]
        solver.add(Or(block))
    return models

# Original separation constraint: at least two businesses between restaurants => distance >=3
orig_s, orig_vars = base_solver([Abs(Int('rest1') - Int('rest2')) >= 3])
orig_models = collect_models(orig_s, orig_vars)

# Define option constraints (without original separation)
opt_constraints = {
    'A': [Or(Int('rest1') == 3, Int('rest1') == 4, Int('rest1') == 5,
          Int('rest2') == 3, Int('rest2') == 4, Int('rest2') == 5)],
    'B': [Or(Abs(Int('rest1') - Int('opt')) == 1, Abs(Int('rest1') - Int('vet')) == 1,
          Abs(Int('rest2') - Int('opt')) == 1, Abs(Int('rest2') - Int('vet')) == 1)],
    'C': [Or(And(Int('rest1') < Int('toy'), Int('toy') < Int('rest2')),
          And(Int('rest2') < Int('toy'), Int('toy') < Int('rest1')),
          And(Int('rest1') < Int('vet'), Int('vet') < Int('rest2')),
          And(Int('rest2') < Int('vet'), Int('vet') < Int('rest1')))],
    'D': [Or(Abs(Int('pharm') - Int('rest1')) <= 3, Abs(Int('pharm') - Int('rest2')) <= 3)],
    'E': [Abs(Int('opt') - Int('shoe')) != 1]
}

found_options = []
for letter, extra in opt_constraints.items():
    # Build solver with base constraints + this option (no original separation)
    s, vars = base_solver(extra)
    # Check if there is any solution
    if s.check() == sat:
        # Collect models for this option
        models = collect_models(s, vars)
        if models == orig_models:
            found_options.append(letter)
    # else unsat, ignore

if len(found_options) == 1:
    print('STATUS: sat')
    print('answer:' + found_options[0])
elif len(found_options) > 1:
    print('STATUS: unsat')
    print('Refine: Multiple options found', found_options)
else:
    print('STATUS: unsat')
    print('Refine: No options found')