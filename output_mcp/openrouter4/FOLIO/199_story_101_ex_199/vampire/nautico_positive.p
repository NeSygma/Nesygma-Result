% Positive file: original conclusion as conjecture
% "No one playing for Nautico is Brazilian."
fof(premise1, axiom, ailton_silva = ailton).
fof(premise2, axiom, football_player(ailton)).
fof(premise3, axiom, loaned_to(ailton, braga)).
fof(premise4, axiom, brazilian(ailton_silva)).
fof(premise5, axiom, plays_for(ailton_silva, nautico)).
fof(premise6, axiom, football_club(nautico)).
fof(premise7, axiom, football_club(braga)).
fof(premise8, axiom, football_club(fluminense)).
fof(conclusion, conjecture, ! [X] : (plays_for(X, nautico) => ~brazilian(X))).