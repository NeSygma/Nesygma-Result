tff(test_type, type, test: $tType).

tff(costs_decl, type, costs: (test * $int) > $o).

tff(gre_test_decl, type, gre_test: test).

tff(gre_test_cost, axiom, costs(gre_test, 205)).
tff(cheaper_than_300, axiom, $less(205, 300)).
tff(goal_negation, conjecture, ~(? [A: $int] : (costs(gre_test, A) & $less(A, 300)))).