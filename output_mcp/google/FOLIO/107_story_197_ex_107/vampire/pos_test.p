fof(applicant_rule, axiom, ! [X] : ((applicant(X) & proves_economic_hardship(X)) => has_financial_aid(X))).
fof(hardship_rule, axiom, ! [X] : ((lives_in_single_parent_family(X) | has_few_resources(X)) => proves_economic_hardship(X))).
fof(tom_fact_1, axiom, lives_in_single_parent_family(tom)).
fof(tom_fact_2, axiom, has_few_resources(tom)).
fof(tom_fact_3, axiom, applicant(tom)).
fof(goal, conjecture, ! [X] : (applicant(X) => ~has_financial_aid(X))).