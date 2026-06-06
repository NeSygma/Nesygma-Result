% Negative test (negated claim)
fof(rule_aid, axiom, ! [X] : ((gre_applicant(X) & economic_hardship(X)) => provides_aid(X))).
fof(rule_hardship, axiom, ! [X] : ((single_parent_family(X) | few_resources(X)) => economic_hardship(X))).
fof(fact_single, axiom, single_parent_family(tom)).
fof(fact_few, axiom, few_resources(tom)).
fof(fact_applicant, axiom, gre_applicant(tom)).
fof(goal, conjecture, ~provides_aid(tom)).