% Positive version: Original conclusion as conjecture
fof(no_baked_sweets_spicy, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(cupcakes_are_baked_sweets, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(mala_hotpots_spicy, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(baked_by_melissa_cupcakes, axiom, ! [X] : (baked_by_melissa(X) => cupcake(X))).
fof(dried_thai_chili_properties, axiom, ! [X] : (dried_thai_chili(X) => (spicy(X) | mala_hotpot(X) | ~baked_sweet(X)))).
fof(dried_thai_chili_exists, axiom, dried_thai_chili(dried_thai_chili)).
fof(goal, conjecture, mala_hotpot(dried_thai_chili)).