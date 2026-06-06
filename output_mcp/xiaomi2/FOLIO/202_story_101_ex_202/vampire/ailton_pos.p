fof(known_as, axiom, known_as(ailton_silva, ailton)).
fof(premise2a, axiom, football_player(ailton)).
fof(premise2b, axiom, loaned_to(ailton, braga)).
fof(premise3a, axiom, brazilian(ailton_silva)).
fof(premise3b, axiom, football_player(ailton_silva)).
fof(premise3c, axiom, plays_for(ailton_silva, nautico)).
fof(premise4a, axiom, football_club(nautico)).
fof(premise4b, axiom, football_club(braga)).
fof(premise5, axiom, football_club(fluminense)).
fof(identity, axiom, ! [X, Y, Z] : (known_as(X, Y) => (plays_for(X, Z) <=> plays_for(Y, Z)))).
fof(identity2, axiom, ! [X, Y, Z] : (known_as(X, Y) => (loaned_to(X, Z) <=> loaned_to(Y, Z)))).
fof(goal, conjecture, plays_for(ailton_silva, fluminense)).