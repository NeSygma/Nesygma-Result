% Negative version

tff(gre_test_decl, type, gre_test: $i).

tff(tom_decl, type, tom: $i).

tff(cost_type, type, cost: ($i * $int) > $o).

tff(cost_fact, axiom, cost(gre_test,205)).

tff(cheaper_fact, axiom, $less(205,300)).

tff(fin_aid_pred, type, financial_aid: $i > $o).

tff(hardship_pred, type, hardship: $i > $o).

tff(single_parent_pred, type, single_parent: $i > $o).

tff(few_resources_pred, type, few_resources: $i > $o).

tff(applying_pred, type, applying: $i > $o).

% Rules

tff(fin_aid_rule, axiom, ! [P: $i] : (hardship(P) => financial_aid(P))).

tff(hardship_rule, axiom, ! [P: $i] : ((single_parent(P) | few_resources(P)) => hardship(P))).

% Tom facts

tff(tom_facts, axiom, single_parent(tom) & few_resources(tom) & applying(tom)).

% Negated goal

tff(goal, conjecture, ~ $less(205,300)).