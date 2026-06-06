% Define sorts

% Managed buildings
fof(managed_building_type, type, managed_building: $tType).
fof(olive_garden_decl, type, olive_garden: managed_building).

% People
fof(person_type, type, person: $tType).
fof(tom_decl, type, tom: person).

% Pets
fof(pet_type, type, pet: $tType).
fof(fluffy_decl, type, fluffy: pet).

% Cats
fof(cat_type, type, cat: $tType).

% Deposit and rent amounts
fof(amount_type, type, amount: $tType).
fof(dollar_decl, type, dollar: amount > $int).

% Predicates
fof(managed_building_decl, type, managed_building: managed_building > $o).
fof(is_cat_decl, type, is_cat: (pet * person) > $o).
fof(cat_is_pet_decl, type, cat_is_pet: $o).
fof(allows_pets_decl, type, allows_pets: managed_building > $o).
fof(requires_deposit_decl, type, requires_deposit: managed_building > $o).
fof(monthly_rent_decl, type, monthly_rent: (managed_building * amount) > $o).
fof(deposit_decl, type, deposit: (managed_building * amount) > $o).
fof(allowed_to_move_in_with_pet_decl, type, allowed_to_move_in_with_pet: (person * pet) > $o).
fof(will_rent_decl, type, will_rent: (person * managed_building) > $o).

% Constants
fof(olive_garden_is_managed_building, axiom, managed_building(olive_garden)).
fof(fluffy_is_tom_cat, axiom, is_cat(fluffy, tom)).
fof(cat_is_pet, axiom, cat_is_pet).
fof(allows_pets_olive_garden, axiom, allows_pets(olive_garden)).
fof(requires_deposit_olive_garden, axiom, requires_deposit(olive_garden)).
fof(monthly_rent_olive_garden, axiom, monthly_rent(olive_garden, 2000)).

% Rules
fof(pets_allowed_implies_move_in_allowed, axiom,
    ! [B: managed_building, P: person, Pet: pet] :
      (allows_pets(B) & is_cat(Pet, P) => allowed_to_move_in_with_pet(P, Pet))).

fof(deposit_rule, axiom,
    ! [B: managed_building, D: amount] :
      (deposit(B, D) => (D = 2000 | D > 2000))).

fof(tom_renting_condition, axiom,
    (will_rent(tom, olive_garden) <=>
     (allowed_to_move_in_with_pet(tom, fluffy) &
      ? [Deposit: amount] : (deposit(olive_garden, Deposit) & Deposit =< 1500)))).

% Goal: The security deposit at the Olive Garden is either $2000 or more.
fof(goal, conjecture,
    ? [D: amount] : (deposit(olive_garden, D) & (D = 2000 | D > 2000))).