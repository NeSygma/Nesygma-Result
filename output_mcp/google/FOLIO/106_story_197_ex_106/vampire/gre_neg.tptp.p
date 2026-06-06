tff(gre_cost_decl, type, gre_cost: $int).
tff(limit_decl, type, limit: $int).
tff(cost_val, axiom, gre_cost = 205).
tff(limit_val, axiom, limit = 300).
tff(goal, conjecture, ~($less(gre_cost, limit))).