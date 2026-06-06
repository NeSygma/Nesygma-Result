% Positive version: Original conclusion as conjecture
fof(no_baked_sweets_spicy, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(cupcakes_are_baked_sweets, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(mala_hotpots_spicy, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(products_from_bbm_are_cupcakes, axiom, ! [X] : (product_from(X, baked_by_melissa) => cupcake(X))).
fof(dried_thai_chilies_property, axiom, spicy(dried_thai_chilies) | mala_hotpot(dried_thai_chilies) | ~baked_sweet(dried_thai_chilies)).
fof(goal, conjecture, product_from(dried_thai_chilies, baked_by_melissa)).