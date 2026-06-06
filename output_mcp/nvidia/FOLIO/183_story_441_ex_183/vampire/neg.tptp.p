% Some grumpy people are mean to animals.
fof(prefix2, axiom, ? [X] : (grumpy(X) & mean_to_animals(X))).

% All animal lovers are nice to animals.
fof(prefix3, axiom, ! [X] : (animal_lover(X) => nice_to_animals(X))).

% All pet owners love animals.
fof(prefix4, axiom, ! [X] : (pet_owner(X) => love_animals(X))).

% Tom is a pet owner.
fof(fact1, axiom, pet_owner(tom)).

% No one nice to animals is also mean to animals.
fof(prefix1, axiom, ! [X] : (nice_to_animals(X) => ~mean_to_animals(X))).

% Conclusion (negated): Tom is both grumpy and mean to animals.
fof(goal, conjecture, (grumpy(tom) & mean_to_animals(tom))).