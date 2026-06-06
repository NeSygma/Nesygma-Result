% Negative version (negated conjecture)
fof(distinct_consts, axiom, (rockie != turtle1)).

% Premises
fof(premise1, axiom, ! [X] : ((rabbit(X) & spotted(X)) => cute(X))).
fof(premise2, axiom, turtle(turtle1) & spotted(turtle1)).
fof(premise3, axiom, ! [X] : (spotted(X) => (rabbit(X) | squirrel(X)))).
fof(premise4, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(premise5, axiom, ! [X] : ((squirrel(X) & spotted(X)) => skittish(X))).
fof(premise6, axiom, spotted(rockie) & calm(rockie)).

% Negated conjecture
fof(goal, conjecture, ( cute(rockie) & calm(rockie) & ( ~skittish(rockie) | ~turtle(rockie) ) )).