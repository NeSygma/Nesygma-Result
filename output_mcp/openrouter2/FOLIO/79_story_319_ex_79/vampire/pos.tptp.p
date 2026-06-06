fof(no_baked_sweets_spicy, axiom, ![X] : (baked_sweets(X) => ~spicy(X))).
fof(all_cupcakes_baked_sweets, axiom, ![X] : (cupcake(X) => baked_sweets(X))).
fof(all_mala_hotpots_spicy, axiom, ![X] : (mala_hotpot(X) => spicy(X))).
fof(all_products_baked_by_melissa_cupcakes, axiom, ![X] : (product_of_baked_by_melissa(X) => cupcake(X))).
fof(disjunction_dried_thai_chilies, axiom, spicy(dried_thai_chilies) | mala_hotpot(dried_thai_chilies) | ~baked_sweets(dried_thai_chilies)).
fof(conclusion, conjecture, product_of_baked_by_melissa(dried_thai_chilies)).