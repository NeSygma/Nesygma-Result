% Axioms
fof(axiom1, axiom, ! [X] : (spill_lot(X) => ~notable_tidy(X))).
fof(axiom2, axiom, ! [X] : (clumsy(X) & foodie(X) & goes_out_frequently(X) & finds_new_food_restaurants(X) => spill_lot(X))).
fof(axiom3, axiom, ! [X] : (cleanly(X) => notable_tidy(X))).
fof(axiom4, axiom, ! [X] : (value_order_spotlessness(X) => cleanly(X))).
fof(axiom5, axiom, ! [X] : (family_prioritizes_order_spotlessness(X) => value_order_spotlessness(X))).
fof(axiom6, axiom, ((spill_lot(peter) & cleanly(peter)) | (~spill_lot(peter) & ~cleanly(peter)))).
fof(conjecture_pos, conjecture, notable_tidy(peter)).