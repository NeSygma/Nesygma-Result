from z3 import *

# Businesses: P (Pharmacy), O (Optometrist), R1 (Restaurant 1), R2 (Restaurant 2), S (Shoe), T (Toy), V (Vet)
# Spaces: 1, 2, 3, 4, 5, 6, 7

def check_option(order):
    # order is a list of 7 strings
    # Map strings to indices
    pos = {}
    for i, b in enumerate(order):
        if b not in pos:
            pos[b] = []
        pos[b].append(i + 1)
    
    # Handle the two restaurants
    # The input list has 'restaurant' twice.
    # Let's re-process the list to identify the two restaurants.
    restaurants = [i+1 for i, b in enumerate(order) if b == 'restaurant']
    
    # Constraint 1: Pharmacy at one end, one restaurant at the other
    # Pharmacy is at 1 or 7. Restaurant is at 7 or 1.
    p_pos = order.index('pharmacy') + 1
    r_pos1 = restaurants[0]
    r_pos2 = restaurants[1]
    
    c1 = (p_pos == 1 and (r_pos1 == 7 or r_pos2 == 7)) or \
         (p_pos == 7 and (r_pos1 == 1 or r_pos2 == 1))
    
    # Constraint 2: Two restaurants separated by at least two other businesses
    # |pos(R1) - pos(R2)| >= 3
    c2 = abs(r_pos1 - r_pos2) >= 3
    
    # Constraint 3: Pharmacy next to O or V
    o_pos = order.index('optometrist') + 1
    v_pos = order.index('veterinarian') + 1
    c3 = (abs(p_pos - o_pos) == 1) or (abs(p_pos - v_pos) == 1)
    
    # Constraint 4: Toy store cannot be next to veterinarian
    t_pos = order.index('toy store') + 1
    c4 = abs(t_pos - v_pos) != 1
    
    return c1 and c2 and c3 and c4

options = {
    "A": ["pharmacy", "optometrist", "shoe store", "restaurant", "veterinarian", "toy store", "restaurant"],
    "B": ["pharmacy", "veterinarian", "optometrist", "shoe store", "restaurant", "toy store", "restaurant"],
    "C": ["restaurant", "shoe store", "veterinarian", "pharmacy", "optometrist", "toy store", "restaurant"],
    "D": ["restaurant", "toy store", "optometrist", "restaurant", "veterinarian", "shoe store", "pharmacy"],
    "E": ["restaurant", "optometrist", "toy store", "restaurant", "shoe store", "veterinarian", "pharmacy"]
}

for label, order in options.items():
    if check_option(order):
        print(f"Option {label} is valid.")
    else:
        print(f"Option {label} is invalid.")