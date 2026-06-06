% Positive version
fof(all_rabbits_spotted_cute, axiom, ! [X] : ((rabbit(X) & spotted(X)) => cute(X))).
fof(some_turtles_spotted, axiom, ? [X] : (turtle(X) & spotted(X))).
fof(only_spotted_animals, axiom, ! [X] : (spotted(X) => (rabbit(X) | squirrel(X)))).
fof(skittish_not_calm, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(squirrel_spotted_skittish, axiom, ! [X] : ((squirrel(X) & spotted(X)) => skittish(X))).
fof(rockie_spotted_calm, axiom, spotted(rockie) & calm(rockie)).
fof(goal, conjecture, turtle(rockie)).