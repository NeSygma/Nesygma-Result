fof(spills_implies_not_tidy, axiom, ! [P] : (spills_food_on_clothing(P) => ~notably_tidy(P))).
fof(clumsy_implies_spills, axiom, ! [P] : (clumsy_foodies(P) => spills_food_on_clothing(P))).
fof(cleanly_implies_tidy, axiom, ! [P] : (cleanly(P) => notably_tidy(P))).
fof(values_order_implies_cleanly, axiom, ! [P] : (values_order_spotlessness(P) => cleanly(P))).
fof(family_prioritizes_implies_values, axiom, ! [P] : (family_prioritizes_order_spotlessness(P) => values_order_spotlessness(P))).
fof(peter_choice, axiom, (spills_food_on_clothing(peter) & cleanly(peter)) | (~spills_food_on_clothing(peter) & ~cleanly(peter))).
fof(conclusion_negation, conjecture, ~((clumsy_foodies(peter) & family_prioritizes_order_spotlessness(peter)) | (~clumsy_foodies(peter) & ~family_prioritizes_order_spotlessness(peter)))).