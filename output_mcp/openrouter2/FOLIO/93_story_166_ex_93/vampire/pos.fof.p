fof(managed_building_olive, axiom, managed_building(olive_garden)).
fof(allows_pets_olive, axiom, allows_pets(olive_garden)).
fof(deposit_le_1500_olive, axiom, deposit_le_1500(olive_garden)).
fof(cat_fluffy, axiom, cat(fluffy)).
fof(pet_fluffy, axiom, pet(fluffy)).
fof(move_in_rule, axiom, ! [B] : (managed_building(B) & allows_pets(B) => allowed_to_move_in_with_pet(tom, fluffy, B))).
fof(rent_rule, axiom, ! [B] : (allowed_to_move_in_with_pet(tom, fluffy, B) & deposit_le_1500(B) => rent_apartment(tom, B))).
fof(goal, conjecture, rent_apartment(tom, olive_garden)).