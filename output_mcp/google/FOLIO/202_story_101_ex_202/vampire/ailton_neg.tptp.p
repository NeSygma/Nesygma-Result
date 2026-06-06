fof(loaned, axiom, loaned_to(ailton_silva, braga)).
fof(plays, axiom, plays_for(ailton_silva, nautico)).
fof(club_braga, axiom, is_football_club(braga)).
fof(club_nautico, axiom, is_football_club(nautico)).
fof(club_fluminense, axiom, is_football_club(fluminense)).
fof(played_def, axiom, ! [P, C] : ((plays_for(P, C) | loaned_to(P, C)) => played_for(P, C))).
fof(distinct, axiom, (ailton_silva != braga & ailton_silva != nautico & ailton_silva != fluminense & braga != nautico & braga != fluminense & nautico != fluminense)).
fof(goal, conjecture, ~played_for(ailton_silva, fluminense)).