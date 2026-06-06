% Positive version: original conclusion as conjecture
% Conclusion: Tom is not both a grumpy person and mean to animals.
% i.e., ~(grumpy(tom) & mean_to_animals(tom))

fof(premise_1, axiom, ! [X] : (nice_to_animals(X) => ~mean_to_animals(X))).
fof(premise_2, axiom, ? [X] : (grumpy(X) & mean_to_animals(X))).
fof(premise_3, axiom, ! [X] : (animal_lover(X) => nice_to_animals(X))).
fof(premise_4, axiom, ! [X] : (pet_owner(X) => loves_animals(X))).
fof(premise_5, axiom, pet_owner(tom)).

% Additional: animal lovers love animals? Actually premise says "All animal lovers are nice to animals" and "All pet owners love animals"
% But we need a link from loves_animals to animal_lover? Not given.
% Let's just encode what's given.

fof(conclusion, conjecture, ~(grumpy(tom) & mean_to_animals(tom))).