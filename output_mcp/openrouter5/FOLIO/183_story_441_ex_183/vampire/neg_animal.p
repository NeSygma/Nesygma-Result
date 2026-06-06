% Negative version: negated conclusion as conjecture
% Negated conclusion: Tom IS both a grumpy person and mean to animals.
% i.e., grumpy(tom) & mean_to_animals(tom)

fof(premise_1, axiom, ! [X] : (nice_to_animals(X) => ~mean_to_animals(X))).
fof(premise_2, axiom, ? [X] : (grumpy(X) & mean_to_animals(X))).
fof(premise_3, axiom, ! [X] : (animal_lover(X) => nice_to_animals(X))).
fof(premise_4, axiom, ! [X] : (pet_owner(X) => loves_animals(X))).
fof(premise_5, axiom, pet_owner(tom)).

fof(conclusion_neg, conjecture, (grumpy(tom) & mean_to_animals(tom))).