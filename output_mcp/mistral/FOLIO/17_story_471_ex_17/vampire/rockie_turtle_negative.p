fof(can_be_spotted_near_def, axiom, ! [X] : (can_be_spotted_near(X, campus) => (rabbit(X) | squirrel(X)))).
fof(all_rabbits_spotted_are_cute, axiom, ! [X] : ((rabbit(X) & can_be_spotted_near(X, campus)) => cute(X))).
fof(some_turtles_spotted, axiom, ? [X] : (turtle(X) & can_be_spotted_near(X, campus))).
fof(skittish_implies_not_calm, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(all_spotted_squirrels_are_skittish, axiom, ! [X] : ((squirrel(X) & can_be_spotted_near(X, campus)) => skittish(X))).
fof(rockie_spotted_and_calm, axiom, can_be_spotted_near(rockie, campus) & calm(rockie)).
fof(rockie_is_not_turtle_conjecture, conjecture, ~turtle(rockie)).