from z3 import *

# Define buildings and their classes
buildings = {
    'Garza': 1, 'Yates': 3, 'Zimmer': 3,  # RealProp
    'Flores': 1, 'Lynch': 2,               # Southco
    'King': 2, 'Meyer': 2, 'Ortiz': 2      # Trustcorp
}

# Initial ownership: 0=RealProp, 1=Southco, 2=Trustcorp
initial_owner = {
    'Garza': 0, 'Yates': 0, 'Zimmer': 0,
    'Flores': 1, 'Lynch': 1,
    'King': 2, 'Meyer': 2, 'Ortiz': 2
}

# For each option, define the final ownership
options = {
    'A': {
        'RealProp': ['Flores', 'Garza'],
        'Southco': ['Lynch', 'Yates', 'Zimmer'],
        'Trustcorp': ['King', 'Meyer', 'Ortiz']
    },
    'B': {
        'RealProp': ['Garza', 'King', 'Ortiz'],
        'Southco': ['Flores', 'Lynch'],
        'Trustcorp': ['Meyer', 'Yates', 'Zimmer']
    },
    'C': {
        'RealProp': ['Garza', 'Lynch'],
        'Southco': ['Flores', 'Yates', 'Zimmer'],
        'Trustcorp': ['King', 'Meyer', 'Ortiz']
    },
    'D': {
        'RealProp': ['Garza', 'Meyer', 'Yates'],
        'Southco': ['Flores', 'Lynch'],
        'Trustcorp': ['King', 'Ortiz', 'Zimmer']
    },
    'E': {
        'RealProp': ['Garza', 'Yates', 'Zimmer'],
        'Southco': ['Lynch', 'Ortiz'],
        'Trustcorp': ['Flores', 'King', 'Meyer']
    }
}

def get_final_owner(opt):
    """Convert option dict to building->owner mapping"""
    final = {}
    for company, bldgs in opt.items():
        if company == 'RealProp':
            owner = 0
        elif company == 'Southco':
            owner = 1
        else:
            owner = 2
        for b in bldgs:
            final[b] = owner
    return final

def check_option_valid(opt_letter, opt_dict):
    """Check if option represents exactly one valid trade"""
    final = get_final_owner(opt_dict)
    
    # Find which buildings changed ownership
    changed = []
    for b in buildings:
        if final[b] != initial_owner[b]:
            changed.append(b)
    
    # Must have exactly one trade - determine trade type from changed buildings
    # Trade type 1: 2 buildings swap (same class, different owners)
    # Trade type 2: 1 class1 <-> 2 class2 (3 buildings change hands)
    # Trade type 3: 1 class2 <-> 2 class3 (3 buildings change hands)
    
    if len(changed) == 2:
        # Type 1: same class swap
        b1, b2 = changed
        if buildings[b1] != buildings[b2]:
            return False
        # They must swap owners
        if final[b1] != initial_owner[b2] or final[b2] != initial_owner[b1]:
            return False
        # Must be between different companies
        if initial_owner[b1] == initial_owner[b2]:
            return False
        return True
    
    elif len(changed) == 3:
        # Type 2 or 3
        # Check if it's type 2: one class1 for two class2
        class1_changed = [b for b in changed if buildings[b] == 1]
        class2_changed = [b for b in changed if buildings[b] == 2]
        class3_changed = [b for b in changed if buildings[b] == 3]
        
        # Type 2: 1 class1 <-> 2 class2
        if len(class1_changed) == 1 and len(class2_changed) == 2 and len(class3_changed) == 0:
            c1_bldg = class1_changed[0]
            c2_bldgs = class2_changed
            # The class1 building and the two class2 buildings must come from different companies
            # and swap: class1 goes to company that had class2, class2s go to company that had class1
            c1_orig_owner = initial_owner[c1_bldg]
            c2_orig_owners = set(initial_owner[b] for b in c2_bldgs)
            
            # Both class2 must come from same company (traded together)
            if len(c2_orig_owners) != 1:
                return False
            c2_orig_owner = list(c2_orig_owners)[0]
            
            # Must be different companies
            if c1_orig_owner == c2_orig_owner:
                return False
            
            # After trade: class1 goes to c2's company, class2s go to c1's company
            if final[c1_bldg] != c2_orig_owner:
                return False
            for b in c2_bldgs:
                if final[b] != c1_orig_owner:
                    return False
            return True
        
        # Type 3: 1 class2 <-> 2 class3
        if len(class1_changed) == 0 and len(class2_changed) == 1 and len(class3_changed) == 2:
            c2_bldg = class2_changed[0]
            c3_bldgs = class3_changed
            c2_orig_owner = initial_owner[c2_bldg]
            c3_orig_owners = set(initial_owner[b] for b in c3_bldgs)
            
            if len(c3_orig_owners) != 1:
                return False
            c3_orig_owner = list(c3_orig_owners)[0]
            
            if c2_orig_owner == c3_orig_owner:
                return False
            
            if final[c2_bldg] != c3_orig_owner:
                return False
            for b in c3_bldgs:
                if final[b] != c2_orig_owner:
                    return False
            return True
        
        return False
    
    else:
        return False

# Check each option
found_options = []
for letter in ['A', 'B', 'C', 'D', 'E']:
    if check_option_valid(letter, options[letter]):
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")