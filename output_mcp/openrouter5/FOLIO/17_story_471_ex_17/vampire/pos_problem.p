% Positive version: original claim "Rockie is a turtle" as conjecture
fof(premise_1, axiom, ! [X] : ((rabbit(X) & spotted_near_campus(X)) => cute(X))).
fof(premise_2, axiom, ? [X] : (turtle(X) & spotted_near_campus(X))).
fof(premise_3, axiom, ! [X] : (spotted_near_campus(X) => (rabbit(X) | squirrel(X)))).
fof(premise_4, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(premise_5, axiom, ! [X] : ((squirrel(X) & spotted_near_campus(X)) => skittish(X))).
fof(premise_6, axiom, spotted_near_campus(rockie)).
fof(premise_7, axiom, calm(rockie)).
fof(goal, conjecture, turtle(rockie)).