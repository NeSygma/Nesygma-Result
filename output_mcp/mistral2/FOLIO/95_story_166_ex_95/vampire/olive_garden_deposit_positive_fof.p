% Define sorts as uninterpreted types (FOF does not support type declarations directly)

% Constants
fof(olive_garden_is_managed_building, axiom, managed_building(olive_garden)).
fof(fluffy_is_tom_cat, axiom, is_cat(fluffy, tom)).
fof(cat_is_pet, axiom, cat_is_pet).
fof(allows_pets_olive_garden, axiom, allows_pets(olive_garden)).
fof(requires_deposit_olive_garden, axiom, requires_deposit(olive_garden)).
fof(monthly_rent_olive_garden, axiom, monthly_rent(olive_garden, 2000)).
fof(more_than_2000_1500, axiom, 2000 > 1500).

% Predicates and rules
fof(pets_allowed_implies_move_in_allowed, axiom,
    ! [B, P, Pet] :
      (allows_pets(B) & is_cat(Pet, P) => allowed_to_move_in_with_pet(P, Pet))).

fof(deposit_rule, axiom,
    ! [B, D] :
      (deposit(B, D) => (D = 2000 | D > 2000))).

fof(tom_renting_condition, axiom,
    (will_rent(tom, olive_garden) <=>
     (allowed_to_move_in_with_pet(tom, fluffy) &
      ? [Deposit] : (deposit(olive_garden, Deposit) & Deposit =< 1500)))).

% Goal: The security deposit at the Olive Garden is either $2000 or more.
fof(goal, conjecture,
    ? [D] : (deposit(olive_garden, D) & (D = 2000 | D > 2000))).