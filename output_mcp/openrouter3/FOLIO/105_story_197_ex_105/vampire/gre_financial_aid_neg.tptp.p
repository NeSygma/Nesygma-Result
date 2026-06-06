% Negative version: ETS does NOT provide financial aid to Tom
tff(cost_type, type, cost: ($i * $int) > $o).
tff(financial_aid_type, type, financial_aid: $i > $o).
tff(economic_hardship_type, type, economic_hardship: $i > $o).
tff(single_parent_family_type, type, single_parent_family: $i > $o).
tff(few_resources_type, type, few_resources: $i > $o).
tff(applying_type, type, applying: $i > $o).
tff(gre_test_decl, type, gre_test: $i).
tff(tom_decl, type, tom: $i).

tff(cost_gre, axiom, cost(gre_test, 205)).
tff(cheaper_than_300, axiom, $less(cost(gre_test, 205), 300)).
tff(financial_aid_rule, axiom, ! [X: $i] : ((applying(X) & economic_hardship(X)) => financial_aid(X))).
tff(economic_hardship_rule, axiom, ! [X: $i] : ((single_parent_family(X) | few_resources(X)) => economic_hardship(X))).
tff(tom_single_parent, axiom, single_parent_family(tom)).
tff(tom_few_resources, axiom, few_resources(tom)).
tff(tom_applying, axiom, applying(tom)).
tff(goal, conjecture, ~financial_aid(tom)).