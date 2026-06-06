from z3 import *
solver = Solver()
# Variables for each movie: screen (1-3) and time (7,8,9)
movies = ['horror','mystery','romance','scifi','western']
# Create dicts
screen = {m: Int(f'screen_{m}') for m in movies}
time = {m: Int(f'time_{m}') for m in movies}
# Domain constraints
for m in movies:
    solver.add(Or(screen[m]==1, screen[m]==2, screen[m]==3))
    solver.add(Or(time[m]==7, time[m]==8, time[m]==9))
# Screen3 must be at 8
solver.add(time['horror'] == 7 | time['horror'] == 9 | time['horror'] == 8)  # placeholder
# Actually enforce each movie time based on screen
# For screen 3, time must be 8
solver.add(Implies(screen['horror']==3, time['horror']==8))
solver.add(Implies(screen['mystery']==3, time['mystery']==8))
solver.add(Implies(screen['romance']==3, time['romance']==8))
solver.add(Implies(screen['scifi']==3, time['scifi']==8))
solver.add(Implies(screen['western']==3, time['western']==8))
# For screens 1 and 2, time must be 7 or 9
for m in movies:
    solver.add(Implies(Or(screen[m]==1, screen[m]==2), Or(time[m]==7, time[m]==9)))
# Each screen has correct number of movies
solver.add(Sum([If(screen[m]==1,1,0) for m in movies]) == 2)
solver.add(Sum([If(screen[m]==2,1,0) for m in movies]) == 2)
solver.add(Sum([If(screen[m]==3,1,0) for m in movies]) == 1)
# No two movies share same screen and time
for i in range(len(movies)):
    for j in range(i+1, len(movies)):
        mi = movies[i]; mj = movies[j]
        solver.add(Not(And(screen[mi]==screen[mj], time[mi]==time[mj])))
# Additional constraints
# Western before horror
solver.add(time['western'] < time['horror'])
# Sci-fi not on screen3
solver.add(screen['scifi'] != 3)
# Romance not on screen2
solver.add(screen['romance'] != 2)
# Horror and mystery on different screens
solver.add(screen['horror'] != screen['mystery'])

# Define option constraints
opt_a_constr = []
# Option A
opt_a_constr.append(screen['horror']==1)
opt_a_constr.append(time['horror']==9)
opt_a_constr.append(screen['romance']==1)
opt_a_constr.append(time['romance']==7)
opt_a_constr.append(screen['western']==2)
opt_a_constr.append(time['western']==7)
opt_a_constr.append(screen['scifi']==2)
opt_a_constr.append(time['scifi']==9)
opt_a_constr.append(screen['mystery']==3)
opt_a_constr.append(time['mystery']==8)

opt_b_constr = []
# Option B
opt_b_constr.append(screen['mystery']==1)
opt_b_constr.append(time['mystery']==7)
opt_b_constr.append(screen['romance']==1)
opt_b_constr.append(time['romance']==9)
opt_b_constr.append(screen['horror']==2)
opt_b_constr.append(time['horror']==7)
opt_b_constr.append(screen['scifi']==2)
opt_b_constr.append(time['scifi']==9)
opt_b_constr.append(screen['western']==3)
opt_b_constr.append(time['western']==8)

opt_c_constr = []
# Option C
opt_c_constr.append(screen['western']==1)
opt_c_constr.append(time['western']==7)
opt_c_constr.append(screen['scifi']==1)
opt_c_constr.append(time['scifi']==9)
opt_c_constr.append(screen['mystery']==2)
opt_c_constr.append(time['mystery']==7)
opt_c_constr.append(screen['horror']==2)
opt_c_constr.append(time['horror']==9)
opt_c_constr.append(screen['romance']==3)
opt_c_constr.append(time['romance']==8)

opt_d_constr = []
# Option D
opt_d_constr.append(screen['romance']==1)
opt_d_constr.append(time['romance']==7)
opt_d_constr.append(screen['mystery']==1)
opt_d_constr.append(time['mystery']==9)
opt_d_constr.append(screen['western']==2)
opt_d_constr.append(time['western']==7)
opt_d_constr.append(screen['horror']==2)
opt_d_constr.append(time['horror']==9)
opt_d_constr.append(screen['scifi']==3)
opt_d_constr.append(time['scifi']==8)

opt_e_constr = []
# Option E
opt_e_constr.append(screen['western']==1)
opt_e_constr.append(time['western']==7)
opt_e_constr.append(screen['mystery']==1)
opt_e_constr.append(time['mystery']==9)
opt_e_constr.append(screen['scifi']==2)
opt_e_constr.append(time['scifi']==7)
opt_e_constr.append(screen['romance']==2)
opt_e_constr.append(time['romance']==9)
opt_e_constr.append(screen['horror']==3)
opt_e_constr.append(time['horror']==8)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
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