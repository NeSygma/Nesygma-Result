from z3 import *
solver = Solver()

# Declare variables
romance_screen = Int('romance_screen')
romance_time = Int('romance_time')
western_screen = Int('western_screen')
western_time = Int('western_time')
sci_fi_screen = Int('sci_fi_screen')
sci_fi_time = Int('sci_fi_time')
mystery_screen = Int('mystery_screen')
mystery_time = Int('mystery_time')
horror_screen = Int('horror_screen')
horror_time = Int('horror_time')

# Define the schedules for each option
options_list = [
    ('A', {
        'romance_screen': 1,
        'romance_time': 7,
        'western_screen': 2,
        'western_time': 7,
        'sci_fi_screen': 2,
        'sci_fi_time': 9,
        'mystery_screen': 3,
        'mystery_time': 8,
        'horror_screen': 1,
        'horror_time': 9,
    }),
    ('B', {
        'romance_screen': 1,
        'romance_time': 9,
        'western_screen': 3,
        'western_time': 8,
        'sci_fi_screen': 2,
        'sci_fi_time': 9,
        'mystery_screen': 1,
        'mystery_time': 7,
        'horror_screen': 2,
        'horror_time': 7,
    }),
    ('C', {
        'western_screen': 1,
        'western_time': 7,
        'sci_fi_screen': 1,
        'sci_fi_time': 9,
        'mystery_screen': 2,
        'mystery_time': 7,
        'horror_screen': 2,
        'horror_time': 9,
        'romance_screen': 3,
        'romance_time': 8,
    }),
    ('D', {
        'romance_screen': 1,
        'romance_time': 7,
        'mystery_screen': 1,
        'mystery_time': 9,
        'western_screen': 2,
        'western_time': 7,
        'horror_screen': 2,
        'horror_time': 9,
        'sci_fi_screen': 3,
        'sci_fi_time': 8,
    }),
    ('E', {
        'western_screen': 1,
        'western_time': 7,
        'mystery_screen': 1,
        'mystery_time': 9,
        'sci_fi_screen': 2,
        'sci_fi_time': 7,
        'romance_screen': 2,
        'romance_time': 9,
        'horror_screen': 3,
        'horror_time': 8,
    })
]

found_options = []
for letter, constr in options_list:
    solver.push()
    # Assign variables according to the option
    solver.add(romance_screen == constr['romance_screen'])
    solver.add(romance_time == constr['romance_time'])
    solver.add(western_screen == constr['western_screen'])
    solver.add(western_time == constr['western_time'])
    solver.add(sci_fi_screen == constr['sci_fi_screen'])
    solver.add(sci_fi_time == constr['sci_fi_time'])
    solver.add(mystery_screen == constr['mystery_screen'])
    solver.add(mystery_time == constr['mystery_time'])
    solver.add(horror_screen == constr['horror_screen'])
    solver.add(horror_time == constr['horror_time'])
    # Add global constraints
    solver.add(western_time < horror_time)          # western before horror
    solver.add(sci_fi_screen != 3)                  # sci-fi not on screen 3
    solver.add(romance_screen != 2)                 # romance not on screen 2
    solver.add(horror_screen != mystery_screen)     # horror and mystery different screens
    # Check satisfiability
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output according to the required multiple‑choice logic
if len(found_options) == 1:
    print('STATUS: sat')
    print(f'answer:{found_options[0]}')
elif len(found_options) > 1:
    print('STATUS: unsat')
    print(f'Refine: Multiple options found {found_options}')
else:
    print('STATUS: unsat')
    print('Refine: No options found')