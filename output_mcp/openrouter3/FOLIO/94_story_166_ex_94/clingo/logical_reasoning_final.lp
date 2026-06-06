% Logical Reasoning Problem: Pets and Deposits

% Domain declarations
building(olive_garden).
person(tom).
pet(fluffy).
cat(fluffy).
amount(2000).
amount(1500).

% Facts from premises
managed_building(olive_garden).
monthly_rent(olive_garden, 2000).
owns(tom, fluffy).
cat(fluffy).
pet(fluffy).

% Rule: A deposit is required to rent an apartment in a managed building
deposit_required(B) :- managed_building(B).

% Rule: If a managed building allows pets, then people are allowed to move in with a pet
allowed_move_in(P, Pet, B) :- allows_pets(B), person(P), pet(Pet), managed_building(B).

% The key question: Does Olive Garden allow pets?
% Premise: "Pets are allowed in some managed buildings" - this means there exists at least one managed building that allows pets
% But it doesn't say which ones. We need to consider possibilities.

% Let's model the possibility that Olive Garden allows pets or not
% We'll use choice rules for open relations
{ allows_pets(B) } :- managed_building(B).

% For the deposit: We need to know the deposit amount for Olive Garden
% The premise says deposit can be equal to or more than monthly rent
% So deposit >= 2000 for Olive Garden

% Let's define deposit amounts as choices (since not specified)
{ deposit_amount(B, A) : amount(A) } :- managed_building(B).

% Constraint: Deposit must be >= monthly rent
:- deposit_amount(B, A), monthly_rent(B, R), A < R.

% Now, the conclusion: Tom is allowed to move into an apartment in The Olive Garden with Fluffy
% This requires:
% 1. Olive Garden allows pets (or at least allows Tom to move in with Fluffy)
% 2. Tom is allowed to move in with Fluffy according to the rules

% Let's derive the conclusion
conclusion_true :- 
    allowed_move_in(tom, fluffy, olive_garden).

% For conclusion to be false, we need to show that Tom is NOT allowed to move in
% But the premises don't give us any information to conclude that Tom is NOT allowed to move in
% The rule only gives a sufficient condition for being allowed to move in, not a necessary condition
% So we cannot derive conclusion_false from the premises

% Therefore, we only have two possibilities:
% 1. If Olive Garden allows pets, then Tom is allowed to move in (conclusion_true)
% 2. If Olive Garden does NOT allow pets, then we don't know if Tom is allowed to move in (uncertain)

% But wait, the problem asks: "Based STRICTLY on the premises, is the conclusion True, False, or Uncertain?"
% This means we need to evaluate the conclusion based ONLY on the given premises
% Since the premises don't tell us whether Olive Garden allows pets, we cannot determine the truth value of the conclusion

% So the answer should be "uncertain"

% Let's write the answer mapping
answer(true) :- conclusion_true.
answer(uncertain) :- not conclusion_true.

% Show directives
#show answer/1.
#show allows_pets/1.
#show allowed_move_in/3.