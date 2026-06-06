fof(rule1, axiom, ! [X] : ((taking_GRE(X) & proves_economic_hardship(X)) => has_financial_aid(X))).
fof(rule2, axiom, ! [X] : ((single_parent_family(X) | few_resources(X)) => proves_economic_hardship(X))).
fof(fact1, axiom, single_parent_family(tom)).
fof(fact2, axiom, few_resources(tom)).
fof(fact3, axiom, taking_GRE(tom)).
fof(conjecture, conjecture, ? [X] : (taking_GRE(X) & has_financial_aid(X))).