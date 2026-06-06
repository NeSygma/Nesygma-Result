from z3 import *

# We need to find which option is NOT forced (must be true) given V=4.
# The question: "each of the following must be true EXCEPT"
# So we find the option whose negation is satisfiable (i.e., the option could be false).

# Define base constraints
def add_base_constraints(s):
    G, K, P, S, T, V = Ints('G K P S T V')
    s.add(And(1 <= G, G <= 6))
    s.add(And(1 <= K, K <= 6))
    s.add(And(1 <= P, P <= 6))
    s.add(And(1 <= S, S <= 6))
    s.add(And(1 <= T, T <= 6))
    s.add(And(1 <= V, V <= 6))
    s.add(Distinct(G, K, P, S, T, V))
    s.add(G != 4)          # guitarist not 4th
    s.add(P < K)           # percussionist before keyboardist
    s.add(V < K)           # violinist before keyboardist
    s.add(K < G)           # keyboardist before guitarist
    # saxophonist after exactly one of {percussionist, trumpeter}
    s.add(If(S > P, 1, 0) + If(S > T, 1, 0) == 1)
    s.add(V == 4)          # violinist is 4th
    return G, K, P, S, T, V

# Build option constraints
solver = Solver()
G, K, P, S, T, V = add_base_constraints(solver)

# Option constraints (the "must be true" statements to test)
options = {
    "A": P < V,
    "B": T < V,
    "C": T < G,
    "D": S < V,
    "E": T < S
}

found_options = []
for letter, constr in options.items():
    s = Solver()
    G2, K2, P2, S2, T2, V2 = add_base_constraints(s)
    # Test if the option is forced: add NOT(option), see if satisfiable
    # Mapping: map letter to the right variable names
    if letter == "A":
        s.add(Not(P2 < V2))
    elif letter == "B":
        s.add(Not(T2 < V2))
    elif letter == "C":
        s.add(Not(T2 < G2))
    elif letter == "D":
        s.add(Not(S2 < V2))
    elif letter == "E":
        s.add(Not(T2 < S2))
    
    if s.check() == sat:
        # Not(option) is SAT, meaning option is NOT forced (could be false)
        found_options.append(letter)

# Now found_options contains the letters whose negation is satisfiable.
# These are the options that are NOT forced to be true.
# The question asks: "each of the following must be true EXCEPT"
# So the answer is the option that is NOT forced.

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")