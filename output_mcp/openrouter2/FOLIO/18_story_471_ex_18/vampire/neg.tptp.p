fof(rabbit_spotted_cute, axiom, ! [X] : ((rabbit(X) & spotted_near_campus(X)) => cute(X))).
fof(squirrel_spotted_skittish, axiom, ! [X] : ((squirrel(X) & spotted_near_campus(X)) => skittish(X))).
fof(skittish_not_calm, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(turtle_spotted_exists, axiom, ? [T] : (turtle(T) & spotted_near_campus(T))).
fof(animal_spotted_only_rabbit_squirrel, axiom, ! [X] : ((animal(X) & spotted_near_campus(X)) => (rabbit(X) | squirrel(X)))).
fof(rockie_spotted, axiom, spotted_near_campus(rockie)).
fof(rockie_calm, axiom, calm(rockie)).
fof(conjecture, conjecture, ~turtle(rockie)).