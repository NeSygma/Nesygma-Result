fof(axiom1, axiom, football_player(ailton_silva)).
fof(axiom2, axiom, loaned_to(ailton_silva, braga)).
fof(axiom3, axiom, club(braga)).
fof(axiom4, axiom, club(nautico)).
fof(axiom5, axiom, club(fluminense)).
fof(axiom6, axiom, plays_for(ailton_silva, nautico)).
fof(distinct, axiom, (ailton_silva != braga & ailton_silva != nautico & ailton_silva != fluminense & braga != nautico & braga != fluminense & nautico != fluminense)).
fof(goal, conjecture, ? [C] : (loaned_to(ailton_silva, C) & club(C))).