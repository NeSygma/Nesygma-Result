fof(spills_tidy, axiom, ! [X] : (spills_food(X) => ~tidy(X))).
fof(clumsy_spills, axiom, ! [X] : ((clumsy_foodie(X) & goes_out_frequently(X)) => spills_food(X))).
fof(cleanly_tidy, axiom, ! [X] : (cleanly(X) => tidy(X))).
fof(value_cleanly, axiom, ! [X] : (value_order(X) => cleanly(X))).
fof(family_value, axiom, ! [X] : (family_prioritizes_order(X) => value_order(X))).
fof(peter_disjunction, axiom, ((spills_food(p) & cleanly(p)) | (~spills_food(p) & ~cleanly(p)))).
fof(conjecture, conjecture, ((clumsy_foodie(p) & goes_out_frequently(p)) | family_prioritizes_order(p))).