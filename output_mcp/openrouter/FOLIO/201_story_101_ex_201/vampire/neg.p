% Negative version (negated conclusion)
fof(distinct_names, axiom, (ailton != ailton_silva & ailton != braga & ailton != nautico & ailton != fluminense & ailton_silva != braga & ailton_silva != nautico & ailton_silva != fluminense & braga != nautico & braga != fluminense & nautico != fluminense)).
fof(known_as, axiom, known_as(ailton_silva, ailton)).
fof(football_player_ailton, axiom, football_player(ailton)).
fof(loaned_ailton_braga, axiom, loaned_out(ailton, braga)).
fof(plays_ailton_silva_nautico, axiom, plays_for(ailton_silva, nautico)).
fof(club_nautico, axiom, football_club(nautico)).
fof(club_braga, axiom, football_club(braga)).
fof(club_fluminense, axiom, football_club(fluminense)).
fof(loaned_out_to_club_def, axiom, ! [P] : (loaned_out_to_club(P) <=> ? [C] : (loaned_out(P, C) & football_club(C)))).
fof(goal_neg, conjecture, loaned_out_to_club(ailton)).