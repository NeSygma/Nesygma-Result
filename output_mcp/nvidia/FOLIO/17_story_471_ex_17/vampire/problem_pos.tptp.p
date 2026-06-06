% FOF encoding of premises and conjecture turtle(rockie)
fof(premise1, axiom, ! [X] : ((rabbit(X) & spotted_near_campus(X)) => cute(X))).
fof(premise2, axiom, ? [X] : (turtle(X) & spotted_near_campus(X))).
fof(premise3, axiom, ! [X] : (spotted_near_campus(X) => (rabbit(X) | squirrel(X))) ).
fof(premise4, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(premise5, axiom, ! [X] : ((squirrel(X) & spotted_near_campus(X)) => skittish(X))).
fof(fact_spotted_rockie, axiom, spotted_near_campus(rockie)).
fof(fact_calm_rockie, axiom, calm(rockie)).
fof(conclusion, conjecture, turtle(rockie)).