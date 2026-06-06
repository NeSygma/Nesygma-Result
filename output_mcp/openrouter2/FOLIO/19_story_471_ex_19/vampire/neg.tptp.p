fof(rule1, axiom, ! [X] : ((rabbit(X) & spotted_near_campus(X)) => cute(X))).
fof(rule2, axiom, ? [X] : (turtle(X) & spotted_near_campus(X))).
fof(rule3, axiom, ! [X] : (spotted_near_campus(X) => (rabbit(X) | squirrel(X)))).
fof(rule4, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(rule5, axiom, ! [X] : ((squirrel(X) & spotted_near_campus(X)) => skittish(X))).
fof(fact1, axiom, spotted_near_campus(rockie)).
fof(fact2, axiom, calm(rockie)).
fof(goal, conjecture, ~ (turtle(rockie) | cute(rockie))).