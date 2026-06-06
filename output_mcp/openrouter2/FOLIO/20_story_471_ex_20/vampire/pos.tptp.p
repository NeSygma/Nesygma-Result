fof(existence_turtle, axiom, ? [X] : (turtle(X) & spotted_near_campus(X))).
fof(only_rabbits_squirrels, axiom, ! [X] : (spotted_near_campus(X) => (rabbit(X) | squirrel(X)))).
fof(rabbit_cute, axiom, ! [X] : ((rabbit(X) & spotted_near_campus(X)) => cute(X))).
fof(squirrel_skittish, axiom, ! [X] : ((squirrel(X) & spotted_near_campus(X)) => skittish(X))).
fof(skittish_not_calm, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(rockie_spotted, axiom, spotted_near_campus(rockie)).
fof(rockie_calm, axiom, calm(rockie)).
fof(conjecture, conjecture, ~ (turtle(rockie) & squirrel(rockie)) => (cute(rockie) | skittish(rockie))).