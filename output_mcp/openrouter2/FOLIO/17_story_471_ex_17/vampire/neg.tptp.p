fof(rabbit_spotted_cute, axiom, ! [X] : ((rabbit(X) & spotted_near_campus(X)) => cute(X))).
fof(some_turtle_spotted, axiom, ? [X] : (turtle(X) & spotted_near_campus(X))).
fof(only_animals_spotted, axiom, ! [X] : ((animal(X) & spotted_near_campus(X)) => (rabbit(X) | squirrel(X)))).
fof(skittish_not_calm, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(squirrel_spotted_skittish, axiom, ! [X] : ((squirrel(X) & spotted_near_campus(X)) => skittish(X))).
fof(rabbit_is_animal, axiom, ! [X] : (rabbit(X) => animal(X))).
fof(turtle_is_animal, axiom, ! [X] : (turtle(X) => animal(X))).
fof(squirrel_is_animal, axiom, ! [X] : (squirrel(X) => animal(X))).
fof(rockie_spotted, axiom, spotted_near_campus(rockie)).
fof(rockie_calm, axiom, calm(rockie)).
fof(conjecture, conjecture, ~turtle(rockie)).