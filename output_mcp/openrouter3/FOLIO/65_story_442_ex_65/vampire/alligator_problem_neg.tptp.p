% All Brown Swiss cattle are cows.
fof(axiom1, axiom, ! [X] : (brown_swiss_cattle(X) => cow(X))).

% Some pets are Brown Swiss cattle.
fof(axiom2, axiom, ? [X] : (pet(X) & brown_swiss_cattle(X))).

% All cows are domesticated animals.
fof(axiom3, axiom, ! [X] : (cow(X) => domesticated(X))).

% Alligators are not domesticated animals.
fof(axiom4, axiom, ! [X] : (alligator(X) => ~domesticated(X))).

% Ted is an alligator.
fof(axiom5, axiom, alligator(ted)).

% Negated conclusion: Ted is a Brown Swiss cattle AND Ted is a pet.
fof(goal_neg, conjecture, brown_swiss_cattle(ted) & pet(ted)).