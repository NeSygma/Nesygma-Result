fof(no_baked_sweets_spicy, axiom, ! [X] : (baked_sweets(X) => ~spicy(X))).
fof(all_cupcakes_baked_sweets, axiom, ! [X] : (cupcake(X) => baked_sweets(X))).
fof(all_mala_hotpots_spicy, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(all_baked_by_melissa_products_cupcakes, axiom, ! [X] : (baked_by_melissa_product(X) => cupcake(X))).
fof(dried_thai_chilies_disjunction, axiom, (spicy(dried_thai_chilies) | mala_hotpot(dried_thai_chilies) | ~baked_sweets(dried_thai_chilies))).
fof(conjecture, conjecture, (~cupcake(dried_thai_chilies) | ~baked_by_melissa_product(dried_thai_chilies))).