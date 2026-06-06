fof(premise_baked_sweet_not_spicy, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(premise_cupcake_baked_sweet, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(premise_mala_hotpot_spicy, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(premise_BBM_cupcake, axiom, ! [X] : (product_from_bbm(X) => cupcake(X))).
fof(fact_spicy_or_mala_or_notbaked, axiom, spicy(dried_thai_chili) | mala_hotpot(dried_thai_chili) | ~baked_sweet(dried_thai_chili)).
fof(conclusion, conjecture, ~product_from_bbm(dried_thai_chili)).