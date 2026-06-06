fof(premise_1, axiom, ! [X] : ((rabbit(X) & spotted(X)) => cute(X))).
fof(premise_2, axiom, ? [X] : (turtle(X) & spotted(X))).
fof(premise_3, axiom, ! [X] : (spotted(X) => (rabbit(X) | squirrel(X)))).
fof(premise_4, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(premise_5, axiom, ! [X] : ((squirrel(X) & spotted(X)) => skittish(X))).
fof(premise_6, axiom, spotted(rockie) & calm(rockie)).
fof(goal, conjecture, (cute(rockie) & calm(rockie)) => (skittish(rockie) & turtle(rockie))).