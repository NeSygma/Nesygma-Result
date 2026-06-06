% Positive test: original conclusion as conjecture
% Premise 1: No one nice to animals is also mean to animals.
fof(premise1, axiom, ! [X] : ~(nice_to_animals(X) & mean_to_animals(X))).
% Premise 2: Some grumpy people are mean to animals.
fof(premise2, axiom, ? [X] : (grumpy(X) & mean_to_animals(X))).
% Premise 3: All animal lovers are nice to animals.
fof(premise3, axiom, ! [X] : (animal_lover(X) => nice_to_animals(X))).
% Premise 4: All pet owners love animals (i.e., are animal lovers).
fof(premise4, axiom, ! [X] : (pet_owner(X) => animal_lover(X))).
% Premise 5: Tom is a pet owner.
fof(premise5, axiom, pet_owner(tom)).
% Conclusion: Tom is not both a grumpy person and mean to animals.
fof(conclusion, conjecture, ~(grumpy(tom) & mean_to_animals(tom))).