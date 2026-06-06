% --- Premises ---
managed_building(olive_garden).
monthly_rent(olive_garden, 2000).

% Cats are pets.
pet(X) :- cat(X).
cat(fluffy).

% Pets are allowed in some managed buildings.
{allows_pets(B)} :- managed_building(B).

% A deposit is required to rent an apartment in a managed building.
% The security deposit can be either equal to the monthly rent at a managed building or more.
% Let's define a domain for possible deposits.
deposit_value(1500).
deposit_value(2000).
deposit_value(2500).

% A deposit D is valid for building B if D >= R.
valid_deposit(B, D) :- managed_building(B), monthly_rent(B, R), deposit_value(D), D >= R.

% If a managed building allows pets, then people are allowed to move in with a pet.
allowed_to_move_in_with_pet(B) :- allows_pets(B).

% Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy,
% and the security deposit is no more than $1500.
% Tom has a cat (Fluffy), so he needs to move in with a pet.
tom_rents(B) :- 
    managed_building(B),
    allowed_to_move_in_with_pet(B),
    valid_deposit(B, D),
    D <= 1500.

% --- Evaluation ---
% Conclusion: Tom will rent an apartment in The Olive Garden.

% 1. Positive logic for True
conclusion_true :- tom_rents(olive_garden).

% 2. Positive logic for False
% Tom rents if there exists D such that D >= 2000 AND D <= 1500.
% Since 2000 > 1500, no such D exists.
% We can prove it's false if for all possible deposits D, D > 1500.
% Since R = 2000, any valid D >= 2000.
% Thus, no D <= 1500 can exist.
conclusion_false :- 
    managed_building(olive_garden),
    monthly_rent(olive_garden, R),
    not exists_valid_deposit_le_1500(olive_garden).

exists_valid_deposit_le_1500(B) :- 
    managed_building(B),
    valid_deposit(B, D),
    D <= 1500.

% 3. Final Answer Mapping
answer(true)      :- conclusion_true.
answer(false)     :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.

#show answer/1.