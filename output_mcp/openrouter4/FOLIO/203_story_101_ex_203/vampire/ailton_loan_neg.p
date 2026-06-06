fof(premise1, axiom, ailton_silva = ailton).
fof(premise2a, axiom, football_player(ailton)).
fof(premise2b, axiom, loaned_to(ailton, braga)).
fof(premise3a, axiom, football_player(ailton_silva)).
fof(premise3b, axiom, plays_for(ailton_silva, nautico)).
fof(premise4a, axiom, football_club(nautico)).
fof(premise4b, axiom, football_club(braga)).
fof(premise5, axiom, football_club(fluminense)).
fof(distinct_clubs, axiom, (braga != nautico & braga != fluminense & nautico != fluminense)).
fof(goal_neg, conjecture, ! [X] : (~football_club(X) | ~loaned_to(ailton_silva, X))).