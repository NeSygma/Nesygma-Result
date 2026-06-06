fof(no_baked_sweets_are_spicy, axiom, ! [X] : (baked_sweets(X) => ~spicy(X))).
fof(all_cupcakes_are_baked_sweets, axiom, ! [X] : (cupcake(X) => baked_sweets(X))).
fof(all_mala_hotpots_are_spicy, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(all_baked_by_melissa_are_cupcakes, axiom, ! [X] : (product_from_baked_by_melissa(X) => cupcake(X))).
fof(dried_thai_chilies_condition, axiom, ! [X] : (dried_thai_chilies(X) => (spicy(X) | mala_hotpot(X) | ~baked_sweets(X)))).

fof(conclusion_negation, conjecture, ~(? [X] : (dried_thai_chilies(X) & mala_hotpot(X)))).