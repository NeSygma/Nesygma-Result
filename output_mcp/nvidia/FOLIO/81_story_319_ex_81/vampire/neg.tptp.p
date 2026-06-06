%--- Negative TPTP file ---
fof(axiom_no_baked_sweet_spicy, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(axiom_all_cupcakes_baked_sweet, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(axiom_all_mala_hotpot_spicy, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(axiom_all_products_BBM_cupcakes, axiom, ! [X] : (product_from_bmm(X) => cupcake(X))).
fof(premise_dried_thai_chili, axiom, spicy(dried_thai_chili) | mala_hotpot(dried_thai_chili) | ~baked_sweet(dried_thai_chili)).
fof(conjecture, conjecture, ~mala_hotpot(dried_thai_chili)).