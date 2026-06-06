% Negative version: negated conclusion as conjecture
% Negation of: If Ted is a Brown Swiss cattle, then Ted is not a pet.
% Negation: Ted is a Brown Swiss cattle AND Ted is a pet.

fof(premise_1, axiom, ! [X] : (brown_swiss_cattle(X) => cow(X))).
fof(premise_2, axiom, ? [X] : (pet(X) & brown_swiss_cattle(X))).
fof(premise_3, axiom, ! [X] : (cow(X) => domesticated_animal(X))).
fof(premise_4, axiom, ! [X] : (alligator(X) => ~domesticated_animal(X))).
fof(premise_5, axiom, alligator(ted)).

fof(goal_neg, conjecture, (brown_swiss_cattle(ted) & pet(ted))).