tff(costs_gre, axiom, costs(gre_test, cost_205)).
tff(cost_205_val, axiom, cost_205 = 205).
tff(cost_300_val, axiom, cost_300 = 300).
tff(cheaper_than_gre, axiom, cheaper_than(cost_205, cost_300)).
tff(financial_aid_rule, axiom, ! [X] : (proves_hardship(X) => provides_financial_aid_to(ets, X))).
tff(hardship_rule, axiom, ! [X] : ((lives_in_single_parent_family(X) | has_few_resources(X)) => proves_hardship(X))).
tff(tom_single_parent, axiom, lives_in_single_parent_family(tom)).
tff(tom_few_resources, axiom, has_few_resources(tom)).
tff(tom_applying, axiom, applying_to_gre(tom)).
tff(goal_negation, conjecture, ? [X] : (applying_to_gre(X) & has_financial_aid(X))).