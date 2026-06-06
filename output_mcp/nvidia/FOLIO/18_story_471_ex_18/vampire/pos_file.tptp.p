fof(rabbit_cute, axiom, ! [X] : ((rabbit(X) & spotted_campus(X)) => cute(X))).
fof(some_turtle_spotted, axiom, ? [X] : (turtle(X) & spotted_campus(X))).
fof(only_rabbits_squirrels, axiom, ! [X] : ((spotted_campus(X)) => (rabbit(X) | squirrel(X))) ).
fof(skittish_not_calm, axiom, ! [X] : ((skittish(X)) => ~calm(X))).
fof(squirrel_skittish, axiom, ! [X] : ((squirrel(X) & spotted_campus(X)) => skittish(X))).
fof(rockie_spotted, axiom, spotted_campus(rockie)).
fof(rockie_calm, axiom, calm(rockie)).
fof(goal, conjecture, ~turtle(rockie)).