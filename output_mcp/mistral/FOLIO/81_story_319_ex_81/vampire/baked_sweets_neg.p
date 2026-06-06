fof(no_baked_sweets_are_spicy, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(all_cupcakes_are_baked_sweets, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(all_mala_hotpots_are_spicy, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(all_baked_by_melissa_are_cupcakes, axiom, ! [X] : (product_from_baked_by_melissa(X) => cupcake(X))).
fof(dried_thai_chilies_property, axiom, spicy(dried_thai_chilies) | mala_hotpot(dried_thai_chilies) | ~baked_sweet(dried_thai_chilies)).
fof(goal, conjecture, ~mala_hotpot(dried_thai_chilies)).