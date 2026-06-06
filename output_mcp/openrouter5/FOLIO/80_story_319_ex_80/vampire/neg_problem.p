% Negative version: negated conclusion as conjecture
% Negated conclusion: Dried Thai chilies ARE products of Baked by Melissa.
% i.e., product_of_baked_by_melissa(dried_thai_chilies)

fof(premise_1, axiom, ! [X] : (baked_sweet(X) => ~spicy(X))).
fof(premise_2, axiom, ! [X] : (cupcake(X) => baked_sweet(X))).
fof(premise_3, axiom, ! [X] : (mala_hotpot(X) => spicy(X))).
fof(premise_4, axiom, ! [X] : (product_of_baked_by_melissa(X) => cupcake(X))).
fof(premise_5, axiom, ! [X] : (dried_thai_chili(X) => (spicy(X) | mala_hotpot(X) | ~baked_sweet(X)))).

fof(fact_dtc, axiom, dried_thai_chili(dried_thai_chilies)).

fof(distinct, axiom, $true).

fof(goal, conjecture, product_of_baked_by_melissa(dried_thai_chilies)).