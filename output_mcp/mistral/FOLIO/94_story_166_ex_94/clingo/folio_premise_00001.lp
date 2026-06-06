% Domain
managed_building(olive_garden).
person(tom).
cat(fluffy).

% Cats are pets
pet(P) :- cat(P).

% Fluffy is Tom's cat
is_pet_of(fluffy, tom).

% Facts about The Olive Garden
rent(olive_garden, 2000).
more(2000, 1500).

% Premises
% A deposit is required to rent an apartment in a managed building
deposit_required(B) :- managed_building(B).

% The security deposit can be either equal to the monthly rent or more
deposit(B, Rent) :- deposit_required(B), rent(B, Rent).  % equal to monthly rent
deposit(B, Amount) :- deposit_required(B), rent(B, Rent), more(Amount, Rent).  % more than monthly rent

% If a managed building allows pets, then people are allowed to move in with a pet
allowed_to_move_in_with_pet(B) :- allows_pets(B).

% Tom will rent an apartment in a managed building if he is allowed to move in with Fluffy, and the security deposit is no more than $1500
% Tom is allowed to move in with Fluffy at building B if the building allows pets and Fluffy is Tom's pet
will_rent_with_pet(tom, B) :-
    managed_building(B),
    allowed_to_move_in_with_pet(B),
    is_pet_of(fluffy, tom).

will_rent(tom, B) :-
    will_rent_with_pet(tom, B),
    deposit(B, Amount),
    Amount <= 1500.

% Premise: Pets are allowed in some managed buildings
% Use a choice rule to allow some buildings to allow pets
{allows_pets(B) : managed_building(B)}.

% Ensure at least one building allows pets (as per premise)
:- not allows_pets(_).

% Conclusion: Tom is allowed to move into an apartment in The Olive Garden with Fluffy
% This means will_rent(tom, olive_garden) should be true
conclusion_true :- will_rent(tom, olive_garden).
conclusion_false :- not will_rent(tom, olive_garden).

% Answer mapping
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.
answer(inconsistent) :- conclusion_true, conclusion_false.

#show answer/1.