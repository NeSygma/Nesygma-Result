% Positive conjecture: Rockie is not a turtle
fof(distinct_rockie_t1, axiom, rockie != t1).
fof(rule1, axiom, ! [X] : ((rabbit(X) & spotted(X)) => cute(X))).
fof(rule2, axiom, turtle(t1)).
fof(rule2_spot, axiom, spotted(t1)).
fof(rule3, axiom, ! [X] : (spotted(X) => (rabbit(X) | squirrel(X)))).
fof(rule4, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(rule5, axiom, ! [X] : ((squirrel(X) & spotted(X)) => skittish(X))).
fof(fact_rockie, axiom, spotted(rockie)).
fof(fact_rockie_calm, axiom, calm(rockie)).
fof(goal, conjecture, ~turtle(rockie)).