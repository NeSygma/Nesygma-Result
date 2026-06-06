% Negative version: negated conclusion as conjecture
% Premises:
% 1. No one nice to animals is also mean to animals.
fof(premise1, axiom, ! [X] : (nice_to_animals(X) => ~mean_to_animals(X))).
% 2. Some grumpy people are mean to animals.
fof(premise2, axiom, ? [X] : (grumpy(X) & mean_to_animals(X))).
% 3. All animal lovers are nice to animals.
fof(premise3, axiom, ! [X] : (animal_lover(X) => nice_to_animals(X))).
% 4. All pet owners love animals.
fof(premise4, axiom, ! [X] : (pet_owner(X) => loves_animals(X))).
% 5. Tom is a pet owner.
fof(premise5, axiom, pet_owner(tom)).

% Negated conclusion: ~((~(grumpy(tom) & mean_to_animals(tom))) => (~grumpy(tom) & ~animal_lover(tom)))
% Which is equivalent to: (~(grumpy(tom) & mean_to_animals(tom))) & ~(~grumpy(tom) & ~animal_lover(tom))
% ~(~grumpy(tom) & ~animal_lover(tom)) = grumpy(tom) | animal_lover(tom)
% So: (~(grumpy(tom) & mean_to_animals(tom))) & (grumpy(tom) | animal_lover(tom))
fof(neg_conclusion, conjecture, (~(grumpy(tom) & mean_to_animals(tom))) & (grumpy(tom) | animal_lover(tom))).