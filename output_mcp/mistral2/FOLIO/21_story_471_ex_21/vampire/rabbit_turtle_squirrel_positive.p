fof(premise1, axiom, ! [X] : (can_be_spotted_near_campus(X) & rabbit(X) => cute(X))).
fof(premise2, axiom, ? [X] : (can_be_spotted_near_campus(X) & turtle(X))).
fof(premise3, axiom, ! [X] : (can_be_spotted_near_campus(X) => (rabbit(X) | squirrel(X)))).
fof(premise4, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(premise5, axiom, ! [X] : (can_be_spotted_near_campus(X) & squirrel(X) => skittish(X))).
fof(premise6a, axiom, can_be_spotted_near_campus(rockie)).
fof(premise6b, axiom, calm(rockie)).

fof(conclusion, conjecture, (cute(rockie) & calm(rockie)) => (turtle(rockie) & skittish(rockie))).