fof(known_as, axiom, known_as(ailton_silva, ailton)).
fof(premise2, axiom, football_player(ailton)).
fof(premise2b, axiom, loaned_to(ailton, braga)).
fof(premise3, axiom, brazilian(ailton_silva)).
fof(premise3b, axiom, footballer(ailton_silva)).
fof(premise3c, axiom, plays_for(ailton_silva, nautico)).
fof(premise4, axiom, football_club(nautico)).
fof(premise4b, axiom, football_club(braga)).
fof(premise5, axiom, football_club(fluminense)).
fof(identity, axiom, ! [X] : (known_as(ailton_silva, X) => plays_for(X, nautico))).
fof(goal, conjecture, ! [X] : (football_club(X) => ~plays_for(ailton_silva, X))).