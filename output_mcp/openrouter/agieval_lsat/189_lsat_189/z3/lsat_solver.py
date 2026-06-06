from z3 import *

# Base constraints for the LSAT problem
persons = ['Q','R','S','T','V','W','X']  # Quinn, Ruiz, Smith, Taylor, Verma, Wells, Xue
member = {p: Bool(f"member_{p}") for p in persons}
leader = {p: Bool(f"leader_{p}") for p in persons}

solver = Solver()
# Exactly 3 members
solver.add(Sum([If(member[p], 1, 0) for p in persons]) == 3)
# Exactly 1 leader
solver.add(Sum([If(leader[p], 1, 0) for p in persons]) == 1)
# Leader implies member
for p in persons:
    solver.add(Implies(leader[p], member[p]))
# Quinn or Ruiz can be a project member only if leading the project.
solver.add(Implies(member['Q'], leader['Q']))
solver.add(Implies(member['R'], leader['R']))
# If Smith is a project member, Taylor must also be.
solver.add(Implies(member['S'], member['T']))
# If Wells is a project member, neither Ruiz nor Verma can be.
solver.add(Implies(member['W'], And(Not(member['R']), Not(member['V']))))

# Define extra constraints for each answer choice
options = {
    "A": [Not(member['Q']), Not(member['S'])],               # Neither Quinn nor Smith is selected.
    "B": [Not(member['Q']), Not(member['T'])],               # Neither Quinn nor Taylor is selected.
    "C": [Not(member['Q']), Not(member['X'])],               # Neither Quinn nor Xue is selected.
    "D": [Not(member['R']), Not(member['W'])],               # Neither Ruiz nor Wells is selected.
    "E": [Not(member['R']), Not(member['V'])],               # Neither Ruiz nor Verma is selected.
}

found_options = []
for letter, extra in options.items():
    solver.push()
    for c in extra:
        solver.add(c)
    # Check if there is at least one solution under this extra condition
    if solver.check() == sat:
        m = solver.model()
        # Block this exact solution to see if another distinct solution exists
        block = []
        for p in persons:
            block.append(member[p] != m.eval(member[p]))
            block.append(leader[p] != m.eval(leader[p]))
        solver.add(Or(block))
        if solver.check() == unsat:
            # Exactly one solution -> this option uniquely determines selection
            found_options.append(letter)
        # else: more than one solution, not uniquely determined
    # else: no solution under this extra condition
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")