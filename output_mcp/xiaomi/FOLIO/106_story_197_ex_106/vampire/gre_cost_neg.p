tff(gre_cost_type, type, gre_cost: $int).
tff(threshold_type, type, threshold_300: $int).

tff(gre_cost_val, axiom, gre_cost = 205).
tff(threshold_val, axiom, threshold_300 = 300).

tff(cost_below_300, axiom, $less(gre_cost, threshold_300)).

tff(goal, conjecture, ~$less(gre_cost, threshold_300)).