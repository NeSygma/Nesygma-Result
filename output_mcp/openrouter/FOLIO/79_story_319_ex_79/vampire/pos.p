fof(no_baked_spicy, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(all_cupcakes_baked, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(all_mala_spicy, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(all_bbm_cupcake, axiom, ! [X] : (product_of_bbm(X) => cupcake(X))).
fof(dried_info, axiom, spicy(dried_thai_chilies) | mala_hotpot(dried_thai_chilies) | ~baked_sweet(dried_thai_chilies)).
fof(goal, conjecture, product_of_bbm(dried_thai_chilies)).