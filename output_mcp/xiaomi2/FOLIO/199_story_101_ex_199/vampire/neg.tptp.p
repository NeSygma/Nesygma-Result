fof(premise_1, axiom, plays_for(ailton_silva, nautico)).
fof(premise_2, axiom, brazilian(ailton_silva)).
fof(premise_3, axiom, football_club(nautico)).
fof(premise_4, axiom, football_club(braga)).
fof(premise_5, axiom, football_club(fluminense)).

% Negation of conclusion: Someone playing for Nautico IS Brazilian.
% Equivalent to: ? [X] : (plays_for(X, nautico) & brazilian(X))
fof(goal, conjecture, ? [X] : (plays_for(X, nautico) & brazilian(X))).