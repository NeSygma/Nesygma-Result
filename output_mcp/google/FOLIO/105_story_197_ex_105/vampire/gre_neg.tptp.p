fof(rule_1, axiom, ! [X] : ((is_gre_applicant(X) & proves_economic_hardship(X)) => gets_financial_aid(X))).
fof(rule_2, axiom, ! [X] : ((lives_in_single_parent_family(X) | has_few_resources(X)) => proves_economic_hardship(X))).
fof(fact_1, axiom, is_gre_applicant(tom)).
fof(fact_2, axiom, lives_in_single_parent_family(tom)).
fof(fact_3, axiom, has_few_resources(tom)).
fof(goal, conjecture, ~gets_financial_aid(tom)).