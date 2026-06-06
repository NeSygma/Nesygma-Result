fof(no_baked_sweets_spicy, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(cupcakes_are_baked_sweets, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(mala_hotpots_spicy, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(bbm_products_are_cupcakes, axiom, ! [X] : (bbm(X) => cupcake(X))).
fof(dtc_properties, axiom, spicy(dtc) | mala_hotpot(dtc) | ~baked_sweet(dtc)).
fof(goal, conjecture, ~bbm(dtc)).