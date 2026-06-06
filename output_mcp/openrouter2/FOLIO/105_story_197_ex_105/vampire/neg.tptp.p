fof(applicant_tom, axiom, applicant(tom, gre)).
fof(single_parent_tom, axiom, single_parent_family(tom)).
fof(few_resources_tom, axiom, few_resources(tom)).
fof(prove_hardship_rule, axiom, ! [X] : ((single_parent_family(X) | few_resources(X)) => proves_economic_hardship(X))).
fof(provide_rule, axiom, ! [X] : ((applicant(X, gre) & proves_economic_hardship(X)) => provides_financial_aid(ets, X))).
fof(conjecture, conjecture, ~provides_financial_aid(ets, tom)).