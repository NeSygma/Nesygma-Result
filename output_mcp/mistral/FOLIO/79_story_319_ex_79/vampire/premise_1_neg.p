fof(baked_sweet_not_spicy, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(cupcake_is_baked_sweet, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(mala_hotpot_is_spicy, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(baked_by_melissa_is_cupcake, axiom, ! [X] : (product_of_baked_by_melissa(X) => cupcake(X))).
fof(dried_thai_chilies_property, axiom, spicy(dried_thai_chilies) | mala_hotpot(dried_thai_chilies) | ~baked_sweet(dried_thai_chilies)).
fof(conclusion_negation, conjecture, ~product_of_baked_by_melissa(dried_thai_chilies)).