fof(rabbit_cute_rule, axiom, ! [X] : ((rabbit(X) & near_campus(X)) => cute(X))).
fof(turtle_near_exists, axiom, ? [X] : (turtle(X) & near_campus(X))).
fof(near_only_rabbits_squirrels, axiom, ! [X] : (near_campus(X) => (rabbit(X) | squirrel(X)))).
fof(skittish_not_calm, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(squirrel_skittish_rule, axiom, ! [X] : ((squirrel(X) & near_campus(X)) => skittish(X))).
fof(rockie_near, axiom, near_campus(rockie)).
fof(rockie_calm, axiom, calm(rockie)).
fof(conjecture, conjecture, ~((cute(rockie) & calm(rockie)) => (skittish(rockie) & turtle(rockie)))).