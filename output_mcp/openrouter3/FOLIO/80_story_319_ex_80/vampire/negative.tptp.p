% Problem: Dried Thai Chilies - Negative
% Premises and NEGATED conclusion that dried Thai chilies ARE products of Baked by Melissa

fof(no_baked_sweets_spicy, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(cupcakes_are_baked_sweets, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(mala_hotpots_spicy, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(bbm_products_are_cupcakes, axiom, ! [X] : (product_from_bbm(X) => cupcake(X))).

% Dried Thai chilies constant
fof(dtc_constant, axiom, dtc = dtc).

% Premise 5: Dried Thai chilies are spicy or mala hotpots or not baked sweets
fof(dtc_properties, axiom, spicy(dtc) | mala_hotpot(dtc) | ~baked_sweet(dtc)).

% NEGATED Conclusion: Dried Thai chilies ARE products of Baked by Melissa
fof(goal, conjecture, product_from_bbm(dtc)).