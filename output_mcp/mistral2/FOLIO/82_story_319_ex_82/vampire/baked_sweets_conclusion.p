fof(baked_sweet_not_spicy, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(all_cupcakes_are_baked_sweets, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(all_mala_hotpots_are_spicy, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(all_baked_by_melissa_are_cupcakes, axiom, ! [X] : (product_of_baked_by_melissa(X) => cupcake(X))).
fof(dried_thai_chili_property, axiom, ! [X] : (dried_thai_chili(X) => (spicy(X) | mala_hotpot(X) | ~baked_sweet(X)))).

fof(conclusion, conjecture, ! [X] : (dried_thai_chili(X) => (~product_of_baked_by_melissa(X) & ~baked_sweet(X)))).