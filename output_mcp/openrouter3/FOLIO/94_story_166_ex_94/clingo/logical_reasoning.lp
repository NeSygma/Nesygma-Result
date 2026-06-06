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

% Rule: Cats are pets (already stated as fact, but for completeness)
% cat(C) :- pet(C). % Not needed since we have pet(fluffy) and cat(fluffy)

% Rule: A deposit is required to rent an apartment in a managed building
deposit_required(B) :- managed_building(B).

% Rule: The security deposit can be either equal to the monthly rent or more
% This means deposit >= monthly rent
% We'll model this as: deposit_amount(B, A) implies A >= monthly_rent(B)
% But we need to know the actual deposit amount for Olive Garden

% Rule: If a managed building allows pets, then people are allowed to move in with a pet
allowed_move_in(P, Pet, B) :- allows_pets(B), person(P), pet(Pet), managed_building(B).

% Rule: Tom will rent if allowed to move in with Fluffy AND deposit <= 1500
% This is about renting, not about being allowed to move in

% The key question: Does Olive Garden allow pets?
% Premise: "Pets are allowed in some managed buildings" - this means there exists at least one managed building that allows pets
% But it doesn't say which ones. We need to consider possibilities.

% Let's model the possibility that Olive Garden allows pets or not
% We'll use choice rules for open relations
{ allows_pets(B) } :- managed_building(B).

% Constraint: If a building allows pets, then people can move in with pets
% This is already in the rule above

% For the deposit: We need to know the deposit amount for Olive Garden
% The premise says deposit can be equal to or more than monthly rent
% So deposit >= 2000 for Olive Garden

% Let's define deposit amounts as choices (since not specified)
{ deposit_amount(B, A) : amount(A) } :- managed_building(B).

% Constraint: Deposit must be >= monthly rent
:- deposit_amount(B, A), monthly_rent(B, R), A < R.

% For Olive Garden specifically, we know monthly rent is 2000
% So deposit must be >= 2000

% Now, the conclusion: Tom is allowed to move into an apartment in The Olive Garden with Fluffy
% This requires:
% 1. Olive Garden allows pets (or at least allows Tom to move in with Fluffy)
% 2. Tom is allowed to move in with Fluffy according to the rules

% Let's derive the conclusion
conclusion_true :- 
    allowed_move_in(tom, fluffy, olive_garden).

% For conclusion to be false, we need to show that Tom is NOT allowed to move in
% This would happen if Olive Garden does NOT allow pets
conclusion_false :- 
    not allows_pets(olive_garden),
    managed_building(olive_garden).

% But wait, there's another possibility: The premises don't specify whether Olive Garden allows pets
% So we need to consider both possibilities

% Let's refine: The conclusion is about being "allowed" to move in
% According to the rule: "If a managed building allows pets, then people are allowed to move in with a pet"
% So if Olive Garden allows pets, then Tom is allowed to move in with Fluffy
% If Olive Garden does NOT allow pets, then the rule doesn't apply, and we don't know if Tom is allowed

% Actually, the rule is an implication: allows_pets(B) -> allowed_move_in(P, Pet, B)
% The contrapositive is: not allowed_move_in(P, Pet, B) -> not allows_pets(B)
% But we can't conclude the converse

% Let's think about this differently:
% The premises don't explicitly state whether Olive Garden allows pets
% So we have two possible worlds:
% 1. Olive Garden allows pets -> Tom is allowed to move in with Fluffy
% 2. Olive Garden does not allow pets -> Tom is NOT allowed to move in with Fluffy (by the rule's contrapositive?)

% Actually, the rule says: "If a managed building allows pets, then people are allowed to move in with a pet"
% This doesn't say what happens if a building doesn't allow pets
% So if Olive Garden doesn't allow pets, we cannot conclude that Tom is NOT allowed to move in
% We simply don't know

% Therefore, the conclusion is uncertain because we don't know if Olive Garden allows pets

% Let's model this properly
% We'll have two scenarios:
% Scenario 1: Olive Garden allows pets
% Scenario 2: Olive Garden does not allow pets

% In Scenario 1: Tom is allowed to move in with Fluffy (by the rule)
% In Scenario 2: We don't have information to conclude either way

% So the conclusion is uncertain

% Let's write the answer mapping
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.

% Show directives
#show answer/1.
#show allows_pets/1.
#show allowed_move_in/3.
#show deposit_amount/2.