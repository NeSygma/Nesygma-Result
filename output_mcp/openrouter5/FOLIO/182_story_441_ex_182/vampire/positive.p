% Positive version: original claim as conjecture
% Premises:
% 1. No one nice to animals is also mean to animals.
% 2. Some grumpy people are mean to animals.
% 3. All animal lovers are nice to animals.
% 4. All pet owners love animals.
% 5. Tom is a pet owner.
% Conclusion: Tom is a grumpy person.

fof(premise1, axiom, ! [X] : (nice_to_animals(X) => ~mean_to_animals(X))).
fof(premise2, axiom, ? [X] : (grumpy(X) & mean_to_animals(X))).
fof(premise3, axiom, ! [X] : (animal_lover(X) => nice_to_animals(X))).
fof(premise4, axiom, ! [X] : (pet_owner(X) => loves_animals(X))).
fof(premise5, axiom, pet_owner(tom)).

% Additional: love animals => animal lover? Not given. So we need to be careful.
% The premises don't say loves_animals => animal_lover. So we cannot infer that.

fof(conclusion, conjecture, grumpy(tom)).