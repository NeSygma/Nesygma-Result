% Positive version
fof(premise1, axiom, ! [X] : ((rabbit(X) & spotted(X)) => cute(X))).
fof(premise2, axiom, ? [X] : (turtle(X) & spotted(X))).
fof(premise3, axiom, ! [X] : (spotted(X) => (rabbit(X) | squirrel(X)))).
fof(premise4, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(premise5, axiom, ! [X] : ((squirrel(X) & spotted(X)) => skittish(X))).
fof(premise6, axiom, spotted(rockie) & calm(rockie)).
fof(goal, conjecture, (turtle(rockie) | cute(rockie))).