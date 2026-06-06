fof(no_baked_sweets_spicy, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(cupcakes_are_baked_sweets, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(mala_hotpots_spicy, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(products_from_bbm_are_cupcakes, axiom, ! [X] : (product_from_baked_by_melissa(X) => cupcake(X))).
fof(dried_thai_chilies_property, axiom, spicy(dried_thai_chilies) | mala_hotpot(dried_thai_chilies) | ~baked_sweet(dried_thai_chilies)).
fof(distinct_entities, axiom, (dried_thai_chilies != baked_sweets & dried_thai_chilies != spicy & dried_thai_chilies != cupcakes & dried_thai_chilies != mala_hotpots & dried_thai_chilies != products_from_baked_by_melissa)).
fof(goal, conjecture, ~(cupcake(dried_thai_chilies) & product_from_baked_by_melissa(dried_thai_chilies))).