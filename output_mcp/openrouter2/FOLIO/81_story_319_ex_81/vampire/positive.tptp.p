fof(no_baked_sweets_spicy, axiom, ! [X] : (baked_sweets(X) => ~spicy(X))).
fof(cupcakes_baked_sweets, axiom, ! [X] : (cupcake(X) => baked_sweets(X))).
fof(mala_hotpots_spicy, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(baked_by_melissa_cupcakes, axiom, ! [X] : (baked_by_melissa(X) => cupcake(X))).
fof(dried_thai_chilies_statement, axiom, (spicy(dried_thai_chilies) | mala_hotpot(dried_thai_chilies) | ~baked_sweets(dried_thai_chilies))).
fof(conjecture, conjecture, mala_hotpot(dried_thai_chilies)).