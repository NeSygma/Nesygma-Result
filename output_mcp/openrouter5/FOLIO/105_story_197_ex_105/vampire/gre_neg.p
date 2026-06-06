% Negative version: Conjecture is "ETS does NOT provide financial aid to Tom"
fof(cost_premise, axiom, $greater(300, 205)).
fof(financial_aid_rule, axiom, ! [X] : ((gre_applicant(X) & proves_economic_hardship(X)) => ets_financial_aid(X))).
fof(hardship_rule, axiom, ! [X] : ((single_parent_family(X) | few_resources(X)) => proves_economic_hardship(X))).
fof(tom_single_parent, axiom, single_parent_family(tom)).
fof(tom_few_resources, axiom, few_resources(tom)).
fof(tom_applicant, axiom, gre_applicant(tom)).
fof(goal_neg, conjecture, ~ets_financial_aid(tom)).