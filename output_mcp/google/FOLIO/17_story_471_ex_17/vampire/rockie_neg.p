fof(p1, axiom, ! [X] : ((rabbit(X) & spotted(X)) => cute(X))).
fof(p2, axiom, ? [X] : (turtle(X) & spotted(X))).
fof(p3, axiom, ! [X] : (spotted(X) => (rabbit(X) | squirrel(X)))).
fof(p4, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(p5, axiom, ! [X] : ((squirrel(X) & spotted(X)) => skittish(X))).
fof(p6, axiom, (spotted(rockie) & calm(rockie))).
fof(disjoint, axiom, ! [X] : ((rabbit(X) => (~turtle(X) & ~squirrel(X))) & (turtle(X) => (~rabbit(X) & ~squirrel(X))) & (squirrel(X) => (~rabbit(X) & ~turtle(X))))).
fof(goal, conjecture, ~turtle(rockie)).