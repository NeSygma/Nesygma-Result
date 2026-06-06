fof(axiom_rabbit_cute, axiom, ! [X] : (rabbit(X) & spotted_near_campus(X) => cute(X))).
fof(axiom_some_turtle_spotted, axiom, ? [X] : (turtle(X) & spotted_near_campus(X))).
fof(axiom_only_rabbit_squirrel, axiom, ! [X] : (spotted_near_campus(X) => (rabbit(X) | squirrel(X)))).
fof(axiom_skittish_not_calm, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(axiom_squirrel_spotted_skittish, axiom, ! [X] : (squirrel(X) & spotted_near_campus(X) => skittish(X))).
fof(axiom_rockie_spotted, axiom, spotted_near_campus(rockie)).
fof(axiom_rockie_calm, axiom, calm(rockie)).
fof(conjecture_neg, conjecture, (~turtle(rockie) & ~cute(rockie))).