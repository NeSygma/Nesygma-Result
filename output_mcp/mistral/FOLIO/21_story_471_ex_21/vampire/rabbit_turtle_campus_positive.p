fof(rule_1, axiom, ! [X] : ((rabbit(X) & can_be_spotted_near_campus(X)) => cute(X))).
fof(rule_2, axiom, ? [X] : (turtle(X) & can_be_spotted_near_campus(X))).
fof(rule_3, axiom, ! [X] : (can_be_spotted_near_campus(X) => (rabbit(X) | squirrel(X)))).
fof(rule_4, axiom, ! [X] : (skittish(X) => ~calm(X))).
fof(rule_5, axiom, ! [X] : ((squirrel(X) & can_be_spotted_near_campus(X)) => skittish(X))).
fof(fact_1, axiom, can_be_spotted_near_campus(rockie)).
fof(fact_2, axiom, calm(rockie)).
fof(conclusion, conjecture, ((cute(rockie) & calm(rockie)) => (skittish(rockie) & turtle(rockie)))).