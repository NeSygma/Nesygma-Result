fof(premise_1, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(premise_2, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(premise_3, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(premise_4, axiom, ! [X] : (product_of_baked_by_melissa(X) => cupcake(X))).
fof(premise_5, axiom, ! [X] : (dried_thai_chili(X) => (spicy(X) | mala_hotpot(X) | ~baked_sweet(X)))).

fof(conclusion_negation, conjecture, ~(? [X] : (dried_thai_chili(X) & cupcake(X) & product_of_baked_by_melissa(X)))).