from z3 import *

# Students: Louis(0), Mollie(1), Onyx(2), Ryan(3), Tiffany(4), Yoshio(5)
L, M, O, R, T, Y = range(6)

def check_assignment(assignment):
    # assignment is a list of 4 students [S1921, S1922, S1923, S1924]
    s1921, s1922, s1923, s1924 = assignment
    
    # Exactly one student per year (already implied by the list structure)
    # All students must be distinct
    if len(set(assignment)) != 4:
        return False
    
    # C1: Only Louis or Tiffany can be assigned to 1923.
    if not (s1923 == L or s1923 == T):
        return False
        
    # C2: If Mollie is assigned, she must be in 1921 or 1922.
    if M in assignment:
        if not (s1921 == M or s1922 == M):
            return False
            
    # C3: If Tiffany is assigned, Ryan must be assigned.
    if T in assignment:
        if R not in assignment:
            return False
            
    # C4: If Ryan is assigned, Onyx must be assigned to the year immediately prior to Ryan's.
    if R in assignment:
        if s1921 == R:
            return False # No year prior to 1921
        if s1922 == R:
            if s1921 != O: return False
        if s1923 == R:
            if s1922 != O: return False
        if s1924 == R:
            if s1923 != O: return False
            
    return True

# Map names to IDs
name_map = {"Louis": L, "Mollie": M, "Onyx": O, "Ryan": R, "Tiffany": T, "Yoshio": Y}

options = {
    "A": ["Louis", "Onyx", "Ryan", "Yoshio"],
    "B": ["Mollie", "Yoshio", "Tiffany", "Onyx"],
    "C": ["Onyx", "Ryan", "Louis", "Tiffany"],
    "D": ["Tiffany", "Onyx", "Louis", "Ryan"],
    "E": ["Yoshio", "Onyx", "Louis", "Mollie"]
}

found_options = []
for letter, names in options.items():
    assignment = [name_map[n] for n in names]
    if check_assignment(assignment):
        found_options.append(letter)

print(f"Valid options: {found_options}")

# Now use the required Z3 skeleton for the final output
solver = Solver()
# Define variables for the assignment
s1921, s1922, s1923, s1924 = Ints('s1921 s1922 s1923 s1924')
vars = [s1921, s1922, s1923, s1924]

# Domain: 0-5
for v in vars:
    solver.add(v >= 0, v <= 5)
solver.add(Distinct(vars))

# C1: 1923 is L or T
solver.add(Or(s1923 == L, s1923 == T))

# C2: If M is assigned, M is 1921 or 1922
# M in assignment <=> (s1921==M or s1922==M or s1923==M or s1924==M)
m_assigned = Or([v == M for v in vars])
solver.add(Implies(m_assigned, Or(s1921 == M, s1922 == M)))

# C3: If T is assigned, R is assigned
t_assigned = Or([v == T for v in vars])
r_assigned = Or([v == R for v in vars])
solver.add(Implies(t_assigned, r_assigned))

# C4: If R is assigned, O is in the year prior
# R in 1922 => O in 1921
# R in 1923 => O in 1922
# R in 1924 => O in 1923
# R cannot be in 1921
solver.add(s1921 != R)
solver.add(Implies(s1922 == R, s1921 == O))
solver.add(Implies(s1923 == R, s1922 == O))
solver.add(Implies(s1924 == R, s1923 == O))

# Define options as constraints
def get_constr(names):
    assignment = [name_map[n] for n in names]
    return And(s1921 == assignment[0], s1922 == assignment[1], s1923 == assignment[2], s1924 == assignment[3])

found_options = []
for letter, names in options.items():
    solver.push()
    solver.add(get_constr(names))
    if solver.check() == sat:
        found_options.append(letter)
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