fof(axiom_rabbit_cute, axiom, ! [X] : ((rabbit(X) & can_be_spotted_near_campus(X)) => cute(X))).
fof(axiom_turtle_exists, axiom, ? [X] : (turtle(X) & can_be_spotted_near_campus(X))).
fof(axiom_only_animals, axiom, ! [X] : (can_be_spotted_near_campus(X) => (rabbit(X) | squirrel(X)))).
fof(axiom_skittish_not_calm, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(axiom_squirrel_skittish, axiom, ! [X] : ((squirrel(X) & can_be_spotted_near_campus(X)) => skittish(X))).
fof(fact_rockie_spotted, axiom, can_be_spotted_near_campus(rockie)).
fof(fact_rockie_calm, axiom, calm(rockie)).
fof(conclusion, conjecture, ((cute(rockie) & calm(rockie)) => (turtle(rockie) & skittish(rockie)))).