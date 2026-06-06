fof(axiom1, axiom, ailton_silva = ailton).
fof(axiom2, axiom, football_player(ailton)).
fof(axiom3, axiom, loaned_to(ailton, braga)).
fof(axiom4, axiom, brazilian(ailton_silva)).
fof(axiom5, axiom, plays_for(ailton_silva, nautico)).
fof(axiom6, axiom, football_club(nautico)).
fof(axiom7, axiom, football_club(braga)).
fof(axiom8, axiom, football_club(fluminense)).
fof(axiom9, axiom, nautico != braga).
fof(axiom10, axiom, nautico != fluminense).
fof(axiom11, axiom, braga != fluminense).
fof(conclusion, conjecture, ? [X] : (plays_for(X, nautico) & brazilian(X))).