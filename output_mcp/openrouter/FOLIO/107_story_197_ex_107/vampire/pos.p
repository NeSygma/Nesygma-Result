fof(rule1, axiom, ![X] : ((single_parent(X) | few_resources(X)) => economic_hardship(X))).
fof(rule2, axiom, ![X] : ((applies_gre(X) & economic_hardship(X)) => financial_aid(X))).
fof(fact1, axiom, single_parent(tom)).
fof(fact2, axiom, few_resources(tom)).
fof(fact3, axiom, applies_gre(tom)).
fof(goal, conjecture, ![X] : (applies_gre(X) => ~financial_aid(X))).