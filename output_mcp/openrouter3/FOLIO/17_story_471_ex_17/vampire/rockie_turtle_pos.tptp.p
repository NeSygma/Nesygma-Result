% Positive version: Rockie is a turtle
fof(rabbit_cute, axiom, ! [X] : (rabbit(X) & spotted_near_campus(X) => cute(X))).
fof(turtle_spotted, axiom, ? [X] : (turtle(X) & spotted_near_campus(X))).
fof(only_rabbits_squirrels, axiom, ! [X] : (spotted_near_campus(X) => (rabbit(X) | squirrel(X)))).
fof(skittish_not_calm, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(squirrel_skittish, axiom, ! [X] : (squirrel(X) & spotted_near_campus(X) => skittish(X))).
fof(rockie_fact, axiom, spotted_near_campus(rockie) & calm(rockie)).
fof(goal, conjecture, turtle(rockie)).