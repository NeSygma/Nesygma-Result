fof(managed_building_def, axiom, managed_building(olive_garden)).
fof(allows_pets_some, axiom, allows_pets(olive_garden)).
fof(requires_deposit, axiom, requires_deposit(olive_garden)).
fof(deposit_rule, axiom,
    ! [D] : (deposit(olive_garden, D) => (D = 2000 | D > 2000))).
fof(monthly_rent_olive_garden, axiom, monthly_rent(olive_garden, 2000)).
fof(more_than_2000_1500, axiom, more_than(2000, 1500)).
fof(cat_is_pet, axiom, cat_is_pet).
fof(fluffy_is_tom_cat, axiom, is_cat(fluffy, tom)).
fof(pets_allowed_implies_move_in_allowed, axiom,
    ! [B, P, Pet] :
      (allows_pets(B) &
       is_cat(Pet, P) =>
       allowed_to_move_in_with_pet(P, Pet))).
fof(tom_renting_condition, axiom,
    (will_rent(tom, olive_garden) <=>
     (allowed_to_move_in_with_pet(tom, fluffy) &
      ? [Deposit] : (deposit(olive_garden, Deposit) & Deposit =< 1500)))).

fof(goal, conjecture,
    ? [D] : (deposit(olive_garden, D) & (D = 2000 | D > 2000))).