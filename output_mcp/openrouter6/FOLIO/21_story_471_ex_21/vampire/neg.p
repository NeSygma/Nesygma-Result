fof(premise1, axiom, ! [X] : ((rabbit(X) & spotted_near_campus(X)) => cute(X))).
fof(premise2, axiom, ? [X] : (turtle(X) & spotted_near_campus(X))).
fof(premise3, axiom, ! [X] : (spotted_near_campus(X) => (rabbit(X) | squirrel(X)))).
fof(premise4, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(premise5, axiom, ! [X] : ((squirrel(X) & spotted_near_campus(X)) => skittish(X))).
fof(premise6, axiom, spotted_near_campus(rockie) & calm(rockie)).
fof(distinct, axiom, rockie != t1).
fof(goal, conjecture, cute(rockie) & calm(rockie) & ~(skittish(rockie) & turtle(rockie))).