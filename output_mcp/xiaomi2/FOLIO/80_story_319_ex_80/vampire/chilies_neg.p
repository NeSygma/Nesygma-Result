fof(no_baked_sweet_spicy, axiom,
    ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(all_cupcake_baked_sweet, axiom,
    ! [X] : (cupcake(X) => baked_sweet(X))).
fof(all_mala_hotpot_spicy, axiom,
    ! [X] : (mala_hotpot(X) => spicy(X))).
fof(all_melissa_cupcake, axiom,
    ! [X] : (baked_by_melissa(X) => cupcake(X))).
fof(dried_thai_chilies_disjunction, axiom,
    (spicy(dried_thai_chilies) | mala_hotpot(dried_thai_chilies) | ~baked_sweet(dried_thai_chilies))).
fof(goal, conjecture,
    baked_by_melissa(dried_thai_chilies)).