from z3 import *

# Birds
O, P, R, S, T = range(5)
birds = [O, P, R, S, T]
bird_names = {O: "oystercatchers", P: "petrels", R: "rails", S: "sandpipers", T: "terns"}

# Locations
G, H = 0, 1

def check_order(order):
    # order is a list of 5 birds
    # 1. The first lecture is in Gladwyn Hall.
    # 2. The fourth lecture is in Howard Auditorium.
    # 3. Exactly three of the lectures are in Gladwyn Hall.
    # 4. The lecture on sandpipers is in Howard Auditorium and is given earlier than the lecture on oystercatchers.
    # 5. The lecture on terns is given earlier than the lecture on petrels, which is in Gladwyn Hall.
    
    # We need to determine the locations for each position in the order.
    # Let locs be a list of 5 locations.
    # We know:
    # locs[0] = G
    # locs[3] = H
    # Sum(locs) == 2 (since 3 are G, 2 are H)
    # locs[pos_S] = H
    # locs[pos_P] = G
    
    # Let's try to find if there exists a valid assignment of locations for a given order.
    
    pos_O = order.index(O)
    pos_P = order.index(P)
    pos_R = order.index(R)
    pos_S = order.index(S)
    pos_T = order.index(T)
    
    # Constraints on order:
    if not (pos_S < pos_O): return False
    if not (pos_T < pos_P): return False
    
    # Constraints on locations:
    # We have 5 positions, 3 are G, 2 are H.
    # locs[0] = G
    # locs[3] = H
    # locs[pos_S] = H
    # locs[pos_P] = G
    
    # Let's use a solver to check if there exists a valid locs assignment
    s = Solver()
    locs = [Int(f'loc_{i}') for i in range(5)]
    for i in range(5):
        s.add(Or(locs[i] == G, locs[i] == H))
    
    s.add(locs[0] == G)
    s.add(locs[3] == H)
    s.add(Sum([If(locs[i] == G, 1, 0) for i in range(5)]) == 3)
    s.add(locs[pos_S] == H)
    s.add(locs[pos_P] == G)
    
    return s.check() == sat

# Answer Choices
# (A) oystercatchers, petrels, rails, sandpipers, terns
# (B) petrels, sandpipers, oystercatchers, terns, rails
# (C) rails, sandpipers, terns, petrels, oystercatchers
# (D) sandpipers, terns, oystercatchers, rails, petrels
# (E) terns, petrels, sandpipers, oystercatchers, rails

choices = {
    "A": [O, P, R, S, T],
    "B": [P, S, O, T, R],
    "C": [R, S, T, P, O],
    "D": [S, T, O, R, P],
    "E": [T, P, S, O, R]
}

found_options = []
for letter, order in choices.items():
    if check_order(order):
        found_options.append(letter)

print(f"STATUS: sat")
print(f"answer:{found_options[0]}")