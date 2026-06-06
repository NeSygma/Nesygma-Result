from z3 import *

# Define Seasons
Spring, Summer, Fall, Winter = Ints('Spring Summer Fall Winter')
seasons = [Spring, Summer, Fall, Winter]

# Define Students
Emma, Mia, James = Ints('Emma Mia James')
students = [Emma, Mia, James]

# Define FavoriteSeason function
# We use a function to map student to a season
fav_season = Function('fav_season', IntSort(), IntSort())

# Define WantsLongVacation
wants_long_vacation = Function('wants_long_vacation', IntSort(), BoolSort())

solver = Solver()

# Premises
# 1. Seasons are distinct
solver.add(Distinct(seasons))
# 2. All students who want to have a long vacation have summer as their favorite season.
# For all students s, if wants_long_vacation(s) then fav_season(s) == Summer
# Since we have a finite set of students, we can just assert it for each.
for s in students:
    solver.add(Implies(wants_long_vacation(s), fav_season(s) == Summer))

# 3. Emma's favorite season is summer.
solver.add(fav_season(Emma) == Summer)

# 4. Mia's favorite season is not the same as Emma's.
solver.add(fav_season(Mia) != fav_season(Emma))

# 5. James wants to have a long vacation.
solver.add(wants_long_vacation(James) == True)

# Conclusion to evaluate: Mia's favorite season is spring.
goal = (fav_season(Mia) == Spring)

# Check Negated Goal (Try to find a counterexample)
s_neg = Solver()
s_neg.add(solver.assertions())
s_neg.add(Not(goal))
neg_res = s_neg.check()

# Check Positive Goal (Try to find a confirming model)
s_pos = Solver()
s_pos.add(solver.assertions())
s_pos.add(goal)
pos_res = s_pos.check()

print(f"Negated Goal Result: {neg_res}")
print(f"Positive Goal Result: {pos_res}")

if neg_res == unsat and pos_res == sat:
    print("STATUS: proved")
    print("CONCLUSION: True")
elif neg_res == sat and pos_res == unsat:
    print("STATUS: proved")
    print("CONCLUSION: False")
elif neg_res == sat and pos_res == sat:
    print("STATUS: proved")
    print("CONCLUSION: Uncertain")
else:
    print("STATUS: unknown")