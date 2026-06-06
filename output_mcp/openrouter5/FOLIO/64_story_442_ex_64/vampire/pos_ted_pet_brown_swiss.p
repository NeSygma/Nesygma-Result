% Positive version: original conclusion as conjecture
% Conclusion: Ted is a pet and Brown Swiss cattle

fof(premise_1, axiom, ! [X] : (brown_swiss_cattle(X) => cow(X))).
fof(premise_2, axiom, ? [X] : (pet(X) & brown_swiss_cattle(X))).
fof(premise_3, axiom, ! [X] : (cow(X) => domesticated_animal(X))).
fof(premise_4, axiom, ! [X] : (alligator(X) => ~domesticated_animal(X))).
fof(premise_5, axiom, alligator(ted)).

% Distinctness: ted is a specific entity, but we don't need to assert distinctness for this problem

fof(goal, conjecture, (pet(ted) & brown_swiss_cattle(ted))).