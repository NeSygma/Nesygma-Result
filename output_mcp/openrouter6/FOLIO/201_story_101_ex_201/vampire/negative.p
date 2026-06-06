fof(premise1, axiom, ailton = ailton_silva).
fof(premise2, axiom, football_player(ailton) & loaned_to(ailton, braga)).
fof(premise3, axiom, football_player(ailton_silva) & plays_for(ailton_silva, nautico)).
fof(premise4, axiom, football_club(nautico) & football_club(braga)).
fof(premise5, axiom, football_club(fluminense)).
fof(distinct, axiom, (ailton != braga & ailton != nautico & ailton != fluminense & braga != nautico & braga != fluminense & nautico != fluminense)).
fof(goal, conjecture, ? [Y] : (football_club(Y) & loaned_to(ailton, Y))).