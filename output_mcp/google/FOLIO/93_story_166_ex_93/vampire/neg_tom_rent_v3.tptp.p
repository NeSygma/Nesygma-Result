tff(managed_building_type, type, managed_building: $tType).
tff(olive_garden, type, olive_garden: managed_building).
tff(rent, type, rent: managed_building > $int).
tff(security_deposit, type, security_deposit: managed_building > $int).
tff(allows_pets, type, allows_pets: managed_building > $o).
tff(allows_move_in_with_pet, type, allows_move_in_with_pet: managed_building > $o).
tff(rent_apartment, type, rent_apartment: (managed_building) > $o).

tff(rent_val, axiom, rent(olive_garden) = 2000).
tff(deposit_rule, axiom, ! [B: managed_building] : $greatereq(security_deposit(B), rent(B))).
tff(rent_condition, axiom, ! [B: managed_building] : ((allows_move_in_with_pet(B) & $lesseq(security_deposit(B), 1500)) => rent_apartment(B))).
tff(pet_rule, axiom, ! [B: managed_building] : (allows_pets(B) => allows_move_in_with_pet(B))).

% The condition for rent_apartment(olive_garden) is (allows_move_in_with_pet(olive_garden) & security_deposit(olive_garden) <= 1500).
% We know security_deposit(olive_garden) >= 2000.
% Therefore, security_deposit(olive_garden) <= 1500 is false.
% Therefore, the condition (allows_move_in_with_pet(olive_garden) & security_deposit(olive_garden) <= 1500) is false.
% This means the rule does not trigger to make rent_apartment(olive_garden) true.
% It does not prove it is false, but it is not provable as true.

tff(goal, conjecture, ~rent_apartment(olive_garden)).