tff(gre_cost, type, gre_test_cost: $int).
tff(cheaper_than_300, axiom, gre_test_cost = 205).


tff(goal_neg, conjecture, $greatereq(gre_test_cost, 300)).