% --- Premises ---
managed_building(olive_garden).
monthly_rent(olive_garden, 2000).
cat(fluffy).
pet(X) :- cat(X).

% Premise 1: Pets are allowed in some managed buildings.
{ allows_pets(B) } :- managed_building(B).
:- not 1 { allows_pets(B) : managed_building(B) }.

% Premise 10: If a managed building allows pets, then people are allowed to move in with a pet.
allowed_to_move_in_with_pet(P, B) :- allows_pets(B), pet(P).

% Conclusion: Tom is allowed to move into an apartment in The Olive Garden with Fluffy.
conclusion_true :- allowed_to_move_in_with_pet(fluffy, olive_garden).

% To prove False, we need to show it's impossible for him to be allowed.
% The premises do not provide a way to prove it's impossible.
% Therefore, conclusion_false cannot be derived.

% --- Answer Mapping ---
answer(true)      :- conclusion_true.
answer(false)     :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.

#show answer/1.