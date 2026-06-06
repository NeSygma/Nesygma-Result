fof(no_baked_sweet_spicy, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(cupcake_is_baked, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(mala_is_spicy, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(melissa_is_cupcake, axiom, ! [X] : (baked_by_melissa(X) => cupcake(X))).
fof(dried_chilies_fact, axiom, (spicy(dried_thai_chilies) | mala_hotpot(dried_thai_chilies) | ~baked_sweet(dried_thai_chilies))).
fof(goal, conjecture, ~baked_by_melissa(dried_thai_chilies)).