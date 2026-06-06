fof(premise1, axiom, ! [X] : (spill_food(X) => ~tidy(X))).
fof(premise2, axiom, ! [X] : ((clumsy_foodie(X) & go_out_frequently_find_new_food_restaurants(X)) => spill_food(X))).
fof(premise3, axiom, ! [X] : (cleanly(X) => tidy(X))).
fof(premise4, axiom, ! [X] : (value_order_and_spotlessness(X) => cleanly(X))).
fof(premise5, axiom, ! [X] : (family_prioritizes_order_and_spotlessness(X) => value_order_and_spotlessness(X))).
fof(premise6, axiom, (spill_food(peter) & cleanly(peter)) | (~spill_food(peter) & ~cleanly(peter))).
fof(conjecture, conjecture, ~(((clumsy_foodie(peter) & go_out_frequently_find_new_food_restaurants(peter)) & family_prioritizes_order_and_spotlessness(peter)) | ((~(clumsy_foodie(peter) & go_out_frequently_find_new_food_restaurants(peter))) & ~family_prioritizes_order_and_spotlessness(peter)))).