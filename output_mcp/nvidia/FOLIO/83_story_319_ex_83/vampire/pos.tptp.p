% Axioms
fof(axiom_no_baked_sweet_spicy, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(axiom_all_cupcakes_baked_sweet, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(axiom_all_mala_hotpot_spicy, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(axiom_all_BBM_products_cupcakes, axiom, ! [X] : (baked_by_melissa(X) => cupcake(X))).
fof(axiom_dried_thaichili_disjunction, axiom, spicy(dried_thaichili) | mala_hotpot(dried_thaichili) | ~baked_sweet(dried_thaichili)).
% Conjecture
fof(conjecture_dried_thaichili_cupcake_BBM, conjecture, cupcake(dried_thaichili) & baked_by_melissa(dried_thaichili)).